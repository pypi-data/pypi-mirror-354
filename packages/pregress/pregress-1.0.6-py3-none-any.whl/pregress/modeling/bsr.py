import numpy as np
import pandas as pd
import statsmodels.api as sm
from itertools import combinations
from .parse_formula import parse_formula  # Ensure correct import based on your setup

def bsr(formula, data, max_var=8, metric="aic"):
    """
    Perform Best Subset Regression based on the given formula, data, and parameters.

    Parameters:
    formula (str): A string representing the regression formula (e.g., "y ~ x1 + x2 + x3").
    data (pd.DataFrame): A pandas DataFrame containing the data.
    max_var (int): The maximum number of predictor variables to consider in subsets.
    metric (str): The metric used to select the best model. Options are: 'adjr2', 'aic', 'bic', 'rmse'.

    Returns:
    statsmodels OLSResults object with additional attributes:
        - best_features: list of predictors in the best model
        - best_by_k: dict mapping number of predictors to best feature list of that size
        - bsr_results: full sorted results DataFrame of all subset models
    """
    
    # Parse the formula to get initial predictors and response
    y_var, x_vars, y, X = parse_formula(formula + "+0", data)
    
    def get_subsets(X, max_size):
        subsets = []
        for size in range(1, max_size + 1):
            for subset in combinations(X.columns, size):
                subsets.append(subset)
        return subsets
    
    def fit_linear_regression(X, y, features):
        # Subset the predictors and add a constant term
        X_subset = X[list(features)]
        X_subset = sm.add_constant(X_subset)
        
        # Fit the OLS regression model
        model = sm.OLS(y, X_subset).fit()
        
        # Calculate the desired metrics
        adj_r2 = model.rsquared_adj
        aic = model.aic
        bic = model.bic
        n = len(y)
        p = len(features) + 1
        mse = np.sum(model.resid ** 2) / (n - p)
        rmse = np.sqrt(mse)
        
        return adj_r2, aic, bic, rmse
    
    # Generate all possible subsets of features up to max_var size
    subsets = get_subsets(X, max_size=max_var)
    
    # Fit linear regression models to each subset of features and record metrics
    results = []
    for subset in subsets:
        adj_r2, aic, bic, rmse = fit_linear_regression(X, y, subset)
        results.append((subset, adj_r2, aic, bic, rmse))
    
    # Convert results to a pandas DataFrame
    results_df = pd.DataFrame(results, columns=['Features', 'Adj. R-squared', 'AIC', 'BIC', 'RMSE'])
    
    # Define a dictionary to map metric to DataFrame columns
    metric_column = {
        "adjr2": "Adj. R-squared",
        "aic": "AIC",
        "bic": "BIC",
        "rmse": "RMSE"
    }
    
    # Raise an error if an invalid metric is provided
    if metric not in metric_column:
        raise ValueError("Invalid metric. Must be one of 'adjr2', 'aic', 'bic', 'rmse'.")
    
    # Sort results by the specified metric
    results_df = results_df.sort_values(by=metric_column[metric], ascending=(metric != "adjr2"))
    
    # Fit best model
    best_row = results_df.iloc[0]
    best_features = list(best_row['Features'])
    X_best = X[best_features].copy()
    X_best['Intercept'] = 1
    cols = ['Intercept'] + [col for col in X_best.columns if col != 'Intercept']
    X_best = X_best[cols]
    
    best_model = sm.OLS(y, X_best).fit()

    # Create best_by_k dictionary
    best_by_k = (
        results_df
        .assign(k=results_df['Features'].apply(len))
        .sort_values(by=metric_column[metric], ascending=(metric != "adjr2"))
        .drop_duplicates(subset='k')
        .set_index('k')['Features']
        .apply(list)
        .to_dict()
    )

    # Attach attributes to the best model
    best_model.best_features = best_features
    best_model.best_by_k = best_by_k
    best_model.bsr_results = results_df
    best_model.bsr_metric = metric

    return best_model
