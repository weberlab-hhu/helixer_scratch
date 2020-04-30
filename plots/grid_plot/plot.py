#!/usr/bin/env python3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# load and transform animal results
df_aug = pd.read_csv('final animal eval - Augustus_all.csv')
df_nn = pd.read_csv('final animal eval - ensemble.csv')
df_meta = pd.read_csv('metadata_animals.csv')

genomes = set(df_aug['genome']).intersection(set(df_nn['genome']))

df_aug = df_aug[df_aug['genome'].isin(genomes)].sort_values('genome').reset_index(drop=True)
df_nn = df_nn[df_nn['genome'].isin(genomes)].sort_values('genome').reset_index(drop=True)
df_meta = df_meta[df_meta['species'].isin(genomes)].sort_values('species').reset_index(drop=True)

df_aug = df_aug.drop(columns=['acc_overall', 'f1_ig', 'f1_utr', 'f1_exon', 'f1_intron', 'legacy_f1_cds','f1_genic'])

# add nn values and metadata to aug df
df_aug['NN'] = df_nn['sub_genic']
df_aug['total_len'] = df_meta['total_len'] / 1e9
df_animals = df_aug.rename(columns={'sub_genic': 'AUG', 'genome': 'species'})

# remove training genomes
df_animals = df_animals[~df_animals['species'].isin(['mus_musculus','oryzias_latipes','gallus_gallus',
                                                     'theropithecus_gelada','anabas_testudineus',
                                                     'drosophila_melanogaster'])].reset_index(drop=True)

# load and transform plant results
df_aug = pd.read_csv('plant_LSTM_eval - Augustus_all.csv')
df_nn = pd.read_csv('final plant eval - ensemble.csv')
df_meta = pd.read_csv('metadata_plants.csv')

genomes = set(df_aug['genome']).intersection(set(df_nn['genome']))

df_aug = df_aug[df_aug['genome'].isin(genomes)].sort_values('genome').reset_index(drop=True)
df_nn = df_nn[df_nn['genome'].isin(genomes)].sort_values('genome').reset_index(drop=True)
df_meta = df_meta[df_meta['species'].isin(genomes)].sort_values('species').reset_index(drop=True)

df_aug = df_aug.drop(columns=['acc_overall', 'f1_ig', 'f1_utr', 'f1_exon', 'f1_intron', 'legacy_f1_cds', 'f1_genic'])

df_aug['NN'] = df_nn['sub_genic']
df_aug['total_len'] = df_meta['total_len'] / 1e9
df_plants = df_aug.rename(columns={'sub_genic': 'AUG', 'genome': 'species'})
df_plants = df_plants[~df_plants['species'].isin(['Athaliana','Bdistachyon','Creinhardtii','Gmax','Mguttatus','Mpolymorpha',
                                                  'Ptrichocarpa','Sitalica','Zmays'])].reset_index(drop=True)

# load aggregated overlapping data
df_ol_animals = pd.read_csv('animals_overlapping_aggregate.csv')
df_ol_plants = pd.read_csv('plants_overlapping_aggregate.csv')

# colors
aug_color = 'chocolate'
hel_color = 'royalblue'

# make subplot grid
fig = plt.figure(figsize=(12, 8))
outer = gridspec.GridSpec(1, 3, wspace=0.1, hspace=0.1)

# boxplots
boxplot_grid = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[0], wspace=0.1, hspace=0.1)

# ax = plt.Subplot(fig, boxplot_grid[0, 0])
# ax = sns.boxplot(y=df_animals["AUG"], medianprops={'color':'red'},
            # ax=ax, color="white", zorder=100)
# for patch in ax.artists:
    # r, g, b, a = patch.get_facecolor()
    # patch.set_facecolor((r, g, b, 0.0))

def add_boxplot(subplot_spec, data, swarm_color, title='', tick_labels=False):
    ax = plt.Subplot(fig, subplot_spec)
    ax = sns.boxplot(y=data, medianprops={'color':'red'}, ax=ax, color='white',
                     showfliers=False, showcaps=False, whiskerprops={'linewidth':0})
    plt.setp(ax.lines, zorder=100)
    ax = sns.swarmplot(y=data, ax=ax, color=swarm_color, size=4)
    ax.set_ylim((0.0, 1.0))
    ax.set_ylabel(None)
    ax.set_xticks([], [])
    if not tick_labels:
        ax.set_yticklabels([])
    if title:
        ax.set_title(title)
    fig.add_subplot(ax)

add_boxplot(boxplot_grid[0, 0], df_animals['AUG'], aug_color, tick_labels=True)
add_boxplot(boxplot_grid[0, 1], df_animals['NN'], hel_color)
add_boxplot(boxplot_grid[1, 0], df_plants['AUG'], aug_color, tick_labels=True)
add_boxplot(boxplot_grid[1, 1], df_plants['NN'], hel_color)

# scatterplots
scatterplot_grid = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[1], wspace=0.1, hspace=0.1)

def add_scatterplot(subplot_spec, data, xlabel=''):
    ax = plt.Subplot(fig, subplot_spec)
    ax = sns.regplot(x=data['total_len'], y=data['AUG'], ax=ax, color=aug_color, scatter_kws={'s':8}, line_kws={'linewidth':1.5})
    ax = sns.regplot(x=data['total_len'], y=data['NN'], ax=ax, color=hel_color, scatter_kws={'s':8}, line_kws={'linewidth':1.5})
    ax.set_ylim((0.0, 1.0))
    ax.set_xlim((-0.2, 5.0))
    ax.set_yticklabels([])
    ax.set_ylabel(None)
    if xlabel:
        ax.set_xlabel(xlabel)
    fig.add_subplot(ax)

add_scatterplot(scatterplot_grid[0], df_animals)
add_scatterplot(scatterplot_grid[1], df_plants, 'Genome Size in Gbp')

plt.show()


