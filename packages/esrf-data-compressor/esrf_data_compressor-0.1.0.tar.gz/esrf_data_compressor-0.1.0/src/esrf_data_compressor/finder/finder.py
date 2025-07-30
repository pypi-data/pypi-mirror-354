import os
import sys
import re
import h5py
import h5py.h5d as h5d
from typing import List, Tuple, Optional


def discover_datasets(path_components: List[str], base_root: str) -> List[str]:
    raw_root = os.path.join(base_root, *path_components, "RAW_DATA")
    if not os.path.isdir(raw_root):
        sys.exit(f"ERROR: RAW_DATA path not found: {raw_root}")

    scan_re = re.compile(r"^scan\d{4}$", re.IGNORECASE)
    datasets: List[str] = []

    for sample in sorted(os.listdir(raw_root)):
        sample_dir = os.path.join(raw_root, sample)
        if not os.path.isdir(sample_dir):
            continue
        for ds in sorted(os.listdir(sample_dir)):
            ds_dir = os.path.join(sample_dir, ds)
            if not os.path.isdir(ds_dir):
                continue

            h5s = [f for f in os.listdir(ds_dir) if f.lower().endswith(".h5")]
            if len(h5s) != 1:
                if len(h5s) > 1:
                    sys.exit(f"ERROR: Multiple .h5 in {ds_dir}: {h5s}")
                continue

            if not any(
                scan_re.match(d) and os.path.isdir(os.path.join(ds_dir, d))
                for d in os.listdir(ds_dir)
            ):
                continue

            datasets.append(os.path.join(ds_dir, h5s[0]))

    if not datasets:
        sys.exit(f"ERROR: No datasets found under {raw_root}")

    return sorted(datasets)


def find_vds_files(
    path_components: List[str], base_root: str, filter_expr: Optional[str]
) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Discover each dataset HDF5, then for each top-level group (e.g. "1.1"):
      - treat each filter key "A/B/C" as a dataset path under that group,
        i.e. grp["A"]["B"]["C"][()].
      - if any filter's desired substring is found in the dataset's value,
        classify that group's VDS sources into TO COMPRESS, reason="grp/A/B/C contains 'val'".
      - otherwise into REMAINING, reason="grp/A/B/C=<actual>".

    Adds a check for datasets already compressed with the JP2KCompressor's Blosc2/Grok filter
    (ID 32026) and classifies those files as REMAINING with reason "<already compressed>".

    Returns two lists of (vds_source_path, reason).
    """
    # parse filter tokens
    filters: List[Tuple[List[str], str]] = []
    if filter_expr:
        for tok in filter_expr.split(","):
            tok = tok.strip()
            if ":" not in tok:
                sys.exit(f"ERROR: Invalid filter token '{tok}'")
            key, val = tok.split(":", 1)
            parts = [p.strip() for p in key.split("/") if p.strip()]
            if not parts:
                sys.exit(f"ERROR: Empty filter key in '{tok}'")
            filters.append((parts, val.strip()))

    to_compress: List[Tuple[str, str]] = []
    remaining: List[Tuple[str, str]] = []

    datasets = discover_datasets(path_components, base_root)

    for cont_path in datasets:
        with h5py.File(cont_path, "r") as f:
            for grp_name, grp in f.items():
                if not isinstance(grp, h5py.Group):
                    continue

                # determine if group matches filter criteria
                group_matched = False
                reason = ""
                for parts, desired in filters:
                    obj = grp
                    for p in parts:
                        obj = obj.get(p)
                        if obj is None:
                            break
                    actual = obj[()] if isinstance(obj, h5py.Dataset) else None
                    if actual is not None and desired in str(actual):
                        reason = f"{grp_name}/{'/'.join(parts)} contains '{desired}'"
                        group_matched = True
                        break
                    else:
                        reason = f"{grp_name}/{'/'.join(parts)}={actual!r}"
                if not filters:
                    reason = f"{grp_name}/<no filter>"

                # harvest VDS sources under this group, detecting existing compression
                def visitor(name, obj):
                    if not isinstance(obj, h5py.Dataset):
                        return
                    plist = obj.id.get_create_plist()
                    if plist.get_layout() != h5d.VIRTUAL:
                        return

                    for i in range(plist.get_virtual_count()):
                        fn = plist.get_virtual_filename(i)
                        if not os.path.isabs(fn):
                            fn = os.path.abspath(
                                os.path.join(os.path.dirname(cont_path), fn)
                            )

                        # inspect file for Blosc2/Grok (JP2K) compression filter
                        already_compressed = False
                        try:
                            with h5py.File(fn, "r") as src:
                                comp_flag = [False]

                                def _check(name2, obj2):
                                    if isinstance(obj2, h5py.Dataset):
                                        plist2 = obj2.id.get_create_plist()
                                        for j in range(plist2.get_nfilters()):
                                            fid = plist2.get_filter(j)[0]
                                            if fid == 32026:
                                                comp_flag[0] = True
                                                return

                                src.visititems(_check)
                                already_compressed = comp_flag[0]
                        except Exception:
                            already_compressed = False

                        if already_compressed:
                            rem_reason = f"{grp_name}/<already compressed>"
                            remaining.append((fn, rem_reason))
                        else:
                            if group_matched:
                                to_compress.append((fn, reason))
                            else:
                                remaining.append((fn, reason))

                grp.visititems(visitor)

    if not to_compress and not remaining:
        sys.exit(f"ERROR: No VDS sources found under {base_root}/{path_components}")

    return to_compress, remaining


def write_report(
    to_list: List[Tuple[str, str]], rem_list: List[Tuple[str, str]], output_path: str
):
    with open(output_path, "w") as rpt:
        rpt.write("## TO COMPRESS ##\n")
        if to_list:
            for p, r in to_list:
                rpt.write(f"{p}    # {r}\n")
        else:
            rpt.write("(none)\n")

        rpt.write("\n## REMAINING ##\n")
        if rem_list:
            for p, r in rem_list:
                rpt.write(f"{p}    # {r}\n")
        else:
            rpt.write("(none)\n")
