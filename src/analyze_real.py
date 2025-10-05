import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "outputs" / "phoenix_civic.db"
OUT = ROOT / "outputs"

def run_query(sql):
    con = sqlite3.connect(DB)
    try:
        return pd.read_sql_query(sql, con)
    finally:
        con.close()

def save_chart(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, bbox_inches="tight", dpi=140)

def plot_water_trend():
    sql = '''
    SELECT year, month, million_gallons,
           LAG(million_gallons) OVER (ORDER BY year, month) AS prev_mg
    FROM phoenix_water_production
    ORDER BY year, month
    '''
    df = run_query(sql)

    # Coerce to numeric (handles commas/blanks)
    to_num = lambda s: pd.to_numeric(s.astype(str).str.replace(",", "").str.strip(), errors="coerce")
    df["million_gallons"] = to_num(df["million_gallons"])
    df["year"]  = pd.to_numeric(df["year"], errors="coerce")
    df["month"] = pd.to_numeric(df["month"], errors="coerce")
    df = df.dropna(subset=["million_gallons","year","month"]).sort_values(["year","month"])
    if df.empty:
        print("No water data after cleaning; skipping plot.")
        return df

    df["ym"] = df["year"].astype(int).astype(str) + "-" + df["month"].astype(int).astype(str).str.zfill(2)

    # IMPORTANT: grab the figure from the axis returned by pandas
    ax = df.plot(kind="line", x="ym", y="million_gallons", marker="o", legend=False)
    ax.set_title("Phoenix Water Production (Million Gallons)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Million Gallons")
    step = max(1, len(df)//12)
    ax.set_xticks(range(0, len(df), step))
    ax.set_xticklabels(df["ym"][::step], rotation=45)

    fig = ax.get_figure()
    fig.tight_layout()
    save_chart(fig, "water_production_trend_real.png")
    plt.close(fig)
    return df

def calls_top_types():
    sql = """
    SELECT final_call_type, COUNT(*) AS call_count
    FROM phoenix_calls_for_service
    GROUP BY final_call_type
    ORDER BY call_count DESC
    LIMIT 20;
    """
    df = run_query(sql)
    # Clean text just in case
    df["final_call_type"] = df["final_call_type"].fillna("Unknown").astype(str).str.strip()
    df["call_count"] = pd.to_numeric(df["call_count"], errors="coerce")
    df = df.dropna(subset=["call_count"]).sort_values("call_count", ascending=True)  # ascending for barh
    if df.empty:
        print("No calls data; skipping plot.")
        return df

    ax = df.plot(kind="barh", x="final_call_type", y="call_count", legend=False)
    ax.set_title("Top Calls for Service Types")
    ax.set_xlabel("Count")
    ax.set_ylabel("Call Type")

    fig = ax.get_figure()
    fig.tight_layout()
    save_chart(fig, "calls_top_types.png")
    plt.close(fig)
    return df

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    wt = plot_water_trend()
    ct = calls_top_types()
    wt.to_csv(OUT / "water_production_trend.csv", index=False)
    ct.to_csv(OUT / "calls_top_types.csv", index=False)
    print("Analysis complete. See outputs/.")

if __name__ == "__main__":
    main()
