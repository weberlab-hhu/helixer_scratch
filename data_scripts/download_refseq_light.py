"""automate download of only what we need from refseq and organization to match phytozome"""

import click
import subprocess
import os
import shutil
from bs4 import BeautifulSoup
import re


ospj = os.path.join


def leaf_path(pth):
    # remove trailing slashes
    while pth.endswith('/'):
        pth = pth[:-1]
    # remove all parental info
    pth = re.sub('.*/', '', pth)
    return pth


class DirHolder:
    def __init__(self, out_dir, overwrite=False):
        self.out_dir = out_dir
        self.found_version = None
        self.overwrite = overwrite
        # clean previous
        if os.path.exists(self.working) and overwrite:
            shutil.rmtree(self.working)
        if not os.path.exists(self.working):
            # setup
            for d in [self.working, self.latest, self.version]:
                os.makedirs(d)

    @property
    def working(self):
        return ospj(self.out_dir, 'working')

    @property
    def latest(self):
        return ospj(self.working, 'latest')

    @property
    def version(self):
        return ospj(self.working, 'version')

    @property
    def out_version(self):
        assert self.found_version is not None
        return ospj(self.out_dir, self.found_version)

    @property
    def out_assembly(self):
        return ospj(self.out_version, 'assembly')

    @property
    def out_annotation(self):
        return ospj(self.out_version, 'annotation')

    def setup_output(self):
        # clean previous
        if os.path.exists(self.out_version) and self.overwrite:
            shutil.rmtree(self.out_version)
        if not os.path.exists(self.out_version):
            # setup
            for d in [self.out_version, self.out_assembly, self.out_annotation]:
                os.makedirs(d)

    def get_version_from_latest(self):
        with open(ospj(self.latest, 'index.html')) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        links = soup.find_all('a')
        assert len(links) == 1, f'len(links) != 1, instead {len(links)}'
        out = links[0]["href"] + '/'
        # parse out just the last version bit and store
        self.found_version = leaf_path(out)
        return out

    def get_genome_paths_from_version(self):
        path_genome_fa = None
        path_genome_gff = None
        path_checksums = None
        with open(ospj(self.version, 'index.html')) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        links = soup.find_all('a')
        for link in links:
            pth = link['href']
            if pth.endswith('md5checksums.txt'):
                assert path_checksums is None, f"path_checksums already set to {path_checksums} in {self.out_dir}"
                path_checksums = pth
            elif pth.endswith('.gff.gz'):
                assert path_genome_gff is None, f"path_genome_gff already set to {path_genome_gff} in {self.out_dir}"
                path_genome_gff = pth
            elif pth.endswith('genomic.fna.gz') and pth.find('from_genomic') == -1:
                assert path_genome_fa is None, f"path_genome_fa already set to {path_genome_fa} in {self.out_dir}"
                path_genome_fa = pth
        for pth in [path_genome_gff, path_genome_fa, path_checksums]:
            assert pth is not None, f"path still unset in [path_genome_gff, path_genome_fa, path_checksums], " \
                                    f"{[path_genome_gff, path_genome_fa, path_checksums]}"
        return path_genome_fa, path_genome_gff, path_checksums


@click.group()
def cli():
    pass


@cli.command()
@click.option('-s', '--species', required=True)
@click.option('-b', '--base-path', required=True)
@click.option('--overwrite/--no-overwrite', default=False)
def get(species, base_path, overwrite):
    dl_one(species, base_path, overwrite)


def dl_one(species, base_path, overwrite):
    ftp_pfx = 'ftp://'
    #basepath = "ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/"
    #species = "Seriola_lalandi"
    dh = DirHolder(species)
    target = f'{ftp_pfx}{base_path}{species}/latest_assembly_versions/'
    subprocess.run(['wget', target], cwd=dh.latest)
    datadir = dh.get_version_from_latest()
    subprocess.run(['wget', datadir], cwd=dh.version)
    paths = dh.get_genome_paths_from_version()
    genome_fa, genome_gff, checksums = [leaf_path(pth) for pth in paths]

    # download actual data
    for pth in paths:
        subprocess.run(['wget', pth])

    # check data made it intact
    oks = subprocess.check_output(['md5sum', '-c', checksums, '--ignore-missing']).decode('utf8').split('\n')
    oks = [ok for ok in oks if ok]  # skip empty line
    for ok in oks:
        assert ok.endswith('OK')
    assert len(oks) == 2, f'not the 2 expected files but {len(oks)} instead: {oks}'

    # move data to project's standard structure
    dh.setup_output()
    shutil.move(checksums, dh.out_version)
    # move and rename fna -> fa and gff -> gff3
    shutil.move(genome_fa, ospj(dh.out_assembly, re.sub('\\.fna\\.gz', '.fa.gz', genome_fa)))
    shutil.move(genome_gff, ospj(dh.out_annotation, re.sub('\\.gff\\.gz', '.gff3.gz', genome_gff)))


if __name__ == "__main__":
    cli()
