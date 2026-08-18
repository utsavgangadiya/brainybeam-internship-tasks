import streamlit as st

st.title("Dataset Viewer")

# Upload file
file = st.file_uploader("Upload CSV file", type=["csv", "txt"])

if file:

    # Read file manually
    content = file.read().decode("utf-8")

    # Split into lines
    lines = content.splitlines()

    # Detect delimiter
    first_line = lines[0]

    if "," in first_line:
        delimiter = ","
    elif ";" in first_line:
        delimiter = ";"
    elif "\t" in first_line:
        delimiter = "\t"
    elif "|" in first_line:
        delimiter = "|"
    else:
        st.error("Delimiter not found")
        st.stop()

    # Header
    headers = first_line.split(delimiter)

    # Dataset rows
    data = []

    for line in lines[1:]:
        if line.strip():
            values = line.split(delimiter)

            # Make sure row has same number of values
            if len(values) == len(headers):
                data.append(values)

    st.write("Total Rows:", len(data))
    st.write("Total Columns:", len(headers))
    st.write("Detected Delimiter:", repr(delimiter))

  
    # Sorting
  

    st.subheader("Sorting")

    sort_column = st.selectbox(
        "Select column",
        headers
    )

    ascending = st.radio(
        "Order",
        ["Ascending", "Descending"],
        horizontal=True
    )

    column_index = headers.index(sort_column)

    try:
        data.sort(
            key=lambda x: float(x[column_index])
        )
    except:
        data.sort(
            key=lambda x: x[column_index].lower()
        )

    if ascending == "Descending":
        data.reverse()

  
    # Pagination
  

    st.subheader("Pagination")

    rows_per_page = st.selectbox(
        "Rows per page",
        [10, 25, 50, 100]
    )

    total_pages = (len(data) + rows_per_page - 1) // rows_per_page

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=max(1, total_pages),
        value=1
    )

    start = (page - 1) * rows_per_page
    end = start + rows_per_page

    page_data = data[start:end]

  
    # Display dataset
  

    table = []

    for row in page_data:
        record = {}

        for i in range(len(headers)):
            record[headers[i]] = row[i]

        table.append(record)

    st.dataframe(
        table,
        use_container_width=True
    )

    st.write(
        f"Page {page} of {total_pages}"
    )