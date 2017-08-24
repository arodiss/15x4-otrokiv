import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_correlations(corr, file_name, x_labels, y_labels, mask=None, plot_title=None):
    plt.subplots(figsize=(11, 9))
    ax = plt.axes()

    hm = sns.heatmap(
        corr,
        annot=True,
        mask=mask,
        cmap=sns.diverging_palette(220, 10, as_cmap=True),
        vmax=0.8,
        vmin=-0.8,
        linewidths=.5,
        ax=ax
    )
    if plot_title:
        ax.set_title(plot_title)
    hm.set_xticklabels([label.replace('_', '\n') for label in x_labels], rotation=90)
    hm.set_yticklabels([label.replace('_', '\n') for label in y_labels], rotation=0)
    hm.get_figure().savefig('figures/' + file_name)


if __name__ == '__main__':
    target_metrics = ['score', 'youtube_score', 'youtube_minutes watched', 'youtube_comments', 'youtube_avg watch',
                      'youtube_likes', 'youtube_dislikes', 'youtube_shares', 'youtube_playlists', 'youtube_subscribers']
    source_metrics = ['knowledge', 'science', 'narrative', 'fun', 'slides', 'charisma', 'video_sound', 'understanding',
                      'conversion', 'is_hard_science', 'youtube_length']

    data = pd.read_csv('data/concatenated.csv')
    correlations = data.corr()
    correlations = correlations[target_metrics]
    correlations = correlations.loc[source_metrics]
    plot_correlations(correlations, "correlations.png", target_metrics, source_metrics)

    target_metrics = ['in_score', 'in_knowledge', 'in_science', 'in_narrative', 'in_fun', 'in_slides', 'in_charisma', 'in_video_sound', 'in_understanding']
    source_metrics = ['out_score', 'out_knowledge', 'out_science', 'out_narrative', 'out_fun', 'out_slides', 'out_charisma', 'out_video_sound', 'out_understanding']
    correlations = data.corr()
    correlations = correlations[target_metrics]
    correlations = correlations.loc[source_metrics]
    mask = np.ones_like(correlations, dtype=np.bool)
    np.fill_diagonal(mask, False)
    plot_correlations(correlations, "correlations-cross.png", target_metrics, source_metrics, mask=mask)
