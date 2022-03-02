import click
import subprocess
import os
import shutil
from bs4 import BeautifulSoup


ospj = os.path.join

class DirHolder:
    def __init__(self, out_dir):
        self.out_dir = out_dir
        # clean previous
        if os.path.exists(self.working):
            shutil.rmtree(self.working)
        # setup
        for d in [self.working, self.latest, self.version]:
            os.path.makedirs(d)

    @property
    def working(self):
        return ospj(self.out_dir, 'working')

    @property
    def latest(self):
        return ospj(self.out_dir, 'latest')

    @property
    def version(self):
        return ospj(self.out_dir, 'version')
    

    def get_version_from_latest(self):
        with open(ospj(self.latest, 'index.html')) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        links = soup.find_all('a')
        assert len(links) == 1, f'len(links) != 1, instead {len(links)}'
        return links[0]["href"] + '/'

    def get_genome_fa_from_version(self):
        pass

    def get_genome_gff_from_version(self):
        pass


@click.command()
def cli():
    ftp_pfx = 'ftp://'
    basepath = "ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/"
    species = "Seriola_lalandi"
    dh = DirHolder(species)
    target = f'{ftp_pfx}{basepath}{species}/latest_assembly_versions/'
    subprocess.run(['wget', target], cwd=dh.latest)
    genome_version = dh.get_version_from_latest()
    datadir = f'{target}/{genome_version}/'
    subprocess.run(['wget', target], cwd=dh.version)


if __name__ == "__main__":
    cli()
