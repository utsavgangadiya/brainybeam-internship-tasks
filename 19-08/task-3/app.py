import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Manual Categorical Encoding",
    layout="wide"
)

st.title("Categorical Data - Manual Encoding")

# --------------------------------------------------
# Upload dataset
# --------------------------------------------------

file = st.file_uploader(
    "Upload Dataset",
    type=["csv"]
)

if file:

    df = pd.read_csv(file)

    st.subheader("Original Dataset")
    st.dataframe(df, use_container_width=True)

    # --------------------------------------------------
    # Find categorical columns automatically
    # --------------------------------------------------

    categorical_columns = []

    for column in df.columns:

        # Text/object columns
        if df[column].dtype == "object":
            categorical_columns.append(column)

    # Add known categorical columns if they are numeric
    known_categorical = [
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "ca",
        "thal"
    ]

    for column in known_categorical:

        if column in df.columns and column not in categorical_columns:
            categorical_columns.append(column)

    st.subheader("Categorical Columns")

    if len(categorical_columns) == 0:

        st.warning("No categorical columns found.")

        st.stop()

    st.write(categorical_columns)

    # --------------------------------------------------
    # Manual encoding
    # --------------------------------------------------

    mappings = {}
    encoded_df = df.copy()

    for column in categorical_columns:

        mapping = {}
        next_number = 0

        # Create mapping from existing categories
        for value in df[column]:

            # Handle missing values
            if pd.isna(value):
                value = "Unknown"

            value = str(value)

            if value not in mapping:
                mapping[value] = next_number
                next_number += 1

        mappings[column] = mapping

        # Encode dataset
        encoded_values = []

        for value in df[column]:

            if pd.isna(value):
                value = "Unknown"

            value = str(value)

            if value in mapping:
                encoded_values.append(mapping[value])
            else:
                # Unknown value
                encoded_values.append(-1)

        encoded_df[column] = encoded_values

    # --------------------------------------------------
    # Show mappings
    # --------------------------------------------------

    st.subheader("Category Mappings")

    for column in mappings:

        st.write(f"### {column}")

        mapping = mappings[column]

        for category, number in mapping.items():

            st.write(
                f"**{category}** → `{number}`"
            )

    # --------------------------------------------------
    # Test unknown category
    # --------------------------------------------------

    st.subheader("Test Unknown Category")

    selected_column = st.selectbox(
        "Select categorical column",
        categorical_columns
    )

    new_category = st.text_input(
        "Enter a new category",
        placeholder="Example: Very High"
    )

    if st.button("Encode New Category"):

        if new_category.strip() == "":

            st.warning(
                "Please enter a category."
            )

        else:

            new_category = new_category.strip()

            mapping = mappings[selected_column]

            # Existing category
            if new_category in mapping:

                encoded_value = mapping[new_category]

                st.info(
                    f"'{new_category}' already exists."
                )

                st.success(
                    f"Encoded value: {encoded_value}"
                )

            # Unknown category
            else:

                encoded_value = len(mapping)

                # Add new category dynamically
                mapping[new_category] = encoded_value

                st.warning(
                    f"Unknown category detected: "
                    f"'{new_category}'"
                )

                st.success(
                    f"New mapping created: "
                    f"'{new_category}' → {encoded_value}"
                )

                # Update mapping
                mappings[selected_column] = mapping

    # --------------------------------------------------
    # Encoded dataset
    # --------------------------------------------------

    st.subheader("Encoded Dataset")

    st.dataframe(
        encoded_df,
        use_container_width=True
    )

    # --------------------------------------------------
    # Download
    # --------------------------------------------------

    csv_data = encoded_df.to_csv(index=False)

    st.download_button(
        "Download Encoded Dataset",
        csv_data,
        "encoded_dataset.csv",
        "text/csv"
    )