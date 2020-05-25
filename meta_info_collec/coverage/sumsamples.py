samplepath = 'sample_ids.txt'
qualitypath = 'good_stranded.txt'
chosenpath = 'good_stranded_files.txt'
outpath = 'selected.csv'

# import files for included checks
with open(qualitypath, 'r') as f:
    qualities = f.readlines()
    qualities = [x.rstrip() for x in qualities]

with open(chosenpath, 'r') as f:
    chosens = f.readlines()
    chosens = [x.rstrip() for x in chosens]

chosens = [x.replace('mapped/', '') for x in chosens]
chosens = [x.replace('.bam', '') for x in chosens]

handleout = open(outpath, 'w')
with open(samplepath, 'r') as f:
    for line in f:
        sample = line.rstrip()
        outline = '{},{},{}\n'.format(sample, sample in qualities, sample in chosens)
        handleout.write(outline)
handleout.close()
