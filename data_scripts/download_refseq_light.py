"""automate download of only what we need from refseq and organization to match phytozome"""
import sys

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
            for d in [self.working, self.latest, self.version, self.current]:
                os.makedirs(d)

    @property
    def working(self):
        return ospj(self.out_dir, 'working')

    @property
    def latest(self):
        return ospj(self.working, 'latest')

    @property
    def current(self):
        """the _other_ ~equivalent to latest directory that some species have"""
        return ospj(self.working, 'current')

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

    def get_version_from_latest(self, preferred_version):
        with open(ospj(self.latest, 'index.html')) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        links = soup.find_all('a')
        if preferred_version is not None:
            links = [link for link in links if link['href'].find(preferred_version) > -1]
        assert len(links) == 1, f'len(links) != 1, instead {len(links)}; {links}\n'
        out = links[0]["href"] + '/'
        # parse out just the last version bit and store
        self.found_version = leaf_path(out)
        return out

    def get_version_from_current(self, preferred_version):
        with open(ospj(self.current, 'index.html')) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        links = soup.find_all('a')
        # directory only (skip XML and readme file)
        links = [link for link in links if link['href'].endswith('/')]
        if preferred_version is not None:
            links = [link for link in links if link['href'].find(preferred_version) > -1]
        assert len(links) == 1, f'len(links) != 1, instead {len(links)}; {links}'
        out = links[0]["href"]
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
                assert path_checksums is None, f"path_checksums already set to {path_checksums} in {self.out_dir}\n"
                path_checksums = pth
            elif pth.endswith('.gff.gz'):
                assert path_genome_gff is None, f"path_genome_gff already set to {path_genome_gff} in {self.out_dir}\n"
                path_genome_gff = pth
            elif pth.endswith('genomic.fna.gz') and pth.find('from_genomic') == -1:
                assert path_genome_fa is None, f"path_genome_fa already set to {path_genome_fa} in {self.out_dir}\n"
                path_genome_fa = pth
        for pth in [path_genome_gff, path_genome_fa, path_checksums]:
            assert pth is not None, f"path still unset in [path_genome_gff, path_genome_fa, path_checksums], " \
                                    f"{[path_genome_gff, path_genome_fa, path_checksums]}\n"
        return path_genome_fa, path_genome_gff, path_checksums


@click.group()
def cli():
    pass


@cli.command()
@click.option('-s', '--species', required=True)
@click.option('-b', '--base-path', required=True, help='main download path, e.g. '
                                                       'ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/')
@click.option('--out-dir', default='./')
@click.option('--overwrite/--no-overwrite', default=False)
@click.option('--preferred-version')
def get(species, base_path, out_dir, overwrite, preferred_version):
    dl_one(species, base_path, out_dir, overwrite, preferred_version)


@cli.command()
@click.option('-b', '--base-path', required=True, help='main download path, e.g. '
                                                       'ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/')
@click.option('--out-dir', default='./')
@click.option('--overwrite/--no-overwrite', default=False)
@click.option('--resume-after', help='exact refseq name of last species to complete successfully, all species up to '
                                     'and including this will be skipped, if specified')
def get_all(base_path, out_dir, overwrite, resume_after):
    if resume_after is None:
        ready2add = True
    else:
        ready2add = False
    # prep directory, todo, don't fail on empty
    if os.path.exists(out_dir) and overwrite:
        print(f'Not implementing auto-deletion here for "{out_dir}", delete it yourself!', file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    ftp_pfx = 'ftp://'
    target = f'{ftp_pfx}{base_path}/'
    subprocess.run(['wget', target])
    # parse out all species names
    with open('index.html') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    links = soup.find_all('a')
    species = []

    for link in links:
        href = link['href']
        if href.endswith('/'):
            sp = leaf_path(href)
            if ready2add:
                species.append(sp)
            if sp == resume_after:
                ready2add = True

    # clean up for later
    if resume_after is not None:
        os.remove(ospj(out_dir, 'index.html'))
    shutil.move('index.html', out_dir)

    # descriptive error if accidentally skipping everything
    if not ready2add:
        print(f'--resume-after set to {resume_after}, but was not found, skipping all species', file=sys.stderr)
        sys.exit(1)

    # and go go species fetcher!
    for a_sp in species:
        try:
            dl_one(a_sp, base_path, out_dir, overwrite)
        except FileNotFoundError as e:
            known_error_log(a_sp, out_dir, e)
        except AssertionError as e:
            known_error_log(a_sp, out_dir, e)
        # todo, maybe auto-detect and log suppressed genomes differently?
        # where 'suppressed' is the only folder inside all_assembly_versions/


def known_error_log(species, out_dir, e):
    with open(ospj(out_dir, 'download.log'), 'a') as f:
        f.write(f"ERROR encountered downloading {species}\n")
        f.write(str(e) + '\n')


def dl_one(species, base_path, out_dir, overwrite, preferred_version=None):
    ftp_pfx = 'ftp://'
    dh = DirHolder(ospj(out_dir, species), overwrite=overwrite)
    # download latest contents by species name, so we can get the version name
    # most species indicate the latest and greatest assembly version by putting it in latest_assembly_versions
    target = f'{ftp_pfx}{base_path}{species}/latest_assembly_versions/'
    subprocess.run(['wget', target], cwd=dh.latest)
    try:
        datadir = dh.get_version_from_latest(preferred_version)
    except FileNotFoundError:
        # a handful of species instead indicate the latest and greatest version as follows
        target = f'{ftp_pfx}{base_path}{species}/annotation_releases/current/'
        subprocess.run(['wget', target], cwd=dh.current)
        # the contents of the resulting index.html are also slightly different; so a different parsing function is used
        datadir = dh.get_version_from_current(preferred_version)
    # download version contents by version name, so we can get the file names
    subprocess.run(['wget', datadir], cwd=dh.version)
    paths = dh.get_genome_paths_from_version()
    genome_fa, genome_gff, checksums = [leaf_path(pth) for pth in paths]

    # download actual data
    for pth in paths:
        subprocess.run(['wget', pth])

    # check data made it intact
    oks = subprocess.check_output(['md5sum', '-c', checksums, '--ignore-missing']).decode('utf8').split('\n')
    oks = [ok for ok in oks if ok]  # skip empty line
    error = None
    try:
        for ok in oks:
            assert ok.endswith('OK')
        assert len(oks) == 2, f'not the 2 expected files but {len(oks)} instead: {oks}'
    except AssertionError as e:
        # catch this, so that files are still moved to their target location below
        # thus they are available for debugging, but will not cause trouble for later downloads
        # e.g. by resulting in md5checksums.txt.1 !
        error = e
    # move data to project's standard structure
    dh.setup_output()
    shutil.move(checksums, dh.out_version)
    # move and rename fna -> fa and gff -> gff3
    shutil.move(genome_fa, ospj(dh.out_assembly, re.sub('\\.fna\\.gz', '.fa.gz', genome_fa)))
    shutil.move(genome_gff, ospj(dh.out_annotation, re.sub('\\.gff\\.gz', '.gff3.gz', genome_gff)))
    if error is not None:
        raise error


if __name__ == "__main__":
    cli()
