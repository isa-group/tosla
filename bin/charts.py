import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rdflib import Graph
from matplotlib.ticker import PercentFormatter
from tabulate import tabulate
import numpy as np

# CQ1: Number of services per provider
def plot_CQ1_services(df1):
    if df1.empty:
        print("No results for CQ1.")
    else:
        counts = df1["provider"].value_counts().sort_index()
        counts.plot(
            kind="bar",
            color=sns.color_palette("Set2", n_colors=len(counts)),
            figsize=(6, 4),
            title="Number of Services per Provider",
            xlabel="Provider",
            ylabel="Services"
        )
        plt.tight_layout()
        plt.show()

# CQ2: Target objective per SLI and provider
def plot_CQ2_metrics(df2, shorten, to_num):
    if df2.empty:
        print("No results for CQ2.")
        return

    df = df2.copy()

    for col in ["SLI", "operator", "objectiveValue", "service", "provider"]:
        if col in df.columns:
            df[col] = df[col].map(shorten)

    if "objectiveValue" not in df.columns:
        print("No 'objectiveValue' column in CQ2 results.")
        return

    df["targetObjective"] = df["objectiveValue"].map(to_num)

    long = (
        df.dropna(subset=["targetObjective"])
          .groupby(["provider", "service", "SLI"], as_index=False)["targetObjective"].max()
          .sort_values(["provider", "service", "SLI"])
    )

    if long.empty:
        print("No numeric target objectives to display.")
        return

    wide = (
        long
        .pivot(index=["provider", "service"], columns="SLI", values="targetObjective")
        .reset_index()
    )

    if wide.empty:
        print("Nothing to display after pivot.")
        return

    new_cols = {}
    for c in wide.columns:
        if c not in ["provider", "service"]:
            new_cols[c] = f"{c} (target objective)"
    wide = wide.rename(columns=new_cols)

    print(tabulate(wide, headers="keys", tablefmt="grid", showindex=False))


# CQ3: SLI coverage by service and provider
from tabulate import tabulate

