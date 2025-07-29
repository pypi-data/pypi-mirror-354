import statsmodels.api as sm
from .parse_formula import parse_formula
from .fit import fit

def step(formula, data, direction='backward', criterion='aic', threshold_in=0.05, threshold_out=0.10, max_steps=100, verbose=False):
    """
    Perform stepwise model selection based on a specified criterion.

    Parameters:
    ----------
    formula : str
        A regression formula of the form 'Y ~ X1 + X2 + ...'.
    data : pandas.DataFrame
        The dataset containing the variables in the formula.
    direction : {'forward', 'backward', 'both'}, default='backward'
        Direction of selection:
        - 'forward': starts with the intercept only and adds variables.
        - 'backward': starts with all variables and removes variables.
        - 'both': combination of forward and backward steps.
    criterion : {'aic', 'bic', 'adjr2', 'pvalue'}, default='aic'
        The metric used to evaluate model performance at each step.
        - 'aic': Akaike Information Criterion.
        - 'bic': Bayesian Information Criterion.
        - 'adjr2': Adjusted R-squared.
        - 'pvalue': Highest p-value among predictors (excluding intercept).
    threshold_in : float, default=0.05
        (Currently unused) Intended threshold for including a variable based on p-value.
    threshold_out : float, default=0.10
        (Currently unused) Intended threshold for removing a variable based on p-value.
    max_steps : int, default=100
        Maximum number of steps to take before stopping.
    verbose : bool, default=False
        If True, prints progress messages showing each step taken.

    Returns:
    -------
    model : statsmodels object
        The final selected model, with additional attributes accessible through standard statsmodels API.
    """

    def get_score(model):
        if criterion == 'aic':
            return model.aic
        elif criterion == 'bic':
            return model.bic
        elif criterion == 'adjr2':
            return 1 - (1 - model.rsquared) * (model.nobs - 1) / (model.nobs - model.df_model - 1)
        elif criterion == 'pvalue':
            return model.pvalues.drop("Intercept", errors="ignore").max()
        else:
            raise ValueError("Invalid criterion")

    # Parse to get variable names and transformed data
    Y_name, X_names, Y_out, X_out = parse_formula(formula, data)

    label = criterion.upper()

    # Correct initialization of selected and remaining variables
    if direction in ['forward', 'both']:
        selected = ['Intercept'] if 'Intercept' in X_out.columns else []
        remaining = [v for v in X_out.columns if v != 'Intercept']
    else:  # backward only
        selected = X_names.copy()
        remaining = list(set(X_out.columns) - set(selected))

    # Builds model from selected variables
    def model_from_vars(vars):
        if not vars or vars == ['Intercept']:
            term = f"{Y_name} ~ 1"
        else:
            term = f"{Y_name} ~ {' + '.join([v for v in vars if v != 'Intercept'])}"
            if 'Intercept' not in vars:
                term += ' -1'
        return fit(term, data)

    best_model = model_from_vars(selected)
    current_score = get_score(best_model)

    if verbose:
        print(f"Initial {label} = {current_score:.4f}")

    step_count = 0
    while step_count < max_steps:
        step_count += 1
        changed = False

        # Forward step
        if direction in ['forward', 'both']:
            scores = []
            for var in remaining:
                trial_vars = selected + [var]
                try:
                    model = model_from_vars(trial_vars)
                    score = get_score(model)
                    scores.append((score, var, model))
                except:
                    continue
            if scores:
                best = min(scores, key=lambda x: x[0]) if criterion in ['aic', 'bic', 'pvalue'] else max(scores, key=lambda x: x[0])
                if (criterion in ['aic', 'bic', 'pvalue'] and best[0] < current_score) or \
                   (criterion == 'adjr2' and best[0] > current_score):
                    selected.append(best[1])
                    remaining.remove(best[1])
                    best_model = best[2]
                    current_score = best[0]
                    changed = True
                    if verbose:
                        print(f"Step {step_count}: add {best[1]} ({label}={current_score:.4f})")

        # Backward step
        if direction in ['backward', 'both'] and [v for v in selected if v != 'Intercept']:
            scores = []
            for var in [v for v in selected if v != 'Intercept']:
                trial_vars = [v for v in selected if v != var]
                model = model_from_vars(trial_vars)
                score = get_score(model)
                scores.append((score, var, model))
            if scores:
                best = min(scores, key=lambda x: x[0]) if criterion in ['aic', 'bic', 'pvalue'] else max(scores, key=lambda x: x[0])
                if (criterion in ['aic', 'bic', 'pvalue'] and best[0] < current_score) or \
                   (criterion == 'adjr2' and best[0] > current_score):
                    selected.remove(best[1])
                    remaining.append(best[1])
                    best_model = best[2]
                    current_score = best[0]
                    changed = True
                    if verbose:
                        print(f"Step {step_count}: remove {best[1]} ({label}={current_score:.4f})")

        if not changed:
            break

    return best_model
