import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Heart Disease - Manual One-Hot Encoding",
    layout="wide"
)

st.title("Heart Disease - Manual One-Hot Encoding")
# Upload datase

file = st.file_uploader(
    "Upload Heart Disease Dataset",
    type=["csv"]
)

if file:

    df = pd.read_csv(file)

    st.subheader("Original Dataset")
    st.dataframe(df, use_container_width=True)

    # Identify categorical columns

    possible_categorical = [
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "ca",
        "thal"
    ]

    categorical_columns = []

    for column in possible_categorical:

        if column in df.columns:
            categorical_columns.append(column)

    # Check categorical columns

    if len(categorical_columns) == 0:

        st.error("No categorical columns found.")

        st.write("Available columns:")
        st.write(list(df.columns))

        st.stop()

    st.success(
        "Categorical columns detected successfully."
    )

    st.write(
        "Categorical Columns:",
        categorical_columns
    )

    # Manual One-Hot Encoding Function

    def manual_one_hot_encode(data, columns):

        result = data.copy()

        mappings = {}

        for column in columns:

            categories = []

            # Find categories manually
            for value in data[column]:

                if pd.isna(value):
                    value = "Unknown"

                value = str(value)

                if value not in categories:
                    categories.append(value)

            mappings[column] = categories

            # Create one-hot columns

            for category in categories:

                safe_category = (
                    category
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("/", "_")
                )

                new_column = (
                    column + "_" + safe_category
                )

                encoded_values = []

                for value in data[column]:

                    if pd.isna(value):
                        value = "Unknown"

                    value = str(value)

                    if value == category:
                        encoded_values.append(1)
                    else:
                        encoded_values.append(0)

                result[new_column] = encoded_values

            # Remove original categorical column
            result.drop(
                column,
                axis=1,
                inplace=True
            )

        return result, mappings

    # Perform Manual Encoding

    encoded_df, mappings = manual_one_hot_encode(
        df,
        categorical_columns
    )

    # Display mappings

    st.subheader("Manual One-Hot Encoding Mapping")

    for column in mappings:

        st.write(f"### {column}")

        for category in mappings[column]:

            safe_category = (
                category
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
            )

            st.write(
                f"{category} → "
                f"`{column}_{safe_category}`"
            )

    # Show encoded dataset

    st.subheader("Encoded Dataset")

    st.dataframe(
        encoded_df,
        use_container_width=True
    )

    # Test unseen category

    st.subheader("Test Unseen Category")

    test_column = st.selectbox(
        "Select categorical column",
        categorical_columns
    )

    test_value = st.text_input(
        "Enter a category to test",
        placeholder="Example: Unknown Type"
    )

    if st.button("Encode Test Category"):

        if test_value.strip() == "":

            st.warning(
                "Please enter a category."
            )

        else:

            test_value = test_value.strip()

            known_categories = mappings[test_column]

            # Existing category
            if test_value in known_categories:

                st.success(
                    f"'{test_value}' already exists."
                )

                safe_category = (
                    test_value
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("/", "_")
                )

                st.write(
                    "One-hot column:"
                )

                st.code(
                    f"{test_column}_{safe_category}"
                )

                st.write(
                    "Encoded value: 1"
                )

            # New unseen category
            else:

                st.warning(
                    f"Unseen category detected: "
                    f"'{test_value}'"
                )

                # Add new category
                known_categories.append(test_value)

                mappings[test_column] = known_categories

                safe_category = (
                    test_value
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("/", "_")
                )

                new_column = (
                    test_column + "_" + safe_category
                )

                st.success(
                    "New category handled successfully!"
                )

                st.write(
                    f"New one-hot column: "
                    f"`{new_column}`"
                )

                st.write(
                    "Encoded value for this category: 1"
                )

                st.info(
                    "Other categories would receive 0 "
                    "for this new one-hot column."
                )

    # Download encoded dataset

    csv_data = encoded_df.to_csv(index=False)

    st.download_button(
        label="Download Encoded Dataset",
        data=csv_data,
        file_name="heart_disease_one_hot_encoded.csv",
        mime="text/csv"
    )