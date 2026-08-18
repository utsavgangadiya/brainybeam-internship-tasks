# Task 3 — Missing Value Handling

## Objective

The objective of this task was to identify missing values in the Heart Disease dataset without using Pandas `.isna()` or `.dropna()`, apply multiple imputation techniques, and select an appropriate method.

## Missing Value Detection

Missing values were identified manually by checking each value for:

* `NaN` values using `value != value`
* Empty strings
* Blank values

No `.isna()` or `.dropna()` functions were used for missing-value detection or removal.

## Imputation Techniques

Three methods were implemented and compared:

### 1. Mean Imputation

Missing numerical values are replaced with the average of the available values.

**Advantage:** Simple and effective for normally distributed data.

**Limitation:** Can be strongly affected by outliers.

### 2. Median Imputation

Missing numerical values are replaced with the middle value after sorting the available values.

**Advantage:** Less affected by extreme values and outliers.

**Limitation:** May slightly reduce the natural variation in the data.

### 3. Mode Imputation

Missing values are replaced with the most frequently occurring value.

**Advantage:** Suitable for categorical features.

**Limitation:** Can make the most common category overrepresented.

## Method Selection

For numerical Heart Disease features, **median imputation** is preferred when the data contains outliers or is not normally distributed.

For categorical features, **mode imputation** is more appropriate.

Mean imputation can be used for numerical features when the data is approximately normally distributed and does not contain significant outliers.

Therefore, the best method depends on the characteristics of each feature rather than applying one method to the complete dataset.

## Conclusion

Multiple imputation techniques were successfully implemented without using `.isna()` or `.dropna()`.

The comparison showed that **median imputation is a practical choice for many numerical Heart Disease features**, while **mode imputation is suitable for categorical features**.

This task demonstrates how missing data can be identified and handled manually while considering the characteristics of the dataset.
