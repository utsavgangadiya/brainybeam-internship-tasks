import streamlit as st
import pandas as pd

st.title("Heart Disease - Missing Value Handling")

# Upload dataset
file = st.file_uploader("Upload Heart Disease CSV", type=["csv"])

if file:

    df = pd.read_csv(file)

    st.subheader("Original Dataset")
    st.dataframe(df)

    # Identify missing values WITHOUT isna() / dropna()

    missing_count = {}

    for column in df.columns:

        count = 0

        for value in df[column]:

            # Check for NaN manually
            if value != value:
                count += 1

            # Check empty strings
            elif isinstance(value, str) and value.strip() == "":
                count += 1

        missing_count[column] = count

    st.subheader("Missing Values")

    for column in missing_count:
        st.write(column, ":", missing_count[column])

    # Create copies for different techniques

    mean_df = df.copy()
    median_df = df.copy()
    mode_df = df.copy()

    # Mean Imputation

    for column in mean_df.columns:

        if pd.api.types.is_numeric_dtype(mean_df[column]):

            values = []

            for value in mean_df[column]:

                if value == value:
                    values.append(value)

            if len(values) > 0:

                total = 0

                for value in values:
                    total += value

                mean_value = total / len(values)

                for i in range(len(mean_df[column])):

                    value = mean_df[column].iloc[i]

                    if value != value:
                        mean_df.iloc[i, mean_df.columns.get_loc(column)] = mean_value

    # Median Imputation

    for column in median_df.columns:

        if pd.api.types.is_numeric_dtype(median_df[column]):

            values = []

            for value in median_df[column]:

                if value == value:
                    values.append(value)

            if len(values) > 0:

                # Manual sorting
                for i in range(len(values)):

                    for j in range(i + 1, len(values)):

                        if values[i] > values[j]:
                            values[i], values[j] = values[j], values[i]

                n = len(values)

                if n % 2 == 1:
                    median_value = values[n // 2]

                else:
                    median_value = (
                        values[(n // 2) - 1] +
                        values[n // 2]
                    ) / 2

                for i in range(len(median_df[column])):

                    value = median_df[column].iloc[i]

                    if value != value:
                        median_df.iloc[
                            i,
                            median_df.columns.get_loc(column)
                        ] = median_value

    # Mode Imputation

    for column in mode_df.columns:

        frequency = {}

        for value in mode_df[column]:

            if value == value and value != "":
                if value in frequency:
                    frequency[value] += 1
                else:
                    frequency[value] = 1

        if len(frequency) > 0:

            mode_value = list(frequency.keys())[0]

            for value in frequency:

                if frequency[value] > frequency[mode_value]:
                    mode_value = value

            for i in range(len(mode_df[column])):

                value = mode_df[column].iloc[i]

                if value != value or (
                    isinstance(value, str)
                    and value.strip() == ""
                ):

                    mode_df.iloc[
                        i,
                        mode_df.columns.get_loc(column)
                    ] = mode_value

    # Compare results

    st.subheader("Imputation Techniques")

    st.write("### 1. Mean Imputation")
    st.write(
        "Missing numerical values are replaced with the average "
        "of the available values."
    )

    st.write("### 2. Median Imputation")
    st.write(
        "Missing numerical values are replaced with the middle "
        "value after sorting the available values."
    )

    st.write("### 3. Mode Imputation")
    st.write(
        "Missing values are replaced with the most frequently "
        "occurring value."
    )

    # Select result

    method = st.selectbox(
        "Select Imputation Method",
        [
            "Mean",
            "Median",
            "Mode"
        ]
    )

    if method == "Mean":
        result = mean_df

    elif method == "Median":
        result = median_df

    else:
        result = mode_df

    st.subheader("Imputed Dataset")

    st.dataframe(result)

    # Missing values after imputation

    st.subheader("Missing Values After Imputation")

    remaining_missing = {}

    for column in result.columns:

        count = 0

        for value in result[column]:

            if value != value:
                count += 1

            elif isinstance(value, str) and value.strip() == "":
                count += 1

        remaining_missing[column] = count

    for column in remaining_missing:
        st.write(column, ":", remaining_missing[column])