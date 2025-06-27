import pandas as pd
import os

from collections import Counter

def analyze_files_with_groups(file_paths,
                              out_csv="insitu_results_all.csv",
                              out_csv_by_mouse="insitu_results_by_mouse.csv"):
    # 1) define your group mapping
    group_map = {
        "9693": "sgRosa26",
        "9794": "sgRosa26",
        "128": "sgRosa26",
        "131": "sgRosa26",
        "132": "sgRosa26",
        "9935": "sgTrpc6",
        "9936": "sgTrpc6",
        "9937": "sgTrpc6",
        "1299": "sgTrpc6",
        "121": "sgTrpc6",
        "123": "sgTrpc6", 
    }

    all_records = []
    combos = {
        "Th": frozenset(["Th"]),
        "Trpc6": frozenset(["Trpc6"]),
        "Th:Trpc6": frozenset(["Th","Trpc6"])
    }
    markers = ["Th","Trpc6"]
    in_set = lambda s,m: m in s

    for path in file_paths:
        fn = os.path.basename(path)       # e.g. "1299_1.csv"
        name, _ = os.path.splitext(fn)    # "1299_1"
        mouse_ID, slice_ = name.split("_",1)
        group = group_map.get(mouse_ID, "Unknown")

        df = pd.read_csv(path)
        df["marker_set"] = df["Classification"]\
                             .fillna("")\
                             .apply(lambda c: frozenset(p.strip() for p in c.split(":") if p.strip()))

        # counts
        cnts = Counter(df["marker_set"])
        for label, fset in combos.items():
            all_records.append({
                "Group":    group,
                "mouse_ID": mouse_ID,
                "slice":    slice_,
                "Metric":   "Count",
                "Label":    label,
                "Value":    cnts[fset]
            })

        # mean intensities overall
        for m in markers:
            mask = df["marker_set"].apply(lambda s: in_set(s,m))
            μ = df.loc[mask, f"Cell: {m} mean"].mean()
            all_records.append({
                "Group":    group,
                "mouse_ID": mouse_ID,
                "slice":    slice_,
                "Metric":   "Mean_all",
                "Label":    m,
                "Value":    μ
            })

        # within Th⁺
        th_mask = df["marker_set"].apply(lambda s: in_set(s,"Th"))
        for m in markers:
            mask = th_mask & df["marker_set"].apply(lambda s: in_set(s,m))
            μ = df.loc[mask, f"Cell: {m} mean"].mean()
            all_records.append({
                "Group":    group,
                "mouse_ID": mouse_ID,
                "slice":    slice_,
                "Metric":   "Mean_Th_pos",
                "Label":    m,
                "Value":    μ
            })

        # within Th⁻
        th_neg_mask = df["marker_set"].apply(lambda s: not in_set(s,"Th"))
        for m in markers:
            mask = th_neg_mask & df["marker_set"].apply(lambda s: in_set(s,m))
            μ = df.loc[mask, f"Cell: {m} mean"].mean()
            all_records.append({
                "Group":    group,
                "mouse_ID": mouse_ID,
                "slice":    slice_,
                "Metric":   "Mean_Th_neg",
                "Label":    m,
                "Value":    μ
            })

    # build full DataFrame
    results_df = pd.DataFrame.from_records(all_records)
    cols = ["Group","mouse_ID","slice","Metric","Label","Value"]
    results_df = results_df[cols]
    results_df.to_csv(out_csv, index=False)
    print(f"Slice‐level metrics saved to {out_csv}")

    # average across slices for each mouse_ID
    averaged_df = (results_df
        .groupby(["Group","mouse_ID","Metric","Label"], as_index=False)["Value"]
        .mean()
    )
    averaged_df.to_csv(out_csv_by_mouse, index=False)
    print(f"Mouse‐level averages saved to {out_csv_by_mouse}")

    return results_df, averaged_df

# Example usage:
if __name__ == "__main__":
    files = [   "1299_1.csv","1299_2.csv","1299_4.csv",
                "9693_1.csv","9693_2.csv","9693_3.csv",
                "9794_1.csv","9794_2.csv","9794_3.csv",
                "9935_2.csv","9935_3.csv",
                "9936_1.csv","9936_2.csv","9936_3.csv",
                "9937_2.csv","9937_3.csv","9937_4.csv",
                "121_1.csv","121_2.csv","121_3.csv",
                "123_1.csv","123_2.csv","123_3.csv",
                "128_1.csv","128_2.csv","128_3.csv",
                "131_1.csv","131_2.csv","131_3.csv"
                ]
    slice_df, mouse_df = analyze_files_with_groups(files)