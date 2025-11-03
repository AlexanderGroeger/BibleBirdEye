import random
from pandas import DataFrame

def sample_less_likely(df: DataFrame):
    """
    Sample a row from the DataFrame, giving preference to rows with lower 'attempts' and 'correct' counts.
    """
    # Calculate weights based on attempts and correct counts
    max_attempts = df['attempts'].max() if not df['attempts'].empty else 1
    max_correct = df['correct'].max() if not df['correct'].empty else 1

    def weight(row):
        attempt_factor = (max_attempts - row['attempts'] + 1)
        correct_factor = (max_correct - row['correct'] + 1)
        return attempt_factor * correct_factor

    weights = df.apply(weight, axis=1)
    total_weight = weights.sum()
    probabilities = weights / total_weight if total_weight > 0 else [1/len(df)] * len(df)

    return df.sample(n=1, weights=probabilities).iloc[0].index
    