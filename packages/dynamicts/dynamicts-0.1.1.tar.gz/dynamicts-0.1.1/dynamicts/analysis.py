"""
analysis.py

This module provides the TsaAnalysis class for exploratory and statistical analysis of time series data,
including distribution visualization, missing value checks, outlier detection, and rolling statistics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import skew, kurtosis

from dynamicts.report_generator import log_plot_to_md_report, log_plot_to_html_report, log_message_to_html_report

class TsaAnalysis:
    """
    Time Series Analysis class for basic EDA and diagnostics on time series data.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing the time series data.
    date_col : str, default="date"
        Name of the column representing dates.
    target_col : str, default="y"
        Name of the column representing the target variable.
    """
    def __init__(self, df:pd.DataFrame, date_col: str = "date", target_col: str = "y"):
        """
        Initialize the TsaAnalysis object.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe containing the time series data.
        date_col : str
            The name of the date column.
        target_col : str
            The name of the target column.
        """
        # self.raw_df = df.copy() #Incase I might need to do the step here
        self.date_col = date_col
        self.target_col = target_col
        self.df = df
        

    def plot_distribution(self):
        """
        Plot the distribution (histogram + KDE) and boxplot of the target variable.
        The plots are logged to the HTML report.
        """
        y = self.df[self.target_col].dropna()
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        #Histogram + KDE
        sns.histplot(y, kde=True, ax=axes[0], bins=30, color='cornflowerblue')
        axes[0].set_title(f"Distribution of {self.target_col}")
        axes[0].set_xlabel(self.target_col)
        axes[0].set_ylabel("Frequency")

        #Boxplot
        sns.boxplot(x=y, ax=axes[1], color="lightcoral")
        axes[1].set_title(f'Boxplot of {self.target_col}')
        axes[1].set_xlabel(self.target_col)

        plt.tight_layout()

        #Save to md report
        # log_plot_to_md_report(fig, title=f"Distribution of {self.target_col}")
        log_plot_to_html_report(fig, title=f"Distribution of {self.target_col}")
        plt.close(fig)

    def check_distribution_stats(self):
        """
        Compute and log skewness and kurtosis statistics for the target variable.
        Provides interpretation of the distribution's symmetry and tail behavior.
        """
        y = self.df[self.target_col].dropna()

        skewness_val = skew(y)
        kurtosis_val = kurtosis(y)

        # Interpretation
        if abs(skewness_val) < 0.5:
            skew_msg = "approximately_symmetric"
        elif skewness_val > 0:
            skew_msg = "right_skewed"
        else:
            skew_msg = "left_skewed"

        if kurtosis_val < 0:
            kurt_msg = "light_tailed (plattkurtic)"
        elif kurtosis_val > 0:
            kurt_msg = "heavy-tailed (lepokurtic)" 
        else: 
            kurt_msg = "normal-tailed (mesokurtic)"

        full_msg = (
        f"Skewness of '{self.target_col}': {skewness_val:.4f}\n"
        f"Kurtosis of '{self.target_col}': {kurtosis_val:.4f}\n"
        f"→ Distribution is {skew_msg} and {kurt_msg}."
        )

        log_message_to_html_report(full_msg, title=f"Distribution Stats: {self.target_col}")
    
    def check_missing_values(self):
        """
        Check and log the number and percentage of missing values in the target column.
        Provides recommendations if missing values are present.
        """
        series = self.df[self.target_col]
        total_points = len(series)
        missing_count = series.isna().sum()
        missing_percentage = (missing_count/total_points) * 100

        msg = f"""
            Total Observations: {total_points}
            Missing values in '{self.target_col}': {missing_count} ({missing_percentage:.2f}%)

            
        """
        if missing_count > 0:
            msg = msg+"<b>Recommendation:</b> Consider forward/backward fill or interpolation if your model does not support missing values."
        log_message_to_html_report(msg.strip(), title=f"Missing Value Analysis for '{self.target_col}'")

    def detect_outliers(self, method="both", plot=True):
        """
        Detect outliers in the target variable using IQR, Z-Score, or both methods.
        Optionally plots and logs the outliers.

        Parameters
        ----------
        method : str, default="both"
            Outlier detection method: "iqr", "zscore", or "both".
        plot : bool, default=True
            Whether to plot the outliers on a line plot.
        """
        y = self.df[self.target_col].dropna()

        # IQR method
        Q1 = y.quantile(0.25)
        Q3 = y.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = y[(y < Q1 - 1.5 * IQR) | (y > Q3 + 1.5 * IQR)]

        # Z-Score method
        z_scores = np.abs(stats.zscore(y))
        z_outliers = y[z_scores > 3]

        # Combine or choose
        if method == "iqr":
            combined_outliers = iqr_outliers
            method_label = "IQR"
        elif method == "zscore":
            combined_outliers = z_outliers
            method_label = "Z-Score"
        else:
            combined_outliers = y[(y.index.isin(iqr_outliers.index)) | (y.index.isin(z_outliers.index))]
            method_label = "IQR + Z-Score"

        outlier_count = len(combined_outliers)
        total = len(y)
        percentage = (outlier_count / total) * 100

        msg = f"""
        Outlier Detection using: {method_label}
        Total Observations: {total}
        Outliers Detected: {outlier_count} ({percentage:.2f}%)

        <b>Recommendation:</b> Investigate these points manually before deciding to remove or treat them.
        """

        log_message_to_html_report(msg.strip(), title=f"Outlier Detection ({method_label})")

        if plot:
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.lineplot(x=y.index, y=y, label="Original Data", ax=ax)
            sns.scatterplot(x=combined_outliers.index, y=combined_outliers, color='red', s=40, label="Outliers", ax=ax)
            ax.set_title(f"Outliers Detected using {method_label}")
            ax.set_ylabel(self.target_col)
            ax.set_xlabel("Date")
            plt.xticks(rotation=45)
            plt.tight_layout()

            log_plot_to_html_report(fig, title=f"{method_label} Outlier Detection for {self.target_col}")
            plt.close(fig)

    def measure_rolling_statistics(self, window=7):
        """
        Compute and plot rolling mean, standard deviation, and covariance for the target variable.

        Parameters
        ----------
        window : int, default=7
            The window size for rolling statistics.
        """
        series = self.df[self.target_col]

        roll_mean = series.rolling(window).mean()
        roll_std = series.rolling(window).std()
        roll_cov = series.rolling(window).cov(series.shift(1))

        # Plotting
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.plot(series.index, series, label="Original", alpha=0.5)
        ax.plot(roll_mean.index, roll_mean, label="Rolling Mean", color='blue')
        ax.plot(roll_std.index, roll_std, label="Rolling Std Dev", color='green')
        ax.plot(roll_cov.index, roll_cov, label="Rolling Covariance", color='purple')
        ax.set_title(f"Rolling Statistics (Window={window})")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        log_plot_to_html_report(fig, title=f"Rolling Statistics of {self.target_col}")
        plt.close(fig)

        # Logging brief stats
        msg = f"""
        Rolling statistics over window = {window} computed for:
        1. Mean
        2. Standard Deviation
        3. Covariance (with lagged series)

        <b>Tip:</b> Rolling metrics help identify trends, volatility, and local stability.
        """
        log_message_to_html_report(msg.strip(), title="Rolling Statistics Summary")


# Example
df = pd.read_csv("data/complaints.csv")
# df['date'] = pd.to_datetime(df['week'])
# df = df.set_index('date')
# df.index.name = 'date'
# df["complaints"] = df["complaints"]str.replace(",","").astype(int)
# df.to_csv("data/complaints.csv")
print(df.head())

# Rename the 'complaints' column to 'y'
# df = df.rename(columns={'complaints': 'y'})
tsa = TsaAnalysis(df, date_col="date", target_col="complaints")
tsa.plot_distribution()
tsa.check_distribution_stats()
tsa.check_missing_values()
tsa.detect_outliers()
tsa.measure_rolling_statistics()