import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

# Load datase

dataset_path = Path(__file__).resolve().parents[2] / "heart_disease_with_risk_factor.csv"
df = pd.read_csv(dataset_path)


# Numerical column

numerical_columns = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]

# Manual Media

def manual_median(values):

    values = values.copy()

    # Manual sorting
    for i in range(len(values)):

        for j in range(i + 1, len(values)):

            if values[i] > values[j]:

                values[i], values[j] = (
                    values[j],
                    values[i]
                )

    n = len(values)

    if n % 2 == 1:

        return values[n // 2]

    else:

        return (
            values[n // 2 - 1]
            + values[n // 2]
        ) / 2

# Manual Percentil

def manual_percentile(values, percentage):

    values = values.copy()

    # Manual sorting
    for i in range(len(values)):

        for j in range(i + 1, len(values)):

            if values[i] > values[j]:

                values[i], values[j] = (
                    values[j],
                    values[i]
                )

    position = (
        (len(values) - 1)
        * percentage
    )

    lower = int(position)
    upper = lower + 1

    if upper >= len(values):

        return values[lower]

    fraction = position - lower

    return (
        values[lower]
        + fraction *
        (values[upper] - values[lower])
    )

# Manual Box Plot

def create_manual_boxplot(values, column_name):

    # Remove missing values manually
    clean_values = []

    for value in values:

        if value == value:
            clean_values.append(float(value))

    if len(clean_values) == 0:
        return

    # Calculate quartiles

    q1 = manual_percentile(
        clean_values,
        0.25
    )

    median = manual_median(
        clean_values
    )

    q3 = manual_percentile(
        clean_values,
        0.75
    )

    # Calculate IQR

    iqr = q3 - q1

    # Calculate fences

    lower_fence = q1 - (
        1.5 * iqr
    )

    upper_fence = q3 + (
        1.5 * iqr
    )

    # Find whisker values

    lower_whisker = None
    upper_whisker = None

    for value in clean_values:

        if value >= lower_fence:

            if lower_whisker is None:
                lower_whisker = value

            elif value < lower_whisker:
                lower_whisker = value

        if value <= upper_fence:

            if upper_whisker is None:
                upper_whisker = value

            elif value > upper_whisker:
                upper_whisker = value

    # Find outliers

    outliers = []

    for value in clean_values:

        if (
            value < lower_fence
            or value > upper_fence
        ):

            outliers.append(value)

    # Create plot

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    center = 1

    # Draw box

    box_height = 0.4

    rectangle = Rectangle(
        (
            q1,
            center - box_height / 2
        ),
        q3 - q1,
        box_height,
        fill=True,
        edgecolor="black",
        alpha=0.6
    )

    ax.add_patch(rectangle)

    # Draw median

    ax.plot(
        [median, median],
        [
            center - box_height / 2,
            center + box_height / 2
        ],
        linewidth=3
    )

    # Draw whiskers

    ax.plot(
        [lower_whisker, q1],
        [center, center],
        linewidth=2
    )

    ax.plot(
        [q3, upper_whisker],
        [center, center],
        linewidth=2
    )

    # Draw whisker caps

    cap_height = 0.15

    ax.plot(
        [lower_whisker, lower_whisker],
        [
            center - cap_height,
            center + cap_height
        ],
        linewidth=2
    )

    ax.plot(
        [upper_whisker, upper_whisker],
        [
            center - cap_height,
            center + cap_height
        ],
        linewidth=2
    )

    # Draw outliers manually

    for outlier in outliers:

        ax.plot(
            outlier,
            center,
            marker="o",
            markersize=7
        )

    # Add annotations

    ax.text(
        q1,
        center + 0.32,
        f"Q1 = {q1:.2f}",
        ha="center"
    )

    ax.text(
        median,
        center - 0.38,
        f"Median = {median:.2f}",
        ha="center"
    )

    ax.text(
        q3,
        center + 0.32,
        f"Q3 = {q3:.2f}",
        ha="center"
    )

    ax.text(
        lower_fence,
        center - 0.55,
        f"Lower Fence = {lower_fence:.2f}",
        ha="center",
        fontsize=9
    )

    ax.text(
        upper_fence,
        center - 0.55,
        f"Upper Fence = {upper_fence:.2f}",
        ha="center",
        fontsize=9
    )

    # Plot formatting

    ax.set_title(
        f"Manual Box Plot - {column_name}",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel(column_name)

    ax.set_yticks([center])
    ax.set_yticklabels([column_name])

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    ax.set_ylim(
        0.5,
        1.5
    )

    # Display outlier information

    print("\n" + "=" * 50)

    print("Feature:", column_name)

    print("Q1:", round(q1, 2))
    print("Median:", round(median, 2))
    print("Q3:", round(q3, 2))
    print("IQR:", round(iqr, 2))

    print(
        "Lower Fence:",
        round(lower_fence, 2)
    )

    print(
        "Upper Fence:",
        round(upper_fence, 2)
    )

    print(
        "Number of Outliers:",
        len(outliers)
    )

    if len(outliers) > 0:

        print(
            "Outliers:",
            outliers
        )

    else:

        print("Outliers: None")

    plt.tight_layout()
    plt.show()

# Generate box plot for every featur

for column in numerical_columns:

    values = []

    for value in df[column]:

        if value == value:
            values.append(value)

    create_manual_boxplot(
        values,
        column
    )