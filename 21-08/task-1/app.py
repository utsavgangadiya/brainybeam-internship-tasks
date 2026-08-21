import pandas as pd
import csv

# Load processed dataset

df = pd.read_csv(
    "heart_disease_with_risk_factor.csv"
)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# Output file

output_file = "heart_disease_processed.csv"


# Manually write CSV

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(
        file,
        delimiter=",",
        quoting=csv.QUOTE_MINIMAL
    )

    # ----------------------------------------------
    # Write column names manually
    # ----------------------------------------------

    headers = []

    for column in df.columns:
        headers.append(str(column))

    writer.writerow(headers)

    # ----------------------------------------------
    # Write data rows manually
    # ----------------------------------------------

    for i in range(len(df)):

        row = []

        for column in df.columns:

            value = df[column].iloc[i]

            # Handle missing values
            if pd.isna(value):

                row.append("")

            else:

                # Remove unnecessary decimal .0
                # from integer-like values
                if isinstance(value, float):

                    if value.is_integer():
                        row.append(str(int(value)))
                    else:
                        row.append(str(value))

                else:
                    row.append(str(value))

        writer.writerow(row)


# Check file size

import os

file_size = os.path.getsize(output_file)

print("\nProcessed dataset saved successfully!")
print("File:", output_file)
print("File size:", file_size, "bytes")


# Verify saved file

with open(
    output_file,
    "r",
    encoding="utf-8"
) as file:

    lines = file.readlines()

print("Total lines:", len(lines))

print("\nFirst 5 lines:")

for line in lines[:5]:
    print(line.strip())