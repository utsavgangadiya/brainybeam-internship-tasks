import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Heart Disease - Numerical Data Distribution")

file = st.file_uploader(
    "Upload Heart Disease CSV",
    type=["csv"]
)

if file:

    df = pd.read_csv(file)

    st.subheader("Dataset")
    st.dataframe(df)

    # Find numerical columns

    numerical_columns = []

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):
            numerical_columns.append(column)

    st.write("Numerical Columns:", numerical_columns)

    # Individual distributions

    st.subheader("Individual Distributions")

    for column in numerical_columns:

        values = []

        for value in df[column]:
            if value == value:
                values.append(value)

        if len(values) == 0:
            continue

        # Manual mean
        total = 0

        for value in values:
            total += value

        mean = total / len(values)

        # Manual sorting for median
        sorted_values = values.copy()

        for i in range(len(sorted_values)):
            for j in range(i + 1, len(sorted_values)):

                if sorted_values[i] > sorted_values[j]:
                    sorted_values[i], sorted_values[j] = (
                        sorted_values[j],
                        sorted_values[i]
                    )

        n = len(sorted_values)

        if n % 2 == 1:
            median = sorted_values[n // 2]
        else:
            median = (
                sorted_values[n // 2 - 1] +
                sorted_values[n // 2]
            ) / 2

        # Plot

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.hist(
            values,
            bins=15,
            edgecolor="black",
            alpha=0.75
        )

        ax.axvline(
            mean,
            linestyle="--",
            linewidth=2,
            label=f"Mean: {mean:.2f}"
        )

        ax.axvline(
            median,
            linestyle=":",
            linewidth=2,
            label=f"Median: {median:.2f}"
        )

        ax.set_title(
            f"Distribution of {column}",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )

        ax.legend()

        st.pyplot(fig)

        plt.close(fig)

    # Comparative plots

    st.subheader("Comparative Distribution")

    selected_columns = st.multiselect(
        "Select columns to compare",
        numerical_columns,
        default=numerical_columns[:4]
    )

    if len(selected_columns) > 0:

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        for column in selected_columns:

            values = []

            for value in df[column]:

                if value == value:
                    values.append(value)

            if len(values) > 0:

                ax.hist(
                    values,
                    bins=15,
                    alpha=0.45,
                    label=column
                )

        ax.set_title(
            "Comparison of Numerical Distributions",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )

        ax.legend()

        st.pyplot(fig)

        plt.close(fig)
