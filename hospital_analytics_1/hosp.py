import pandas as pd
import os
import matplotlib.pyplot as plt

# -------------------------------------------------
# 1. Load datasets into variables
# -------------------------------------------------
patients = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Patients_20250909_193847.xlsx")
supply_chain = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Supply_Chain_20250909_193847.xlsx")
analytics = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Analytics_20250909_193847.xlsx")
hospital = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Hospital_Dataset_20250909_193847.xlsx")
inventory = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Inventory_20250909_193847.xlsx")
transactions = pd.read_csv(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Transactions_2024_20250909_193847.csv")

# -------------------------------------------------
# 2. Put them into a dictionary
# -------------------------------------------------
dfs = {
    "Patients": patients,
    "Supply_Chain": supply_chain,
    "Analytics": analytics,
    "Hospital": hospital,
    "Inventory": inventory,
    "Transactions": transactions
}

# -------------------------------------------------
# 3. Define important columns
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
# 4. Function to compute mean & median
# -------------------------------------------------
def compute_summary(df, columns):
    summary = {}
    for col in columns:
        if col in df.columns:
            summary[col] = {
                "mean": df[col].mean(),
                "median": df[col].median()
            }
    return pd.DataFrame(summary).T
base_folder = r"C:\Users\Sanskriti Singh\OneDrive\Desktop\Hospital_Analytics_1"
summaries_folder = os.path.join(base_folder, "summaries")

os.makedirs(summaries_folder, exist_ok=True)

# -------------------------------------------------
# 5. Generate summaries
# -------------------------------------------------
summaries = {}
for name, df in dfs.items():
    summaries[name] = compute_summary(df, cols[name])
    print(f"\n===== {name} Summary =====")
    print(summaries[name])

# -------------------------------------------------
# 6. Save to Excel
# -------------------------------------------------
with pd.ExcelWriter("Healthcare_Summary_Report.xlsx") as writer:
    for name, summary in summaries.items():
        summary.to_excel(writer, sheet_name=name)

print("\n📊 Summary report saved to Healthcare_Summary_Report.xlsx")
import os

# -------------------------------------------------
# 6. Save to Excel with absolute path
# -------------------------------------------------
output_file = r"C:\Users\Sanskriti Singh\DownloadsHealthcare_Summary_Report.xlsx"
abs_path = os.path.abspath(output_file)

with pd.ExcelWriter(abs_path) as writer:
    for name, summary in summaries.items():
        summary.to_excel(writer, sheet_name=name)

print(f"\n📊 Summary report saved to: {abs_path}")
# -------------------------------
# 3. Helper function for charts
# -------------------------------
import os

charts_dir = "charts"
os.makedirs(charts_dir, exist_ok=True)


def save_hist_boxplot(df, column, filename_prefix):
    """Generate histogram for a given column."""
    if column not in df.columns:
        print(f"⚠️ Column {column} not found in dataset")
        return
    
    plt.figure(figsize=(6, 4))
    df[column].dropna().hist(bins=30)
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f"{filename_prefix}.png"))
    plt.close()
    
    
def show_hist_boxplot(df, column):
    """Show histogram and boxplot for a given column interactively."""
    if column not in df.columns:
        print(f"⚠️ Column {column} not found in dataset")
        return
    
    # Histogram
    plt.figure(figsize=(6, 4))
    df[column].dropna().hist(bins=30)
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()   # 👈 this will display the plot

def save_and_show(df, column, title_prefix=""):
    if column not in df.columns:
        print(f"⚠️ Column '{column}' not found. Available: {list(df.columns)}")
        return

    series = pd.to_numeric(df[column], errors="coerce").dropna()
    if series.empty:
        print(f"⚠️ Column '{column}' has no numeric data")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # Histogram
    axes[0].hist(series, bins=30)
    axes[0].set_title(f"{title_prefix} Histogram of {column}")
    axes[0].set_xlabel(column)
    axes[0].set_ylabel("Frequency")

    # Boxplot
    axes[1].boxplot(series, vert=False)
    axes[1].set_title(f"{title_prefix} Boxplot of {column}")
    axes[1].set_xlabel(column)

    plt.tight_layout()

    # ✅ Save chart before showing
    filename = f"{title_prefix}_{column}.png".replace(" ", "_")
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close(fig)  # Close figure so it's saved properly

    print(f"✅ Saved chart to: {filepath}")

