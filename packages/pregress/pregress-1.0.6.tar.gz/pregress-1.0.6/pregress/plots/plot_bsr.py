import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_bsr(model, type="predictors", top_n=5, annotate=True):
    """
    Plot results from a best subset regression model.

    Parameters:
    model (statsmodels object): Output of `bsr()` with .bsr_results, .best_by_k, and .bsr_metric.
    type (str): 'line', 'bar', or 'predictors'.
    top_n (int): Number of top models to display (applies to 'bar' and 'predictors').
    annotate (bool): Whether to annotate the best metric value on the plot.
    """
    if not hasattr(model, "bsr_results") or not hasattr(model, "best_by_k") or not hasattr(model, "bsr_metric"):
        raise ValueError("Model must have .bsr_results, .best_by_k, and .bsr_metric attributes.")

    results_df = model.bsr_results.copy()
    feature_col = "Features"
    metric = model.bsr_metric

    metric_column = {
        "adjr2": "Adj. R-squared",
        "aic": "AIC",
        "bic": "BIC",
        "rmse": "RMSE"
    }

    col = metric_column[metric]
    results_df["Num Predictors"] = results_df[feature_col].apply(len)

    # Reconstruct best_df using best_by_k dictionary
    best_rows = []
    for k, feats in model.best_by_k.items():
        match = results_df[results_df[feature_col].apply(lambda f: sorted(f) == sorted(feats))]
        if not match.empty:
            best_rows.append(match.iloc[0])
    best_df = pd.DataFrame(best_rows)
    best_df["Num Predictors"] = best_df[feature_col].apply(len)

    if type == "line":
        plt.figure(figsize=(10, 6))
        plt.plot(best_df["Num Predictors"], best_df[col], marker="o")

        if annotate:
            if metric == "adjr2":
                best_row = best_df.loc[best_df[col].idxmax()]
            else:
                best_row = best_df.loc[best_df[col].idxmin()]
            x = best_row["Num Predictors"]
            y = best_row[col]
            plt.text(x, y, f"{y:.2f}", ha="center", va="bottom", fontweight="bold")

        plt.xlabel("Number of Predictors")
        plt.ylabel(col)
        plt.title(f"{col} by Number of Predictors")
        plt.xticks(np.arange(best_df["Num Predictors"].min(),
                             best_df["Num Predictors"].max() + 1, step=1))
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    elif type == "bar":
        ascending = (metric != "adjr2")
        top = best_df.sort_values(by=col, ascending=ascending).head(top_n)

        plt.figure(figsize=(10, 6))
        bars = plt.bar(top["Num Predictors"], top[col], width=0.6)

        if annotate:
            best_row = top.loc[top[col].idxmax() if metric == "adjr2" else top[col].idxmin()]
            x = best_row["Num Predictors"]
            y = best_row[col]
            plt.text(x, y, f"{y:.2f}", ha='center', va='bottom', fontweight="bold")

        plt.xlabel("Number of Predictors")
        plt.ylabel(col)
        plt.title(f"Top {top_n} Best Models by {col}")

        min_val, max_val = top[col].min(), top[col].max()
        margin = (max_val - min_val) * 0.1 if max_val != min_val else 1
        plt.ylim(min_val - margin, max_val + margin)

        plt.xticks(top["Num Predictors"])
        plt.grid(False)
        plt.tight_layout()
        plt.show()

    elif type == "predictors":
        ascending = (metric != "adjr2")
        top_models = results_df.sort_values(by=col, ascending=ascending).head(top_n)
        all_features = sorted({feat for feats in results_df[feature_col] for feat in feats})

        data = []
        metric_vals = []

        for _, row in top_models.iterrows():
            feats = row[feature_col]
            metric_val = row[col]
            row_data = [1 if f in feats else 0 for f in all_features]
            data.append(row_data)
            metric_vals.append(f"{metric_val:.3f}")

        heatmap_df = pd.DataFrame(data, index=metric_vals, columns=all_features)
        plt.figure(figsize=(10, len(metric_vals) * 0.5 + 1))
        sns.heatmap(heatmap_df, cmap="Greens", annot=True, fmt="d",
                    linewidths=0.5, linecolor="gray", cbar=False)
        plt.title(f"Top {top_n} Models by {col}")
        plt.xlabel("Predictors")
        plt.ylabel(col)
        plt.tight_layout()
        plt.show()

    else:
        raise ValueError("Invalid type. Choose from: 'line', 'bar', or 'predictors'.")
