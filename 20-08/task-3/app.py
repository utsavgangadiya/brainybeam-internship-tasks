import pandas as pd

# Load dataset

df = pd.read_csv("heart_disease_categorical.csv")


# Manual percentile rank function

def percentile_rank(values, current_value):

    # Count values smaller than current value
    below = 0

    # Count values equal to current value
    equal = 0

    for value in values:

        if value < current_value:
            below += 1

        elif value == current_value:
            equal += 1

    # Percentile rank
    rank = (
        (below + (equal / 2))
        / len(values)
    )

    return rank


# Get chol and thalach values

chol_values = []

thalach_values = []

for i in range(len(df)):

    chol = df["chol"].iloc[i]
    thalach = df["thalach"].iloc[i]

    if chol == chol and thalach == thalach:

        chol_values.append(float(chol))
        thalach_values.append(float(thalach))


# Create risk_factor

risk_factors = []

chol_percentiles = []
thalach_percentiles = []

for i in range(len(df)):

    chol = df["chol"].iloc[i]
    thalach = df["thalach"].iloc[i]

    # Handle missing values
    if chol != chol or thalach != thalach:

        risk_factors.append(None)
        chol_percentiles.append(None)
        thalach_percentiles.append(None)

        continue

    chol = float(chol)
    thalach = float(thalach)

    # Percentile ranking

    chol_rank = percentile_rank(
        chol_values,
        chol
    )

    thalach_rank = percentile_rank(
        thalach_values,
        thalach
    )

    chol_percentiles.append(chol_rank)
    thalach_percentiles.append(thalach_rank)

    # Domain knowledge
    #
    # High cholesterol = higher risk
    # Low maximum heart rate = higher risk

    cholesterol_risk = chol_rank

    heart_rate_risk = 1 - thalach_rank

    # Interaction term
    #
    # High cholesterol + low heart rate
    # together increase the risk score

    interaction = (
        cholesterol_risk *
        heart_rate_risk
    )

    # Final risk factor
    #
    # 40% cholesterol risk
    # 40% heart-rate risk
    # 20% interaction

    risk_factor = (
        0.40 * cholesterol_risk
        +
        0.40 * heart_rate_risk
        +
        0.20 * interaction
    )

    risk_factors.append(
        round(risk_factor, 4)
    )


# Add new feature

df["chol_percentile"] = chol_percentiles

df["thalach_percentile"] = thalach_percentiles

df["risk_factor"] = risk_factors


# Create risk category

risk_category = []

for value in df["risk_factor"]:

    if value != value:

        risk_category.append("Unknown")

    elif value >= 0.70:

        risk_category.append("High")

    elif value >= 0.40:

        risk_category.append("Medium")

    else:

        risk_category.append("Low")


df["risk_category"] = risk_category


# Display results

print("\nNew Feature Dataset:")
print(
    df[
        [
            "chol",
            "thalach",
            "chol_percentile",
            "thalach_percentile",
            "risk_factor",
            "risk_category"
        ]
    ].head(20)
)


# Save dataset

df.to_csv(
    "heart_disease_with_risk_factor.csv",
    index=False
)

print(
    "\nNew dataset saved as "
    "heart_disease_with_risk_factor.csv"
)