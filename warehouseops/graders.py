import pandas as pd


def grade_output(output, expected):
    """Programmatic grader to compare SQL results with partial credit."""
    if output is None or not isinstance(output, pd.DataFrame):
        return 0.01  # Minimum score strictly > 0

    try:
        # Standardize column names (lowercase) and types for comparison
        output.columns = [str(c).lower() for c in output.columns]
        expected.columns = [str(c).lower() for c in expected.columns]

        # Check for exact equality first
        if output.equals(expected):
            return 0.99  # Maximum score strictly < 1

        score = 0.01
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

        # Return score clamped between 0.01 and 0.95
        return min(max(score, 0.01), 0.95)

    except Exception:
        return 0.01
