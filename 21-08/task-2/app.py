from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# Load dataset

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


# Manual Histogram Function

def create_manual_histogram(values, column_name, number_of_bins=10):

    # Remove missing values manually
    clean_values = []

    for value in values:

        if value == value:
            clean_values.append(float(value))

    if len(clean_values) == 0:
        return

    # Find minimum and maximum

    minimum = clean_values[0]
    maximum = clean_values[0]

    for value in clean_values:

        if value < minimum:
            minimum = value

        if value > maximum:
            maximum = value

    # Calculate bin width

    if maximum == minimum:
        bin_width = 1
    else:
        bin_width = (
            maximum - minimum
        ) / number_of_bins

    # Create frequency list

    frequencies = []

    for i in range(number_of_bins):
        frequencies.append(0)

    # Manually assign values to bins

    for value in clean_values:

        if maximum == minimum:

            bin_index = 0

        else:

            bin_index = int(
                (value - minimum) / bin_width
            )

            # Include maximum value
            if bin_index >= number_of_bins:
                bin_index = number_of_bins - 1

        frequencies[bin_index] += 1

    # Create bin positions

    bin_edges = []

    for i in range(number_of_bins + 1):

        edge = minimum + (
            i * bin_width
        )

        bin_edges.append(edge)

    # Create figure

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    # Draw histogram bars manually

    for i in range(number_of_bins):

        left = bin_edges[i]

        height = frequencies[i]

        rectangle = Rectangle(
            (left, 0),
            bin_width,
            height,
            fill=True,
            edgecolor="black",
            alpha=0.75
        )

        ax.add_patch(rectangle)

    # Set limits
    ax.set_xlim(
        minimum - bin_width * 0.05,
        maximum + bin_width * 0.05
    )

    # Find highest frequency
    highest_frequency = 0

    for frequency in frequencies:

        if frequency > highest_frequency:
            highest_frequency = frequency

    ax.set_ylim(
        0,
        highest_frequency + 2
    )

    # Labels and title

    ax.set_title(
        "Manual Histogram - " + column_name,
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel(column_name)
    ax.set_ylabel("Frequency")

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    # Add frequency annotations

    for i in range(number_of_bins):

        if frequencies[i] > 0:

            center = (
                bin_edges[i]
                + bin_width / 2
            )

            ax.text(
                center,
                frequencies[i] + 0.2,
                str(frequencies[i]),
                ha="center",
                fontsize=9
            )

    plt.tight_layout()

    plt.show()


# Create histogram for every numerical feature

for column in numerical_columns:

    values = []

    for value in df[column]:

        if value == value:
            values.append(value)

    create_manual_histogram(
        values,
        column,
        number_of_bins=10
    )