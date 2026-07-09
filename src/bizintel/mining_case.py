"""mining_case.py - example.

An example of exploring and mining raw smart sales data.

Author: Denise Case
Date: 2026-06

Process:
    - Load raw CSV data files.
    - Inspect each dataset (shape, columns, types).
    - Check basic data quality (missing values, duplicates).
    - Summarize numeric columns.
    - Visualize product price distribution.
    - Visualize sales trend over time.
    - Log a summary of findings.

Data Source:
- data/raw/customers_data.csv
- data/raw/products_data.csv
- data/raw/sales_data.csv

Terminal command to run this file from the root project folder:

uv run python -m bizintel.mining_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it with your alias, and modify your copy.
  If you do, include your command to run it in the docstring above and in README.md.
"""

# === DECLARE IMPORTS (bring in free code from elsewhere) ===

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import matplotlib.pyplot as plt
import pandas as pd

from bizintel.utils_data import (
    check_quality,
    inspect_basic,
    load_data,
    summarize_numeric,
)
from bizintel.utils_logger import LOG, log_header
from bizintel.utils_viz import plot_line

# === DECLARE GLOBAL CONSTANTS AND CONFIGURATION ===

# In Python, a constant is a variable that should not change after it is defined.
# We indicate this with all capital letters and the Final type hint from the typing module.

# Raw data folder path (relative to the root project folder).
DATA_RAW: Final[Path] = Path("data/raw")

# The three raw data files for the smart sales project.
CUSTOMERS_FILE: Final[Path] = DATA_RAW / "customers_data.csv"
PRODUCTS_FILE: Final[Path] = DATA_RAW / "products_data.csv"
SALES_FILE: Final[Path] = DATA_RAW / "sales_data.csv"


# === Section 2. Define Reusable Functions ===

# === Section 2.1 DEFINE A PRICE DISTRIBUTION FUNCTION ===

# Define a reusable function that takes
# the products DataFrame as input
# and visualizes the distribution of unit prices.
# A histogram shows how many products fall into each price range.


def plot_price_distribution(df_products: pd.DataFrame) -> None:
    """Plot a histogram of product unit prices.

    WHY: Price distribution tells us whether products are
    clustered in a narrow range or spread across many price points.
    This is a key input for pricing strategy and product mix decisions.

    Args:
        df_products: Products DataFrame with UnitPrice column.

    Returns:
        None
    """
    LOG.info("Plotting price distribution")

    # Get the UnitPrice column as a single numeric Series (1D array)
    # Coerce errors to NaN so non-numeric values do not crash the chart
    # Call pd.to_numeric() to convert the column to numeric
    # Cast the result to a 1D pandas Series for clarity
    # By wrapping the result in pd.Series(),
    # we ensure that we have a Series object to hold all the prices.
    prices: pd.Series = pd.Series(
        pd.to_numeric(df_products["UnitPrice"], errors="coerce")
    )

    # Call the matplotlib subplots() method
    # to create a figure and axes for the histogram
    #
    # Pass in a figure size for better readability
    # (9, 5) means 9 inches wide and 5 inches tall
    # The subplots() function returns a tuple of (figure, axes)
    # We only need the axes object, so we use _ to ignore the figure

    _, ax = plt.subplots(figsize=(9, 5))

    # Call the ax.hist() method to plot the histogram
    #
    # The first argument (the parts inside the parentheses)
    # is the data, the prices Series (a 1D array)
    # We call .dropna() to remove any NaN values before plotting
    #
    # The second argument is the number of bins to divide the price range into
    # Each bin represents a price range
    # The height of each bar shows how many products fall in that range
    #
    # The third argument is the color of the bars
    # The fourth argument is the color of the edges of the bars
    # To find color strings that work in matplotlib,
    # see https://matplotlib.org/stable/gallery/color/named_colors.html

    ax.hist(prices.dropna(), bins=10, color="steelblue", edgecolor="white")

    # Set the title for the chart
    # And remind users to close the chart window to continue the workflow
    ax.set_title("Product Price Distribution (CLOSE chart to continue)")

    # Set the x-axis and y-axis labels for clarity
    ax.set_xlabel("Unit Price ($)")
    ax.set_ylabel("Number of Products")

    # Use plt.tight_layout() to automatically adjust the spacing
    # between the chart elements so they do not overlap
    plt.tight_layout()

    LOG.info("Price distribution chart created")


# === Section 2.2 DEFINE A SALES TREND FUNCTION ===

# Define a reusable function that takes the sales DataFrame
# and visualizes total sales amount over time.
# A line chart shows whether sales are growing, declining, or flat.


