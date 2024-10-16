import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd
from wordcloud import WordCloud

class Visualization:
    def __init__(self, df):
        """
        Initializes the class with a DataFrame.

        Args:
            df: A Pandas DataFrame
        """
        self.df = df

    def format_func(self, value, tick_number):
        """
        Formatter for large numbers.

        Args:
            value: The value to format.
            tick_number: The tick number.
        """
        if value >= 1_000_000:
            return f'{value / 1_000_000:.1f}M'
        elif value >= 1_000:
            return f'{value / 1_000:.1f}K'
        else:
            return str(int(value))

    def combined_plot(self, cols, plt_fn, fig_size=(40, 45)):
        """
        Generates combined plots with a single dataset.

        Args:
            cols: List of column names to plot.
            plt_fn: Function to create the plots.
            fig_size: Tuple for figure size.
        """
        n_col = 2
        n_row = (len(cols) + n_col - 1) // n_col
        fig, axes = plt.subplots(n_row, n_col, figsize=fig_size)
        axes = axes.flatten()
        
        for i, col in enumerate(cols):
            plt_fn(axes[i], col)
            
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.show()

    def bar_plot(self, ax, col):
        """
        Bar plot for categorical columns.

        Args:
            ax: The axes to plot on.
            col: The column name for which to create the bar plot.
        """
        value_counts = self.df[col].value_counts().sort_values(ascending=False)
        if len(value_counts) > 8:
            value_counts = value_counts.head(8)
            
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette="Paired", order=value_counts.index)

        ax.set_title(f'Top {len(value_counts)} Most Frequent Values in "{col}"', fontsize=20)
        ax.set_xlabel(f'{col}', fontsize=16)
        ax.set_ylabel('Frequency', fontsize=16)

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_func))

    def dist_plot(self, ax, col, bins=30):
        """
        Distribution plot for numerical columns.

        Args:
            ax: The axes to plot on.
            col: The column name for which to create the distribution plot.
            bins: Number of bins for the histogram.
        """
        sns.histplot(self.df[col], bins=bins, ax=ax, kde=True, color='blue')
        
        ax.set_title(f'Distribution of "{col}"', fontsize=20)
        ax.set_xlabel(f'{col}', fontsize=16)
        ax.set_ylabel('Frequency', fontsize=16)

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_func))

    def box_plot(self, ax, col):
        """
        Box plot for numerical columns.

        Args:
            ax: The axes to plot on.
            col: The column name for which to create the box plot.
        """
        sns.boxplot(x=self.df[col], ax=ax, color='lightblue')

        ax.set_title(f'Box Plot of "{col}"', fontsize=20)
        ax.set_xlabel(f'{col}', fontsize=16)

    def pie_chart(self, ax, col):
        """
        Pie chart for categorical columns.

        Args:
            ax: The axes to plot on.
            col: The column name for which to create the pie chart.
        """
        value_counts = self.df[col].value_counts()
        
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Paired"))
        ax.axis('equal')

        ax.set_title(f'Pie Chart of "{col}"', fontsize=20)

    def scatter_plot(self, ax, x_col, y_col):
        """
        Scatter plot for numerical columns.

        Args:
            ax: The axes to plot on.
            x_col: The column name for the x-axis.
            y_col: The column name for the y-axis.
        """
        sns.scatterplot(data=self.df, x=x_col, y=y_col, ax=ax, alpha=0.6)

        ax.set_title(f'Scatter Plot: {y_col} vs. {x_col}', fontsize=15)
        ax.set_xlabel(f'{x_col}', fontsize=12)
        ax.set_ylabel(f'{y_col}', fontsize=12)

    def time_series_plot(self, date_col, value_cols, fig_size=(16, 8)):
        """
        Generates combined time series plots for specified value columns.

        Args:
            date_col: The column name for the date.
            value_cols: List of column names for the values to plot.
            fig_size: Tuple for figure size.
        """
        self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce') 
        self.df['year'] = self.df[date_col].dt.year

        n_col = len(value_cols)
        fig, axes = plt.subplots(1, n_col, figsize=fig_size)

        for ax, col in zip(axes, value_cols):
            time_series_data = self.df.groupby('year')[col].sum().reset_index()
            sns.lineplot(data=time_series_data, x='year', y=col, ax=ax, marker='o')

            ax.set_title(f'Time Series of "{col}" Over Years', fontsize=15)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel(col, fontsize=12)

        plt.tight_layout()
        plt.show()


    def word_cloud(self, ax, text_col):
        """
        Generates a word cloud from a specified text column.

        Args:
            ax: The axes to plot on.
            text_col: The column name from which to generate the word cloud.
        """
        text = ' '.join(self.df[text_col].dropna())

        wordcloud = WordCloud(width=1000, height=600, background_color='white').generate(text)

        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f'Word Cloud for "{text_col}"', fontsize=14)