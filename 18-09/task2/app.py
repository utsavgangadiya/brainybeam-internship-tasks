# Heart Disease Prediction Using Machine Learning	Show summary statistics (mean, median, mode, min, max, std) by implementing manual calculations without using built-in statistical functions.
import streamlit as st
import csv
import math

st.title("Heart Disease Dataset - Summary Statistics")

# Upload dataset
file = st.file_uploader("Upload Heart Disease CSV", type=["csv"])

if file:

    # Read CSV manually
    content = file.read().decode("utf-8")
    lines = content.splitlines()

    reader = csv.reader(lines)
    rows = list(reader)

    headers = rows[0]
    data = rows[1:]

    st.write("Total Rows:", len(data))
    st.write("Total Columns:", len(headers))

    # Manual calculation functions

    def calculate_mean(values):
        total = 0

        for value in values:
            total += value

        return total / len(values)


    def calculate_median(values):
        sorted_values = values.copy()

        # Manual sorting
        for i in range(len(sorted_values)):
            for j in range(i + 1, len(sorted_values)):
                if sorted_values[i] > sorted_values[j]:
                    sorted_values[i], sorted_values[j] = (
                        sorted_values[j],
                        sorted_values[i]
                    )

        n = len(sorted_values)

        if n % 2 == 1:
            return sorted_values[n // 2]
        else:
            middle1 = sorted_values[(n // 2) - 1]
            middle2 = sorted_values[n // 2]

            return (middle1 + middle2) / 2


    def calculate_mode(values):
        frequency = {}

        for value in values:
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1

        mode = values[0]
        highest_frequency = frequency[mode]

        for value in frequency:
            if frequency[value] > highest_frequency:
                mode = value
                highest_frequency = frequency[value]

        return mode


    def calculate_min(values):
        smallest = values[0]

        for value in values:
            if value < smallest:
                smallest = value

        return smallest


    def calculate_max(values):
        largest = values[0]

        for value in values:
            if value > largest:
                largest = value

        return largest


    def calculate_std(values):
        mean = calculate_mean(values)

        squared_difference = 0

        for value in values:
            difference = value - mean
            squared_difference += difference * difference

        variance = squared_difference / len(values)

        return math.sqrt(variance)


    # Select numeric column

    numeric_columns = []

    for column_index in range(len(headers)):

        values = []

        for row in data:
            try:
                value = float(row[column_index])
                values.append(value)
            except:
                pass

        if len(values) > 0:
            numeric_columns.append(headers[column_index])


    column = st.selectbox(
        "Select a numeric column",
        numeric_columns
    )

    column_index = headers.index(column)

    # Get numeric values
    values = []

    for row in data:
        try:
            values.append(float(row[column_index]))
        except:
            pass

    # Calculate statistics

    if len(values) > 0:

        mean = calculate_mean(values)
        median = calculate_median(values)
        mode = calculate_mode(values)
        minimum = calculate_min(values)
        maximum = calculate_max(values)
        std = calculate_std(values)

        # Display results

        st.subheader("Summary Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Mean", round(mean, 2))
            st.metric("Median", round(median, 2))

        with col2:
            st.metric("Mode", round(mode, 2))
            st.metric("Minimum", round(minimum, 2))

        with col3:
            st.metric("Maximum", round(maximum, 2))
            st.metric("Standard Deviation", round(std, 2))

    else:
        st.error("No numeric values found in this column.")