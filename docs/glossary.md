# Glossary

Use this page to record terms and ideas that help you understand
professional analytics projects.

This project covers data mining and exploration:
reading raw CSV files into pandas DataFrames and inspecting their contents.

Pro-tip: Expand the VS Code **Outline** view (below the navigator on the right)
to see this file organization at-a-glance.

## Python and pandas

### pandas

pandas is a Python library for working with tabular data.
It provides the DataFrame as the core data structure
and tools for loading, inspecting, filtering, and summarizing data.

### DataFrame

A DataFrame is a two-dimensional table of data with labeled rows and columns.
It is the central data structure in pandas.
A DataFrame is similar to a spreadsheet or a database table.

### read_csv

`pd.read_csv()` is a pandas function that reads a CSV file
into a DataFrame.
It automatically detects column names from the first row of the file.

### shape

The shape of a DataFrame is a tuple showing the number of rows and columns.
For example, `(201, 5)` means 201 rows and 5 columns.
Checking shape after loading is a quick way to confirm the file loaded correctly.

### dtypes

dtypes (data types) describe what kind of value each column holds.
Common types include `int64` (integer), `float64` (decimal), and `object` (text).
Checking dtypes reveals whether a column loaded as the expected type.

### head

`df.head()` returns the first five rows of a DataFrame.
It is a quick way to see what the data looks like after loading.

### describe

`df.describe()` returns summary statistics for numeric columns.
It includes count, mean, min, max, and quartile values.
Unexpected values here often signal data quality issues.

## Data Exploration

### exploratory data analysis

Exploratory data analysis (EDA) is the process of inspecting a dataset
to understand its structure, distributions, and quality before analysis.
EDA informs decisions about cleaning, features, and modeling.

### distribution

A distribution shows how values in a column are spread.
A histogram is a common chart for visualizing distributions.
Understanding distributions helps identify outliers and skewed data.

### histogram

A histogram divides a numeric column into bins and shows
how many values fall into each bin.
It is useful for
