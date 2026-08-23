import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from pathlib import Path

# Load datase

dataset_path = Path(__file__).resolve().parents[2] / "heart_disease_missing_values.csv"
df = pd.read_csv(dataset_path)

# Check missing values manuall

missing_grid = []

total_missing = 0

for i in range(len(df)):

    row = []

    for column in df.columns:

        value = df[column].iloc[i]

        # Check missing value manually
        if pd.isna(value):
            row.append(1)
            total_missing += 1

        else:
            row.append(0)

    missing_grid.append(row)

# Display missing-value informatio

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))
print("Total Missing Values:", total_missing)

# If no missing value

if total_missing == 0:

    print("\nNo missing values found.")
    print("Heatmap is not required.")

else:

    # Create manual grid

    fig, ax = plt.subplots(
        figsize=(14, 8)
    )

    rows = len(df)
    columns = len(df.columns)

    # Draw every grid cell manually

    for i in range(rows):

        for j in range(columns):

            value = missing_grid[i][j]

            # ------------------------------------------
            # Custom color gradient
            # ------------------------------------------

            if value == 1:

                # Missing value
                face_color = "red"

            else:

                # Existing value
                face_color = "white"

            rectangle = Rectangle(
                (j, rows - i - 1),
                1,
                1,
                facecolor=face_color,
                edgecolor="lightgray",
                linewidth=0.5
            )

            ax.add_patch(rectangle)

    # Axis configuration

    ax.set_xlim(
        0,
        columns
    )

    ax.set_ylim(
        0,
        rows
    )

    # Column names
    ax.set_xticks(
        [i + 0.5 for i in range(columns)]
    )

    ax.set_xticklabels(
        df.columns,
        rotation=45,
        ha="right"
    )

    # Row numbers
    ax.set_yticks(
        [i + 0.5 for i in range(rows)]
    )

    ax.set_yticklabels(
        range(rows - 1, -1, -1)
    )

    # Title

    ax.set_title(
        "Manual Missing Values Heatmap",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "Dataset Columns"
    )

    ax.set_ylabel(
        "Dataset Rows"
    )

    # Legend

    normal_box = Rectangle(
        (0, 0),
        1,
        1,
        facecolor="white",
        edgecolor="black"
    )

    missing_box = Rectangle(
        (0, 0),
        1,
        1,
        facecolor="red",
        edgecolor="black"
    )

    ax.legend(
        [normal_box, missing_box],
        [
            "Available Value",
            "Missing Value"
        ],
        loc="upper right"
    )

    plt.tight_layout()

    plt.show()