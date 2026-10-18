"""Reproducible exploratory figures; descriptive, not causal findings."""
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from .config import FIGURES, NUMERIC_FEATURES, TARGET, create_output_dirs
from .data import load_data


def make_plots(df):
    create_output_dirs()
    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df[TARGET].value_counts().reindex([0, 1], fill_value=0)
    ax.bar(counts.index.astype(str), counts.values)
    ax.set(title='Machine failure class distribution', xlabel='Failure (0=no, 1=yes)', ylabel='Rows')
    plt.tight_layout();plt.savefig(FIGURES / 'target_distribution.png', dpi=160);plt.close()

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for ax, col in zip(axes.flat, NUMERIC_FEATURES):
        sns.histplot(data=df, x=col, hue=TARGET, bins=35, stat='density', common_norm=False,
                     element='step', ax=ax)
        ax.set_title(col)
    axes.flat[-1].axis('off')
    fig.tight_layout();fig.savefig(FIGURES / 'sensor_distributions.png', dpi=160);plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df[NUMERIC_FEATURES + [TARGET]].corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Pearson correlations (descriptive only)')
    fig.tight_layout();fig.savefig(FIGURES / 'correlations.png', dpi=160);plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    rate = df.groupby('Type')[TARGET].mean().mul(100).sort_index()
    ax.bar(rate.index, rate.values)
    ax.set(title='Observed failure rate by product type', xlabel='Type', ylabel='Failure rate (%)')
    fig.tight_layout();fig.savefig(FIGURES / 'failure_rate_by_type.png', dpi=160);plt.close(fig)
    print(f'Four figures saved in {FIGURES}')


def main():
    argparse.ArgumentParser().parse_args()
    make_plots(load_data())

if __name__ == '__main__':main()
