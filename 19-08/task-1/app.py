import streamlit as st
import csv

st.title("Heart Disease - Duplicate Detection")

file = st.file_uploader(
    "Upload Heart Disease CSV",
    type=["csv"]
)

if file:

    # Read dataset manually

    content = file.read().decode("utf-8")
    lines = content.splitlines()

    reader = csv.reader(lines)
    rows = list(reader)

    headers = rows[0]
    data = rows[1:]

    st.subheader("Original Dataset")

    st.write("Total Rows:", len(data))
    st.write("Total Columns:", len(headers))

    # Custom duplicate comparison algorithm

    unique_rows = []
    duplicate_rows = []

    for i in range(len(data)):

        current_row = data[i]
        is_duplicate = False

        # Compare current row with previously stored rows
        for unique_row in unique_rows:

            same = True

            for j in range(len(headers)):

                if current_row[j] != unique_row[j]:
                    same = False
                    break

            if same:
                is_duplicate = True
                break

        if is_duplicate:
            duplicate_rows.append(current_row)
        else:
            unique_rows.append(current_row)

    # Results

    st.subheader("Duplicate Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Original Rows",
            len(data)
        )

    with col2:
        st.metric(
            "Duplicate Rows",
            len(duplicate_rows)
        )

    with col3:
        st.metric(
            "Unique Rows",
            len(unique_rows)
        )

    # Display duplicate rows

    if len(duplicate_rows) > 0:

        st.subheader("Duplicate Rows")

        duplicate_table = []

        for row in duplicate_rows:

            record = {}

            for i in range(len(headers)):
                record[headers[i]] = row[i]

            duplicate_table.append(record)

        st.dataframe(
            duplicate_table,
            use_container_width=True
        )

    else:

        st.success("No duplicate rows found.")

    # Remove duplicates manually

    st.subheader("Dataset After Removing Duplicates")

    cleaned_table = []

    for row in unique_rows:

        record = {}

        for i in range(len(headers)):
            record[headers[i]] = row[i]

        cleaned_table.append(record)

    st.dataframe(
        cleaned_table,
        use_container_width=True
    )

    # Impact analysis

    st.subheader("Impact on Data Integrity")

    if len(data) > 0:

        duplicate_percentage = (
            len(duplicate_rows) / len(data)
        ) * 100

        st.write(
            "Duplicate Percentage:",
            round(duplicate_percentage, 2),
            "%"
        )

        if len(duplicate_rows) > 0:

            st.warning(
                "Duplicate records can cause certain observations "
                "to be counted multiple times."
            )

        else:

            st.success(
                "No duplicate records were detected, so duplicate rows "
                "are not affecting this dataset."
            )