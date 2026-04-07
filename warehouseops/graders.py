import pandas as pd


def grade_output(output, expected):
    """Programmatic grader to compare SQL results with partial credit."""
    if output is None or not isinstance(output, pd.DataFrame):
        return 0.0

    try:
        # Standardize column names (lowercase) and types for comparison
        output.columns = [str(c).lower() for c in output.columns]
        expected.columns = [str(c).lower() for c in expected.columns]

        # Check for exact equality first
        if output.equals(expected):
            return 1.0

        score = 0.0
        # Partial Credit 1: Correct columns
        if set(output.columns) == set(expected.columns):
            score += 0.3

        # Partial Credit 2: Correct row count
        if len(output) == len(expected):
            score += 0.2

        # Partial Credit 3: First row/value match (basic logic check)
        if (
            len(output) > 0
            and len(expected) > 0
            and output.iloc[0, 0] == expected.iloc[0, 0]
        ):
            score += 0.2

        # If dataframes have same shape but different values
        if output.shape == expected.shape:
            score += 0.1

        return min(score, 0.9)  # Cap partial rewards below 1.0

    except Exception:
        return 0.0
