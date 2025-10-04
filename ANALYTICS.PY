import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------------------------
# 1. Load datasets into variables
# -------------------------------------------------
patients = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Patients_20250909_193847.xlsx")
supply_chain = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Supply_Chain_20250909_193847.xlsx")
analytics = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Analytics_20250909_193847.xlsx")
hospital = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Hospital_Dataset_20250909_193847.xlsx")
inventory = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Inventory_20250909_193847.xlsx")
transactions = pd.read_csv(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Transactions_2024_20250909_193847.csv")

dfs = {
    "Patients": patients,
    "Supply_Chain": supply_chain,
    "Analytics": analytics,
    "Hospital": hospital,
    "Inventory": inventory,
    "Transactions": transactions
}

# -------------------------------------------------
# 2. Important columns for analysis
# -------------------------------------------------
cols = {
    "Patients": ["length_of_stay", "complexity_score"],
    "Supply_Chain": ["ordered_quantity", "unit_price", "total_value"],
    "Analytics": ["total_spending", "avg_transaction_cost", "transaction_count", "revenue_lost", "formulary_adherence_pct"],
    "Hospital": ["bed_capacity", "annual_budget"],
    "Inventory": ["current_stock", "days_of_stock", "stock_value", "turnover_rate"],
    "Transactions": ["quantity_consumed", "unit_cost", "total_cost", "revenue_lost"]
}

# -------------------------------------------------
# 3. Folder to save charts
# -------------------------------------------------
charts_dir = "charts"
os.makedirs(charts_dir, exist_ok=True)

# -------------------------------------------------
# 4. Function: compute mean & median
# -------------------------------------------------
def compute_summary(df, columns):
    summary = {}
    for col in columns:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            if not series.empty:
                summary[col] = {
                    "mean": series.mean(),
                    "median": series.median()
                }
    return pd.DataFrame(summary).T

# -------------------------------------------------
# 5. Function: save histogram + boxplot
# -------------------------------------------------
def save_hist_boxplot(df, column, dataset_name):
    if column not in df.columns:
        print(f"⚠️ Column '{column}' not found in {dataset_name}")
        return
    
    series = pd.to_numeric(df[column], errors="coerce").dropna()
    if series.empty:
        print(f"⚠️ Column '{column}' in {dataset_name} has no numeric data")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # Histogram
    axes[0].hist(series, bins=30)
    axes[0].set_title(f"{dataset_name} Histogram of {column}")
    axes[0].set_xlabel(column)
    axes[0].set_ylabel("Frequency")

    # Boxplot
    axes[1].boxplot(series, vert=False)
    axes[1].set_title(f"{dataset_name} Boxplot of {column}")
    axes[1].set_xlabel(column)

    plt.tight_layout()

    filename = f"{dataset_name}_{column}.png".replace(" ", "_")
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close(fig)

    print(f"✅ Saved: {filepath}")

# -------------------------------------------------
# 6. Generate summaries + plots for each dataset
# -------------------------------------------------
summaries = {}
for name, df in dfs.items():
    print(f"\n===== {name} Summary =====")
    summaries[name] = compute_summary(df, cols[name])
    print(summaries[name])

    # Generate charts for all important columns
    for col in cols[name]:
        save_hist_boxplot(df, col, name)
