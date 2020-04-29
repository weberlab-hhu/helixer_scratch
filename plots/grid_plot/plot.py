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
df_aug['total_len'] = df_meta['total_len']
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
df_aug['total_len'] = df_meta['total_len']
df_plants = df_aug.rename(columns={'sub_genic': 'AUG', 'genome': 'species'})
df_plants = df_plants[~df_plants['species'].isin(['Athaliana','Bdistachyon','Creinhardtii','Gmax','Mguttatus','Mpolymorpha',
                                                  'Ptrichocarpa','Sitalica','Zmays'])].reset_index(drop=True)

# load aggregated overlapping data
df_ol_animals = pd.read_csv('animals_overlapping_aggregate.csv')
df_ol_plants = pd.read_csv('plants_overlapping_aggregate.csv')

# make subplot grid
fig = plt.figure(figsize=(12, 8))
outer = gridspec.GridSpec(1, 3, wspace=0.1, hspace=0.1)

# boxplots
boxplot_grid = gridspec.GridSpecFromSubplotSpec(2, 1,
                subplot_spec=outer[0], wspace=0.1, hspace=0.1)

ax_animals_box = plt.Subplot(fig, boxplot_grid[0])

_, axes = plt.subplots(1, 2, sharey=True, figsize=(10,10))
sns.boxplot(y=df_animals["AUG"], medianprops={'color':'red'},
            ax=axes[0], color="white")
sns.swarmplot(y="AUG", data=df_animals, ax=axes[0], color="chocolate")
axes[0].set_title('AUGUSTUS')
axes[0].set_ylabel("Subgenic F1 Score")

sns.boxplot(y=df_animals["NN"], medianprops={'color':'red'},
            ax=axes[1], color="white")
sns.swarmplot(y="NN", data=df_animals, ax=axes[1], color="royalblue")
axes[1].set_title('Helixer')

axes.ylim((0.0, 1.0))


    for j in range(2):
        ax = plt.Subplot(fig, inner[j])
        t = ax.text(0.5,0.5, 'outer=%d, inner=%d' % (i,j))
        t.set_ha('center')
        ax.set_xticks([])
        ax.set_yticks([])
        fig.add_subplot(ax)

fig.show()


