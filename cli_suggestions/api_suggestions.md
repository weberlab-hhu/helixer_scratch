# Geenuff/import2geenuff.py #

## Current cli help output ## 

usage: import2geenuff.py [-h] [--basedir BASEDIR] [--config-file CONFIG_FILE] [--gff3 GFF3] [--fasta FASTA] [--db-path DB_PATH] [--log-file LOG_FILE] [--replace-db] --species SPECIES [--accession ACCESSION] [--version VERSION] [--acquired-from ACQUIRED_FROM]

optional arguments:  
  -h, **--help**            show this help message and exit  
  **--basedir** BASEDIR     organized output (& input) directory. If this is not set, all four custominput parameters must be set.  
  **--config-file** CONFIG_FILE  
  **--replace-db**          whether to override a GeenuFF database found at the default location or at the location of **--db**_path  

Override default with custom input/output location::  
  **--gff3** GFF3           gff3 formatted file to parse / standardize  
  **--fasta** FASTA         fasta file to parse standardize  
  **--db-path** DB_PATH     path of the GeenuFF database  
  **--log-file** LOG_FILE   output path for import log (default basedir/output/import.log)  
  
Possible genome attributes::  
  **--species** SPECIES     name of the species  
  **--accession** ACCESSION  
  **--version** VERSION     genome version  
  **--acquired-from** ACQUIRED_FROM  
						genome source  

## Proposed changes ## 
### In general ###

* rename to import.py
* remove basedir functionality as it is probably a bit to complicated for new users

### New CLI ###

usage: import.py [-h] [--config-file CONFIG_FILE] --gff3 GFF3 --fasta FASTA --db-path DB_PATH [--log-file LOG_FILE] [--replace-db] --species SPECIES [--accession ACCESSION] [--version VERSION] [--acquired-from ACQUIRED_FROM]

optional arguments:  
  -h, **--help**            Show this help message and exit.  
  **--config-file** CONFIG_FILE  Config in form of a YAML file with lower priority than parameters given on the command line.  
  **--replace-db**          Whether to override a GeenuFF database found at the default location or at the location of **--db-path**.  
  **--log-file** LOG_FILE   Output path for the import log (default is current directory).  

Input/output locations:  
  **--gff3** GFF3           gff3 formatted file to parse / standardize  
  **--fasta** FASTA         fasta file to parse standardize  
  **--db-path** DB_PATH     path of the GeenuFF database  
  
Possible genome attributes:  
  **--species** SPECIES     The name of the species.  
  **--accession** ACCESSION More specific species ID.  
  **--version** VERSION     The genome version.  
  **--acquired-from** ACQUIRED_FROM The genome source.  


# Helixer/export.py #
## Current cli help output ## 

usage: export.py [-h] [--input-db-path INPUT_DB_PATH] [--direct-fasta-to-h5-path DIRECT_FASTA_TO_H5_PATH] --output-path OUTPUT_PATH [--add-additional ADD_ADDITIONAL] [--species SPECIES] [--chunk-size CHUNK_SIZE] [--modes MODES] [--write-by WRITE_BY] [--compression {gzip,lzf}]
                 [--no-multiprocess]

optional arguments:  
  -h, **--help**            show this help message and exit  

Data input and output:  
  **--input-db-path** INPUT_DB_PATH  Path to the GeenuFF SQLite input database (has to contain only one genome).  
  **--direct-fasta-to-h5-path** DIRECT_FASTA_TO_H5_PATH  Directly convert from a FASTA file to .h5, circumventing import into a Geenuff database  
  **--output-path** OUTPUT_PATH  Output file for the encoded data. Must end with ".h5"  
  **--add-additional** ADD_ADDITIONAL  outputs the datasets under alternatives/{add-additional}/ (and checks sort order against existing "data" datasets). Use to add e.g. additional annotations from Augustus.  
  **--species** SPECIES     Species name. Only used with **--direct-fasta-to-h5-path**.  
  
Data generation parameters:  
  **--chunk-size** CHUNK_SIZE  Size of the chunks each genomic sequence gets cut into.  
  **--modes** MODES         either "all" (default), or a comma separated list with desired members of the following {X, y, anno_meta, transitions} that should be exported. This can be useful, for instance when skipping transitions (to reduce size/mem) or skipping X because you are  
                        adding an additional annotation set to an existing file.  
  **--write-by** WRITE_BY   write in super-chunks with this many bp, will be rounded to be divisible by chunk-size  
  **--compression** {gzip,lzf}  Compression algorithm used for the .h5 output files compression level is set as 4.  
  **--no-multiprocess**     Whether to parallize numerification of large sequences. Uses 2x the memory.  

## Proposed changes ## 
### In general ###
* split into two scripts: export-from-geenuff.py and export-from-fasta.py
* always give option for config file in YAML format like with Geenuff
* not sure what to do about **--modes** (most combinations will not work; what do we need here?)
* nice to have: change **--write-by** to **--maximum-memory**, which then uses the value to calculate to maximum write-by value

