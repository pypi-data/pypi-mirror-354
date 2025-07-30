# errorex/suggester.py

def suggest_fixes(exc_value: str, local_vars: list) -> list:
    suggestions = []

    # NaN in y (common ML error)
    if "contains NaN" in exc_value or "Input y contains NaN" in exc_value:
        suggestions.append("It looks like your data contains missing values. Try using `df.dropna()` or checking with `df.isnull().sum()`.")

    # Shape mismatch
    if "inconsistent numbers of samples" in exc_value or "shape mismatch" in exc_value:
        suggestions.append("Check if `X.shape` and `y.shape` match. Make sure you haven't dropped rows from one and not the other.")

    # KeyError
    if "KeyError" in exc_value:
        suggestions.append("You might be accessing a column or key that doesn't exist. Use `.columns` or `.keys()` to inspect available options.")

    # Division by zero
    if "division by zero" in exc_value:
        suggestions.append("You're dividing by zero. Add checks before division to avoid crashing.")

    # Custom: if DataFrame or Series has NaNs
    for var in local_vars:
        if "DataFrame" in var["type"] or "Series" in var["type"]:
            if "NaN" in var["value"]:
                suggestions.append(f"`{var['name']}` may contain NaNs. Try cleaning it before use.")

    return suggestions