def plot_CQ3_sli(df3, shorten):
    if df3.empty:
        print("No results for CQ3.")
        return

    df = df3.copy()

    for c in ["service", "SLI", "provider"]:
        if c in df.columns:
            df[c] = df[c].map(shorten)

    coverage = (
        df.groupby(["provider", "SLI"])["service"]
          .nunique()
          .reset_index(name="num_services")
          .sort_values(["provider", "SLI"])
    )

    if coverage.empty:
        print("No SLI coverage to display.")
        return

    summary = (
        coverage.groupby("provider")["SLI"]
                .nunique()
                .reset_index(name="num_SLIs")
                .sort_values("num_SLIs", ascending=False)
    )

    print("Number of distinct guaranteed SLIs per provider:")
    print(tabulate(summary, headers="keys", tablefmt="grid", showindex=False))

    pivot = (
        coverage
        .pivot(index="provider", columns="SLI", values="num_services")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    print("\nNumber of services that guarantee each SLI (per provider):")
    print(tabulate(pivot, headers="keys", tablefmt="grid", showindex=False))



# CQ4: Compensation relationship between SLI threshold and credit
def to_percent(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x)
    m = re.search(r"[-+]?\d*\.?\d+", s)
    if not m:
        return None
    v = float(m.group())
    return v if "%" in s else (v * 100 if v <= 1.5 else v)

def parse_interval_threshold(s):
    if not isinstance(s, str) or not s:
        return None
    pairs = re.findall(r"(≤|<|≥|>|=)\s*([-+]?\d*\.?\d+)", s)
    if not pairs:
        m = re.search(r"[-+]?\d*\.?\d+", s)
        thr = float(m.group()) if m else None
    else:
        upp = [float(v) for op, v in pairs if op in ("<", "≤")]
        low = [float(v) for op, v in pairs if op in (">", "≥")]
        eq = [float(v) for op, v in pairs if op == "="]
        thr = eq[0] if eq else (min(upp) if upp else (max(low) if low else None))
    return thr * 100 if thr is not None and thr <= 1.5 else thr

def plot_CQ4_compensations(df4, shorten):
    if df4.empty:
        print("No results for CQ4.")
    else:
        for c in ["service", "compensation", "SLI", "provider", "interval", "credit"]:
            if c in df4.columns and c in ["service", "compensation", "SLI", "provider"]:
                df4[c] = df4[c].map(shorten)

        df4["credit_pct"] = df4.get("credit").map(to_percent) if "credit" in df4 else None
        df4["threshold_pct"] = df4.get("interval").map(parse_interval_threshold) if "interval" in df4 else None

        df_scatter = df4.dropna(subset=["credit_pct", "threshold_pct"])
        if df_scatter.empty:
            print("Not enough data for scatter plot.")
        else:

            jitter_x = np.random.normal(0, 0.3, size=len(df_scatter))
            jitter_y = np.random.normal(0, 0.3, size=len(df_scatter))
            df_scatter["threshold_jitter"] = df_scatter["threshold_pct"] + jitter_x
            df_scatter["credit_jitter"] = df_scatter["credit_pct"] + jitter_y

            sns.set_theme(style="whitegrid")
            plt.figure(figsize=(10, 6))
            ax = sns.scatterplot(
                data=df_scatter,
                x="threshold_jitter",
                y="credit_jitter",
                hue="provider",
                style="SLI",
                s=140,
                palette="Set2",
                edgecolor="black",
                linewidth=0.6,
                alpha=0.7
            )

            ax.set_xlabel("SLI threshold (%)", fontsize=12)
            ax.set_ylabel("Credit compensation (%)", fontsize=12)
            ax.xaxis.set_major_formatter(PercentFormatter())
            ax.yaxis.set_major_formatter(PercentFormatter())
            ax.set_title("Compensation Relationship: SLI Threshold vs. Credit", fontsize=16, pad=20)

            ax.legend(
                title="Provider / SLI",
                bbox_to_anchor=(1.02, 1),
                loc="upper left",
                frameon=False
            )
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()

# CQ5: Guarantee responsibilities by provider
def plot_CQ5_providers(df5, shorten):
    if df5.empty:
        print("No results for CQ5.")
    else:
        if "provider" in df5.columns:
            df5["provider"] = df5["provider"].map(shorten)

        totals = df5["provider"].value_counts().reset_index()
        totals.columns = ["provider", "count"]

        plt.figure(figsize=(8, 5))
        ax = sns.barplot(data=totals, x="provider", y="count", palette="Set2")

        ax.set_title("Guarantee responsibilities by provider", fontsize=15, pad=15)
        ax.set_xlabel("Provider", fontsize=12)
        ax.set_ylabel("Number of guarantees", fontsize=12)
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.show()


# CQ6: Responsibility distribution by type
def plot_CQ6_responsibilities(df6, shorten):
    if df6.empty:
        print("No results for CQ6.")
    else:
        for c in ["liabilityType", "liableParty", "provider"]:
            if c in df6.columns:
                df6[c] = df6[c].map(shorten)

        df6["liableParty"] = (
            df6["liableParty"]
            .astype(str)
            .str.replace(r"(?i)^(customer|client|user|tenant).*", "Customer", regex=True)
        )

        counts = (
            df6.groupby(["liabilityType", "liableParty"])
            .size()
            .reset_index(name="count")
        )
        counts["percent"] = counts.groupby("liabilityType")["count"].transform(lambda s: 100 * s / s.sum())

        hue_order = ["Customer"] + [x for x in counts["liableParty"].unique() if x != "Customer"]

        plt.figure(figsize=(9, 5))
        ax = sns.barplot(
            data=counts,
            x="liabilityType",
            y="percent",
            hue="liableParty",
            hue_order=hue_order,
            palette="Set2"
        )
        ax.set_title("Responsibility distribution by type")
        ax.set_xlabel("Responsibility type")
        ax.set_ylabel("Percentage (%)")
        ax.tick_params(axis="x", rotation=20)
        ax.legend(title="Responsible party", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        plt.show()
        

# Alibaba unfair-terms clauses heatmap
def heatmap_Alibaba_utd(utd):
    if utd.empty:
        print("No results for Alibaba unfair-terms queries.")
    else:
        pv = utd.pivot(index="category", columns="document", values="count").fillna(0)
        pv = pv.loc[pv.sum(axis=1).sort_values(ascending=False).index]

        pretty_index = [c.replace("_", " ").title() for c in pv.index]
        pv.index = pretty_index

        h, w = pv.shape
        plt.figure(figsize=(max(6.8, 1.2*w), max(4.5, 0.6*h)))

        ax = sns.heatmap(
            pv,
            cmap="OrRd",
            vmin=0,
            linewidths=0.8,
            linecolor="white",
            cbar_kws={"label": "Count"},
            annot=False 
        )
        vmax = pv.values.max()
        thresh = 0.6 * vmax if vmax > 0 else 0
        for (i, j), val in np.ndenumerate(pv.values):
            if val > 0:
                ax.text(
                    j + 0.5, i + 0.5, f"{int(val)}",
                    ha="center", va="center",
                    fontsize=12, fontweight="bold",
                    color=("white" if val >= thresh else "black")
                )

        ax.set_title("Alibaba — Potentially Unfair Clauses (SLA vs. TOS)", fontsize=16, pad=14)
        ax.set_xlabel("Document", fontsize=12)
        ax.set_ylabel("Category", fontsize=12)
        plt.tight_layout()
        plt.show()

# Unfair terms heatmap by provider SLA agreements  
def heatmap_sla_utd(utd):
    if utd.empty:
        print("No results for unfair terms.")
    else:
        pv = utd.pivot(index="category", columns="provider", values="count").fillna(0)
        cat_order = utd.groupby("category")["count"].sum().sort_values(ascending=False).index
        pv = pv.reindex(cat_order)

        h, w = pv.shape
        plt.figure(figsize=(max(7, 1.1 * w), max(4.5, 0.7 * h)))

        ax = sns.heatmap(
            pv,
            cmap="OrRd",
            vmin=0,
            linewidths=0.8,
            linecolor="white",
            cbar_kws={"label": "Count"},
            annot=False
        )

        for (i, j), val in np.ndenumerate(pv.values):
            if val > 0:
                ax.text(
                    j + 0.5,
                    i + 0.5,
                    f"{int(val)}",
                    ha="center",
                    va="center",
                    fontsize=12,
                    fontweight="bold",
                    color="black" if val < pv.values.max() * 0.7 else "white",
                )

        ax.set_title("Unfair terms per provider", fontsize=16, pad=14)
        ax.set_xlabel("Provider", fontsize=12)
        ax.set_ylabel("Category", fontsize=12)

        plt.tight_layout()
        plt.show()


# Total number of obligations, prohibitions, and permissions
def total_normative_rules(df_norm):
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(
        data=df_norm,
        x="kind",
        y="value",
        hue="provider",
        palette="Set2"
    )

    ax.set_title("Total number of rules by type and service", fontsize=15, pad=15)
    ax.set_xlabel("Rule type", fontsize=12)
    ax.set_ylabel("Total number of rules", fontsize=12)
    ax.legend(title="Provider", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()
