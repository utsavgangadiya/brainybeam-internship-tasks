import pandas as pd
import math

# Load dataset
df = pd.read_csv("heart_disease_categorical.csv")

# Numerical columns to scale
numerical_columns = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]


# Manual Mean

def manual_mean(values):

    total = 0

    for value in values:
        total += value

    return total / len(values)


# Manual Median

def manual_median(values):

    values = values.copy()

    # Manual sorting
    for i in range(len(values)):

        for j in range(i + 1, len(values)):

            if values[i] > values[j]:

                values[i], values[j] = (
                    values[j],
                    values[i]
                )

    n = len(values)

    if n % 2 == 1:
        return values[n // 2]

    else:
        return (
            values[n // 2 - 1]
            + values[n // 2]
        ) / 2


# Manual Standard Deviation

def manual_std(values):

    mean = manual_mean(values)

    total = 0

    for value in values:

        difference = value - mean

        total += difference * difference

    variance = total / len(values)

    return math.sqrt(variance)


# Manual Percentile

def manual_percentile(values, percentage):

    values = values.copy()

    # Manual sorting
    for i in range(len(values)):

        for j in range(i + 1, len(values)):

            if values[i] > values[j]:

                values[i], values[j] = (
                    values[j],
                    values[i]
                )

    position = (len(values) - 1) * percentage

    lower = int(position)
    upper = lower + 1

    if upper >= len(values):
        return values[lower]

    fraction = position - lower

    return (
        values[lower]
        + fraction * (
            values[upper] - values[lower]
        )
    )


# Standardization
# Z = (X - Mean) / Standard Deviation

def standardize(values):

    mean = manual_mean(values)
    std = manual_std(values)

    result = []

    for value in values:

        if std == 0:
            result.append(0)

        else:
            result.append(
                (value - mean) / std
            )

    return result


# Robust Scaling
# X = (X - Median) / IQR

def robust_scale(values):

    median = manual_median(values)

    q1 = manual_percentile(
        values,
        0.25
    )

    q3 = manual_percentile(
        values,
        0.75
    )

    iqr = q3 - q1

    result = []

    for value in values:

        if iqr == 0:
            result.append(0)

        else:
            result.append(
                (value - median) / iqr
            )

    return result

# Create scaled datasets

standardized_df = df.copy()
robust_df = df.copy()

# Convert numerical columns to float
# because scaled values are decimals
for column in numerical_columns:

    standardized_df[column] = (
        standardized_df[column].astype(float)
    )

    robust_df[column] = (
        robust_df[column].astype(float)
    )


for column in numerical_columns:

    values = []

    for value in df[column]:

        if value == value:
            values.append(float(value))

    # Standardization
    standardized_values = standardize(values)

    # Robust scaling
    robust_values = robust_scale(values)

    index = 0

    for i in range(len(df)):

        value = df[column].iloc[i]

        if value == value:

            standardized_df.loc[
                i, column
            ] = standardized_values[index]

            robust_df.loc[
                i, column
            ] = robust_values[index]

            index += 1


# Display results

print("\nOriginal Dataset:")
print(df.head())

print("\nStandardized Dataset:")
print(standardized_df.head())

print("\nRobust Scaled Dataset:")
print(robust_df.head())


# Statistics

print("\nFeature Statistics:")

for column in numerical_columns:

    values = []

    for value in df[column]:

        if value == value:
            values.append(float(value))

    mean = manual_mean(values)
    median = manual_median(values)
    std = manual_std(values)

    q1 = manual_percentile(
        values,
        0.25
    )

    q3 = manual_percentile(
        values,
        0.75
    )

    iqr = q3 - q1

    print("\n", column)
    print("Mean:", round(mean, 2))
    print("Median:", round(median, 2))
    print("Standard Deviation:", round(std, 2))
    print("Q1:", round(q1, 2))
    print("Q3:", round(q3, 2))
    print("IQR:", round(iqr, 2))


# Save results

standardized_df.to_csv(
    "heart_disease_standardized.csv",
    index=False
)

robust_df.to_csv(
    "heart_disease_robust_scaled.csv",
    index=False
)

print("\nFiles created successfully!")
print("1. heart_disease_standardized.csv")
print("2. heart_disease_robust_scaled.csv")