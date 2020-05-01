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
fig = plt.figure(figsize=(12, 6))
# nest gridspecs to have different spacing between column 2 and 3
outer_main = gridspec.GridSpec(1, 2, width_ratios=[2, 1], wspace=0.19)
outer_left = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=outer_main[0], wspace=0.2)
outer_right = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer_main[1])

# boxplots
boxplot_grid = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer_left[0], wspace=0.1, hspace=0.1)

def add_boxplot(subplot_spec, data, swarm_color, title='', tick_labels=False, superscript_label=False):
    ax = plt.Subplot(fig, subplot_spec)
    ax = sns.boxplot(y=data, medianprops={'color':'red'}, ax=ax, color='white',
                     showfliers=False, showcaps=False, whiskerprops={'linewidth':0})
    plt.setp(ax.lines, zorder=100)
    ax = sns.swarmplot(y=data, ax=ax, color=swarm_color, size=4)
    ax.set_ylim((0.0, 1.0))
    ax.set_xticks([], [])
    if not tick_labels:
        ax.set_yticklabels([])
        ax.set_ylabel(None)
    else:
        ax.set_ylabel('Subgenic F1')
    if title:
        ax.set_title(title)
    if superscript_label:
        ax.text(-0.48, 0.95, 'a)', transform=ax.transAxes, size=15, weight='bold')
    fig.add_subplot(ax)

add_boxplot(boxplot_grid[0, 0], df_animals['AUG'], aug_color, tick_labels=True, superscript_label=True)
add_boxplot(boxplot_grid[0, 1], df_animals['NN'], hel_color)
add_boxplot(boxplot_grid[1, 0], df_plants['AUG'], aug_color, tick_labels=True)
add_boxplot(boxplot_grid[1, 1], df_plants['NN'], hel_color)

# scatterplots
scatterplot_grid = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer_left[1], wspace=0.1, hspace=0.1)

def add_scatterplot(subplot_spec, data, xlabel='', superscript_label=False):
    ax = plt.Subplot(fig, subplot_spec)
    ax = sns.regplot(x=data['total_len'], y=data['NN'], ax=ax, color=hel_color,
                     scatter_kws={'s':8}, line_kws={'linewidth':1.5}, label='Helixer')
    ax = sns.regplot(x=data['total_len'], y=data['AUG'], ax=ax, color=aug_color,
                     scatter_kws={'s':8}, line_kws={'linewidth':1.5}, label='AUGUSTUS')
    ax.set_ylim((0.0, 1.0))
    ax.set_xlim((-0.2, 5.0))
    ax.set_yticklabels([])
    ax.set_ylabel(None)
    if xlabel:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xticklabels([])
        ax.set_xlabel(None)
        ax.legend(loc='lower left', fontsize='small')
    if superscript_label:
        ax.text(-0.14, 0.95, 'b)', transform=ax.transAxes, size=15, weight='bold')
    fig.add_subplot(ax)

add_scatterplot(scatterplot_grid[0], df_animals, superscript_label=True)
add_scatterplot(scatterplot_grid[1], df_plants, 'Genome Size in Gbp')

# line plots
lineplot_grid = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer_right[0], wspace=0.1, hspace=0.1)

def add_lineplot(subplot_spec, data, xlabel='', superscript_label=False):
    ax = plt.Subplot(fig, subplot_spec)
    ax.plot(range(100), data['f1'], color='tab:red', linestyle='dashed')
    ax.plot(range(100), data['f1_with_overlapping'], color='tab:red', label='Genic F1')
    ax.plot(range(100), data['acc'], color='tab:purple', linestyle='dashed')
    ax.plot(range(100), data['acc_with_overlapping'], color='tab:purple', label='Accuracy')
    ax.set_ylim((0.0, 1.0))

    ax.set_ylabel('Accuracy / Genic F1')
    ticks = [0, 50, 100]
    ax.set_xticks(ticks)
    if xlabel:
        ax.set_xlabel(xlabel)
        ax.set_xticklabels([t * 200 for t in ticks])
    else:
        ax.set_xlabel(None)
        ax.set_xticklabels([])
        ax.legend(loc='lower left', fontsize='small')
    if superscript_label:
        ax.text(-0.21, 0.95, 'c)', transform=ax.transAxes, size=15, weight='bold')
    fig.add_subplot(ax)

add_lineplot(lineplot_grid[0], df_ol_animals, superscript_label=True)
add_lineplot(lineplot_grid[1], df_ol_plants, xlabel='Basepair Position in Input Sequence')

plt.show()
