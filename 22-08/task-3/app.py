import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

# Load datase

dataset_path = Path(__file__).resolve().parents[2] / "heart_disease_with_risk_factor.csv"
df = pd.read_csv(dataset_path)



# Numerical columns

numerical_columns = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]


# Manual Mean

def manual_mean(values):

    total = 0

    for value in values:
        total += value

    return total / len(values)


# Manual Correlation

def manual_correlation(x, y):

    mean_x = manual_mean(x)
    mean_y = manual_mean(y)

    numerator = 0
    sum_x = 0
    sum_y = 0

    for i in range(len(x)):

        dx = x[i] - mean_x
        dy = y[i] - mean_y

        numerator += dx * dy
        sum_x += dx * dx
        sum_y += dy * dy

    denominator = (sum_x * sum_y) ** 0.5

    if denominator == 0:
        return 0

    return numerator / denominator


# Manual Trendline

def calculate_trendline(x, y):

    mean_x = manual_mean(x)
    mean_y = manual_mean(y)

    numerator = 0
    denominator = 0

    for i in range(len(x)):

        numerator += (
            (x[i] - mean_x)
            *
            (y[i] - mean_y)
        )

        denominator += (
            (x[i] - mean_x) ** 2
        )

    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator

    intercept = mean_y - (
        slope * mean_x
    )

    return slope, intercept


# Calculate all correlations

correlations = []

for i in range(len(numerical_columns)):

    for j in range(i + 1, len(numerical_columns)):

        column_x = numerical_columns[i]
        column_y = numerical_columns[j]

        x_values = []
        y_values = []

        for k in range(len(df)):

            x = df[column_x].iloc[k]
            y = df[column_y].iloc[k]

            if x == x and y == y:

                x_values.append(float(x))
                y_values.append(float(y))

        if len(x_values) > 1:

            correlation = manual_correlation(
                x_values,
                y_values
            )

            correlations.append({
                "x": column_x,
                "y": column_y,
                "correlation": correlation
            })


# Display correlations

print("\nCorrelation Results")
print("=" * 60)

for item in correlations:

    print(
        item["x"],
        "vs",
        item["y"],
        "=",
        round(item["correlation"], 3)
    )


# Select correlated pairs

threshold = 0.20

selected_pairs = []

for item in correlations:

    if abs(item["correlation"]) >= threshold:

        selected_pairs.append(item)


# If no pair reaches threshold,
# select the strongest pairs

if len(selected_pairs) == 0:

    print(
        "\nNo pair reached the threshold."
    )

    print(
        "Selecting strongest correlated pairs instead."
    )

    # Manual sorting by absolute correlation
    correlations.sort(
        key=lambda item: abs(
            item["correlation"]
        ),
        reverse=True
    )

    selected_pairs = correlations[:3]


print("\nPairs selected for plotting")
print("=" * 60)

for item in selected_pairs:

    print(
        item["x"],
        "vs",
        item["y"],
        "=",
        round(item["correlation"], 3)
    )


# Plot selected pairs

for item in selected_pairs:

    column_x = item["x"]
    column_y = item["y"]
    correlation = item["correlation"]

    x_values = []
    y_values = []

    for i in range(len(df)):

        x = df[column_x].iloc[i]
        y = df[column_y].iloc[i]

        if x == x and y == y:

            x_values.append(float(x))
            y_values.append(float(y))

    # Calculate trendline

    slope, intercept = calculate_trendline(
        x_values,
        y_values
    )

    # Find minimum and maximum manually

    x_min = x_values[0]
    x_max = x_values[0]

    for value in x_values:

        if value < x_min:
            x_min = value

        if value > x_max:
            x_max = value

    # Trendline values

    trend_x = [
        x_min,
        x_max
    ]

    trend_y = [
        slope * x_min + intercept,
        slope * x_max + intercept
    ]

    # Create chart

    fig, ax = plt.subplots(
        figsize=(9, 6)
    )

    # Data points
    ax.plot(
        x_values,
        y_values,
        linestyle="",
        marker="o",
        markersize=5,
        alpha=0.6,
        label="Data Points"
    )

    # Trendline
    ax.plot(
        trend_x,
        trend_y,
        linewidth=2,
        label="Trendline"
    )

    # Labels

    ax.set_title(
        f"{column_x} vs {column_y}",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel(column_x)
    ax.set_ylabel(column_y)

    ax.text(
        0.05,
        0.95,
        f"Correlation = {correlation:.3f}",
        transform=ax.transAxes,
        verticalalignment="top"
    )

    ax.grid(
        linestyle="--",
        alpha=0.3
    )

    ax.legend()

    plt.tight_layout()

    plt.show()