# -------------------------------
# 3. Call the function for every desired chart
# -------------------------------
# Patients
show_hist_boxplot(patients, "length_of_stay")
show_hist_boxplot(patients, "complexity_score")

# Supply Chain
show_hist_boxplot(supply_chain, "ordered_quantity")
show_hist_boxplot(supply_chain, "unit_price")
show_hist_boxplot(supply_chain, "total_value")

# Analytics
show_hist_boxplot(analytics, "total_spending")
show_hist_boxplot(analytics, "avg_transaction_cost")
show_hist_boxplot(analytics, "transaction_count")
show_hist_boxplot(analytics, "revenue_lost")

# Hospital
show_hist_boxplot(hospital, "bed_capacity")
show_hist_boxplot(hospital, "annual_budget")

# Inventory
show_hist_boxplot(inventory, "current_stock")
show_hist_boxplot(inventory, "days_of_stock")
show_hist_boxplot(inventory, "stock_value")
show_hist_boxplot(inventory, "turnover_rate")

# Transactions
show_hist_boxplot(transactions, "quantity_consumed")
show_hist_boxplot(transactions, "unit_cost")
show_hist_boxplot(transactions, "total_cost")
show_hist_boxplot(transactions, "revenue_lost")
import pandas as pd
import matplotlib.pyplot as plt   # 👈 this is required

# Load dataset
patients = pd.read_excel(r"C:\Users\Sanskriti Singh\Downloads\Enhanced_Patients_20250909_193847.xlsx")

# Function to show histogram + boxplot
def show_hist_boxplot(df, column, title_prefix=""):
    if column not in df.columns:
        print(f"⚠️ Column '{column}' not found in dataset")
        return

    series = pd.to_numeric(df[column], errors="coerce").dropna()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # Histogram
    axes[0].hist(series, bins=30)
    axes[0].set_title(f"{title_prefix} Histogram of {column}")
    axes[0].set_xlabel(column)
    axes[0].set_ylabel("Frequency")

    # Boxplot
    axes[1].boxplot(series, vert=False)
    axes[1].set_title(f"{title_prefix} Boxplot of {column}")
    axes[1].set_xlabel(column)

    plt.tight_layout()
    plt.show()
def save_and_show(df, column, title_prefix=""):
    if column not in df.columns:
        print(f"⚠️ Column '{column}' not found in dataset. Available: {list(df.columns)}")
        return

    series = pd.to_numeric(df[column], errors="coerce").dropna()
    if series.empty:
        print(f"⚠️ Column '{column}' has no numeric data")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # Histogram
    axes[0].hist(series, bins=30)
    axes[0].set_title(f"{title_prefix} Histogram of {column}")
    axes[0].set_xlabel(column)
    axes[0].set_ylabel("Frequency")

    # Boxplot
    axes[1].boxplot(series, vert=False)
    axes[1].set_title(f"{title_prefix} Boxplot of {column}")
    axes[1].set_xlabel(column)

    plt.tight_layout()

    # ✅ Save chart
    filename = f"{title_prefix}_{column}.png".replace(" ", "_")
    filepath = os.path.join(charts_dir, filename)
    plt.savefig(filepath)
    print(f"✅ Saved: {filepath}")

    # Show chart interactively
    plt.show()

# -------------------------------
# 4. Example calls
# -------------------------------
save_and_show(patients, "length_of_stay")
save_and_show(supply_chain, "ordered_quantity")
save_and_show(analytics, "total_spending")
save_and_show(hospital, "bed_capacity")
save_and_show(inventory, "current_stock")
save_and_show(transactions, "total_cost")