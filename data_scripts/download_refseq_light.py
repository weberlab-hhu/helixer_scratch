import click
import subprocess
import os
from bs4 import BeautifulSoup


@click.command()
def cli():
    ftp_pfx = 'ftp://'
    basepath = "ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/"
    species = "Seriola_lalandi"
    workingdir = os.path.join(species, 'working')
    if not os.path.exists(workingdir):
        os.makedirs(workingdir)
    target = f'{ftp_pfx}{basepath}{species}/latest_assembly_versions/'
    #subprocess.run(['wget', target], cwd=workingdir)
    with open(os.path.join(workingdir, 'index.html')) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    print(soup.find_all('a'))


if __name__ == "__main__":
    cli()