def plot_sales_trend(df_sales: pd.DataFrame) -> None:
    """Plot total sales amount by month.

    WHY: Sales trends over time are one of the most important
    KPIs in any BI dashboard.
    Knowing whether revenue is growing or declining drives
    decisions about staffing, inventory, and marketing.

    Args:
        df_sales: Sales DataFrame with SaleDate and SaleAmount columns.

    Returns:
        None
    """
    LOG.info("Plotting sales trend over time")

    # Make a copy to avoid modifying the original DataFrame
    df = df_sales.copy()

    # Convert SaleDate to a datetime type so we can group by month
    # Coerce errors to NaT (not a time) so bad dates do not crash the chart
    df["SaleDate"] = pd.to_datetime(df["SaleDate"], errors="coerce")

    # Convert SaleAmount to numeric, coercing errors to NaN
    df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors="coerce")

    # Create a YearMonth column for grouping
    # Period("M") means we group by year and month together
    # so January 2025 and January 2026 are separate groups
    df["YearMonth"] = df["SaleDate"].dt.to_period("M")

    # Group by YearMonth and sum the SaleAmount for each month
    # This returns a Series (a single column of values, one per region).
    # We cast to Series because we are grouping a single column.
    grouped: pd.Series = pd.Series(df.groupby("YearMonth")["SaleAmount"].sum())

    # Reset the index to turn the result back into a DataFrame
    # Convert YearMonth back to a string for plotting
    df_trend: pd.DataFrame = grouped.reset_index()
    df_trend["YearMonth"] = df_trend["YearMonth"].astype(str)

    # Plot the sales trend as a line chart
    # Pass in the following arguments:
    # - df: the DataFrame to plot (df_trend)
    # - x: the column for the x-axis (YearMonth)
    # - y: the column for the y-axis (SaleAmount)
    # - title: the chart title
    # - xlabel: the x-axis label
    # - ylabel: the y-axis label
    plot_line(
        df=df_trend,
        x="YearMonth",
        y="SaleAmount",
        title="Total Sales by Month",
        xlabel="Month",
        ylabel="Total Sales Amount ($)",
    )

    LOG.info("Sales trend chart created")


# === Section 2.3 DEFINE A SUMMARIZE FUNCTION ===

# Define a reusable function that takes all 3 DataFrames
# and logs a summary with analyst notes.


def summarize(
    df_customers: pd.DataFrame,
    df_products: pd.DataFrame,
    df_sales: pd.DataFrame,
) -> None:
    """Log a brief summary with analyst notes.

    Args:
        df_customers: Customers DataFrame.
        df_products: Products DataFrame.
        df_sales: Sales DataFrame.

    Returns:
        None
    """
    LOG.info("========================")
    LOG.info("SUMMARY")
    LOG.info("========================")

    # Get row and column counts using the shape attribute
    # shape[0] is rows, shape[1] is columns
    cust_rows: int = df_customers.shape[0]
    cust_cols: int = df_customers.shape[1]
    prod_rows: int = df_products.shape[0]
    prod_cols: int = df_products.shape[1]
    sale_rows: int = df_sales.shape[0]
    sale_cols: int = df_sales.shape[1]

    LOG.info(f"Customers:  {cust_rows} rows, {cust_cols} columns")
    LOG.info(f"Products:   {prod_rows} rows, {prod_cols} columns")
    LOG.info(f"Sales:      {sale_rows} rows, {sale_cols} columns")

    LOG.info("========================")
    LOG.info("ANALYST NOTES:")
    LOG.info("Any inconsistent data should be reviewed later.")
    LOG.info("Any duplicate rows should be reviewed later.")
    LOG.info("Cleaning and data preparation will be done in a later module.")
    LOG.info("========================")


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Main function to run the mining and exploration logic.

    This is where the main logic starts
    when this script is run.
    """
    # First, log the header for the BI module to indicate the start of the workflow.
    log_header(LOG, "BI")

    # Clearly indicate the start of the main function in the logs for easy tracking.
    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    # Use the imported log_path function to
    # log the paths of all critical paths and files for reference.
    log_path(LOG, "Raw data: ", DATA_RAW)
    log_path(LOG, "Customers:", CUSTOMERS_FILE)
    log_path(LOG, "Products: ", PRODUCTS_FILE)
    log_path(LOG, "Sales:    ", SALES_FILE)

    LOG.info("CALL a function to load each dataset.............")
    df_customers = load_data(CUSTOMERS_FILE, "customers")
    df_products = load_data(PRODUCTS_FILE, "products")
    df_sales = load_data(SALES_FILE, "sales")

    LOG.info("CALL a function to inspect each dataset..........")
    inspect_basic(df_customers, "customers")
    inspect_basic(df_products, "products")
    inspect_basic(df_sales, "sales")

    LOG.info("CALL a function to check data quality of each dataset........")
    check_quality(df_customers, "customers")
    check_quality(df_products, "products")
    check_quality(df_sales, "sales")

    LOG.info("CALL a function to summarize numeric columns in each dataset........")
    summarize_numeric(df_customers, "customers")
    summarize_numeric(df_products, "products")
    summarize_numeric(df_sales, "sales")

    LOG.info("CALL a function to plot price distribution........")
    plot_price_distribution(df_products)

    LOG.info("CALL a function to plot sales trend over time........")
    plot_sales_trend(df_sales)

    LOG.info("CALL a function to summarize the datasets........")
    summarize(df_customers, df_products, df_sales)

    LOG.info("CALL a function to show charts........")
    plt.show()

    LOG.info("Workflow complete")
    LOG.info("CLOSE chart windows to continue.")
    LOG.info("Terminate this process with CTRL+c as needed.")
    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    # This conditional ensures that main() is only called
    # when this script is run directly, not when imported.
    main()