### New CLI ###
#### export-from-geenuff.py ####
usage: export-from-geenuff.py [-h] [--config-file CONFIG_FILE] --input-db-path INPUT_DB_PATH --output-path OUTPUT_PATH [--add-additional ADD_ADDITIONAL] [--chunk-size CHUNK_SIZE] [--modes MODES] [--write-by WRITE_BY] [--compression {gzip,lzf}]

optional arguments:  
  -h, **--help**            show this help message and exit  
  **--config-file** CONFIG_FILE  Config in form of a YAML file with lower priority than parameters given on the command line.  

Data input and output:  
  **--input-db-path** INPUT_DB_PATH  Path to the GeenuFF SQLite input database (has to contain only one genome).  
  **--output-path** OUTPUT_PATH  Output file for the encoded data. Must end with ".h5"  
  **--add-additional** ADD_ADDITIONAL  Outputs the datasets under alternatives/{add-additional}/ (and checks sort order against existing "data" datasets). Use to add e.g. additional annotations from Augustus.  
  
Data generation parameters:  
  **--chunk-size** CHUNK_SIZE  Size of the chunks each genomic sequence gets cut into. (Default is 20000.)  
  **--modes** MODES         Either "all" (default), or a comma separated list with desired members of the following {X, y, anno_meta, transitions} that should be exported. This can be useful, for instance when skipping transitions (to reduce size/mem) or skipping X because you are  adding an additional annotation set to an existing file.  
  **--write-by** WRITE_BY   Write in super-chunks with this many base pairs, which will be rounded to be divisible by chunk-size. (Default is 10000000000).  
  **--compression** {gzip,lzf}  Compression algorithm used for the intermediate .h5 output files with a fixed compression level of 4. (Default is "gzip", which is much slower than "lzf".)  
  **--no-multiprocess**     Whether to not parallize the numerification of large sequences. Uses half the memory but can be much slower when many CPU cores can be utilized.  

#### export-from-fasta.py ####
usage: export-from-fasta.py [-h] [--config-file CONFIG_FILE] --fasta-path FASTA-PATH --output-path OUTPUT_PATH --species SPECIES [--chunk-size CHUNK_SIZE] [--compression {gzip,lzf}] [--no-multiprocess]

optional arguments:  
  -h, **--help**            show this help message and exit  
  **--config-file** CONFIG_FILE  Config in form of a YAML file with lower priority than parameters given on the command line.  
  **--species** SPECIES     Species name. 

Data input and output:  
  **--fasta-path** FASTA-PATH  Directly convert from a FASTA file to .h5.  
  **--output-path** OUTPUT_PATH  Output file for the encoded data. Must end with ".h5".  
  
Data generation parameters:  
  **--chunk-size** CHUNK_SIZE  Size of the chunks each genomic sequence gets cut into. (Default is 20000.)  
  **--compression** {gzip,lzf}  Compression algorithm used for the intermediate .h5 output files with a fixed compression level of 4. (Default is "gzip", which is much slower than "lzf".)  
  **--no-multiprocess**     Whether to not parallize the numerification of large sequences. Uses half the memory but can be much slower when many CPU cores can be utilized.  

# Helixer/helixer.py #
* New central helixer script, that does the FASTA -> GFF conversion
* Has access to 3 internal models for animals, plants and fungi
* Chunk size is fixed now due to the trained models
* Parameters from export-from-fasta.py and HelixerPost except for the species name, which is now not useful anymore

usage: helixer.py [-h] [--config-file CONFIG_FILE] --fasta-input-path FASTA_INPUT_PATH --gff-output-path GFF_OUTPUT_PATH --species-category {animal,plant,fungi} [--compression {gzip,lzf}] [--no-multiprocess] [--window-size WINDOW_SIZE] [--edge-threshold EDGE_THRESHOLD] [--peak-threshold PEAK_THRESHOLD] [--min-coding-length MIN_CODING_LENGTH]

optional arguments:  
  -h, **--help**            show this help message and exit  
  **--config-file** CONFIG_FILE  Config in form of a YAML file with lower priority than parameters given on the command line.  

Data input and output:  
  **--fasta-input-path** FASTA_INPUT_PATH  Directly convert from a FASTA file to .h5.  
  **--gff-output-path** GFF_OUTPUT_PATH  Output path for the GFF file.  
  **--species-category** {animal,plant,fungi} What model to use for the annotation. (Default is "animal".)  
  
Data generation parameters:  
  **--compression** {gzip,lzf}  Compression algorithm used for the intermediate .h5 output files with a fixed compression level of 4. (Default is "gzip", which is much slower than "lzf".)  
  **--no-multiprocess**     Whether to not parallize the numerification of large sequences. Uses half the memory but can be much slower when many CPU cores can be utilized.  

Post-processing parameters:  
  **--window-size** WINDOW_SIZE  [description]. (Default is 100).  
  **--edge-threshold** EDGE_THRESHOLD  [description]. (Default is 0.1).  
  **--peak-threshold** PEAK_THRESHOLD  [description]. (Default is 0.8).  
  **--min-coding-length** MIN_CODING_LENGTH  [description]. (Default is 60).  



	


