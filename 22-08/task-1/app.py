import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

# Load datase

dataset_path = Path(__file__).resolve().parents[2] / "heart_disease_categorical.csv"
df = pd.read_csv(dataset_path)

# Categorical column

categorical_columns = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal"
]

# Manual frequency calculatio

def calculate_frequency(values):

    categories = []
    frequencies = []

    for value in values:

        if pd.isna(value):
            value = "Unknown"

        value = str(value)

        # Check whether category already exists
        found = False

        for i in range(len(categories)):

            if categories[i] == value:

                frequencies[i] += 1
                found = True
                break

        # New category
        if not found:

            categories.append(value)
            frequencies.append(1)

    return categories, frequencies

# Create bar plot for each categorical colum

for column in categorical_columns:

    # Make sure column exists
    if column not in df.columns:
        continue

    values = []

    for value in df[column]:
        values.append(value)

    # Manual frequency calculation
    categories, frequencies = calculate_frequency(
        values
    )

    # Dynamic bar width

    number_of_categories = len(categories)

    if number_of_categories <= 3:
        bar_width = 0.65

    elif number_of_categories <= 5:
        bar_width = 0.55

    else:
        bar_width = 0.45

    # Dynamic colors

    colors = []

    for i in range(number_of_categories):

        if i % 3 == 0:
            colors.append("steelblue")

        elif i % 3 == 1:
            colors.append("orange")

        else:
            colors.append("seagreen")

    # Create positions

    positions = []

    for i in range(number_of_categories):
        positions.append(i)

    # Create plot

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    bars = ax.bar(
        positions,
        frequencies,
        width=bar_width,
        color=colors,
        edgecolor="black"
    )

    # Add frequency labels

    for i in range(len(bars)):

        height = frequencies[i]

        ax.text(
            bars[i].get_x()
            + bars[i].get_width() / 2,
            height + 0.5,
            str(height),
            ha="center",
            fontweight="bold"
        )

    # Formatting

    ax.set_title(
        "Distribution of " + column,
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    ax.set_xticks(positions)
    ax.set_xticklabels(
        categories,
        rotation=30,
        ha="right"
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()