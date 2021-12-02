# Geenuff/import2geenuff.py #

## Current cli help output ## 

usage: import2geenuff.py [-h] [--basedir BASEDIR] [--config-file CONFIG_FILE] [--gff3 GFF3] [--fasta FASTA] [--db-path DB_PATH] [--log-file LOG_FILE] [--replace-db] --species SPECIES [--accession ACCESSION] [--version VERSION] [--acquired-from ACQUIRED_FROM]

optional arguments:
  -h, --help            show this help message and exit
  --basedir BASEDIR     organized output (& input) directory. If this is not set, all four custominput parameters must be set.
  --config-file CONFIG_FILE
  --replace-db          whether to override a GeenuFF database found at the default location or at the location of --db_path

Override default with custom input/output location::
  --gff3 GFF3           gff3 formatted file to parse / standardize
  --fasta FASTA         fasta file to parse standardize
  --db-path DB_PATH     path of the GeenuFF database
  --log-file LOG_FILE   output path for import log (default basedir/output/import.log)

Possible genome attributes::
  --species SPECIES     name of the species
  --accession ACCESSION
  --version VERSION     genome version
  --acquired-from ACQUIRED_FROM
						genome source

## Proposed changes ## 
### In general ###

* rename to import.py
* remove basedir functionality as it is probably a bit to complicated for new users

### New CLI ###

usage: import.py [-h] [--config-file CONFIG_FILE] --gff3 GFF3 --fasta FASTA --db-path DB_PATH [--log-file LOG_FILE] [--replace-db] --species SPECIES [--accession ACCESSION] [--version VERSION] [--acquired-from ACQUIRED_FROM]

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE  config in form of a YAML file with lower priority than parameters given on the command line
  --replace-db          whether to override a GeenuFF database found at the default location or at the location of --db_path
  --log-file LOG_FILE   output path for the import log (default is current directory)

Possible genome attributes:
  --species SPECIES     the name of the species
  --accession ACCESSION more specific species ID
  --version VERSION     the genome version
  --acquired-from ACQUIRED_FROM the genome source
