def plot_bar_chart(ax, df, value_column, title):
    sums = df.groupby("category")[value_column].sum()
    if not sums.empty:
        ax.bar(sums.index, sums)
        ax.set_title(title, fontsize=16)
        ax.set_ylabel("Amount")
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
    else:
        ax.set_visible(False)
