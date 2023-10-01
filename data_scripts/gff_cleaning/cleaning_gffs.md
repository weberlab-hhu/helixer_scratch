# How did we get past all those geenuff errors when import GFFs into a GeenuFF db from various sources?

Well, the fast answer is it depends on various sources, and how consistent the gff3s are. 
The GeenuFF parser is designed to be strict and fail on any deviation from the standard specification
and what it is implemented
to handle. The idea is fail early and loud, and make a human clean up the gff3 file
as opposed to silently bricking Helixer's future training data by misinterpreting a non-standard gff3.

Until we have a lot more time available, we can only safely automate and handle some of the most common
errors... we know it's not ideal, but maintain that it's better than failing silently. 

## No really, how did we import hundreds of gffs from Ensembl for the manuscript and to train the v0.3\* models ?

OK, we fought through it once (manually checking that we understood where there errors were coming
from as we went, and that these changes were largely just filtering extra things in the gff3 files
that were never meant to relate to protein-coding genes, and/or were very rare)
Of course we meant to clean it up... and then didn't do it.

So buckle-up, this is historical documentation, not a recommendation, and this is ugly. 

First, we simply stripped all tRNA and rRNA features (from animal gffs), for the fungi skip ahead
to individual species custom fixes (we ran those first and handled them individually, still). Plants didn't
need this (bc Phytozome is fairly strict too).

```
zcat <path/to>.gff3.gz |grep -v tRNA |grep -v rRNA > ncRNA_filtered.gff3.bu
```

Then we use filter\_parentless\_gff3.py, which is the script from the same repo, sister to this readme file,
to remove all features from the gff that were lacking an intentional Parent feature, but
would be expected to have one.
(this is a minimalist, hackish, and surely not robust script, just FYI).

```
# filter_parentless_gff3.py takes 
python filter_parentless_gff3.py -i ncRNA_filtered.gff3.bu > ncRNA_filtered.gff3
```

That worked for most genomes...

### Individual species custom fixes

Sigh.

A lot of species still required their own specific solution. There are many many different ways to break a gff spec. 

You will find a bunch of custom 1-species fixes in `fixgffs/`. 

Heads up that this is an absolute mess, as these were done progressively,
there's almost certainly some outdated bits and
lots of copy-pasta horrors; and things in the comments that should be automated, and 
copied comments that are then totally misleading.

It definitely might be worth trying to run the fungi through the above steps, befor trying the custom scripts. 

Still, uploading these because these scripts a marginally better record than no record whatsoever; 
and the time to rerun, clean up and check all this is simply not in sight. 

So if you try to use these and run into problems, both issues and pull requests would be appreciated!

