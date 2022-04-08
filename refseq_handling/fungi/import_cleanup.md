# gff 'by hand' fixes

### no transcript-leve parent
#### Just needed tRNA to be grepped out

./Candida_parapsilosis/input/fix.sh
./Aspergillus_nidulans/input/fix.sh
./Fusarium_fujikuroi/input/fix.sh
./Parastagonospora_nodorum/input/fix.sh
./Aspergillus_flavus/input/fix.sh
./Podospora_anserina/input/fix.sh

```commandline
# hide the original from geenuff --basedir identification
ori=`ls *.gff3.gz`
mv $ori $ori.ori
# orphan (gene-less) tRNA features and their exons removed with
zcat $ori.ori |grep -v tRNA > ${ori%.gz}
```

#### other

Needed tRNA, and one maybe manually added plasmid to be grepped out

./Pleurotus_ostreatus/input/fix.sh
```commandline
zcat $ori.ori |grep -v tRNA | grep -v NC_009905.1 > ${ori%.gz}
```

Needed tRNA and rRNA to be grepped out

./Encephalitozoon_cuniculi/input/fix.sh

```commandline
zcat $ori.ori |grep -v tRNA |grep -v rRNA > ${ori%.gz}
```

### Manual fixes 

./Candida_dubliniensis/input/fix.sh
```commandline
# hide the original from geenuff --basedir identification
# ori=`ls *.gff3.gz`
# mv $ori $ori.ori
# zcat $ori.ori > ${ori%.gz}
# manually fixed missing gene feature
# and missing protein ID to CDS for the gene rna-NC_012863.1:8411..10039
```

./Sordaria_macrospora/input/fix.sh
```commandline
# hide the original from geenuff --basedir identification
# ori=`ls *.gff3.gz`
# mv $ori $ori.ori
# zcat $ori.ori  > ${ori%.gz}
# manually fixed to add gene feature to the mRNA rna-NW_020185538.1:1799..3505
# and further to add a protein_id to the associated CDS feature
```

### clean up redundant features with python
Many if not most exons were there twice, with the second
copy being assigned as a copy of the 'gene' and not the 'rna'.
The following just filters all these second copies.

./Penicillium_rubens/input/fix.sh

```commandline
# hide the original from geenuff --basedir identification
ori=`ls *.gff3.gz`
mv $ori $ori.ori
```

```python
from geenuff.base.helpers import in_enum_values
from geenuff.base import types
import gzip

fout = open('GCF_000226395.1_PenChr_Nov2007_genomic.gff3', 'w')
with gzip.open('GCF_000226395.1_PenChr_Nov2007_genomic.gff3.gz.ori', 'rt') as f:
    for line in f:
        sline = line.split()
        prnt_line = True
        if line.startswith('#'):
            pass
        elif not in_enum_values(sline[2], types.TranscriptLevel):
            if sline[8].find('Parent=gene') > -1:
                prnt_line = False
        if prnt_line:
            fout.write(line)
fout.close()
```