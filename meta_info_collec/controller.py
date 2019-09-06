"""simplifies start of various metainfo steps for new genomes"""
import glob
import logging
import subprocess

logging.basicConfig(level=logging.INFO,
                    filename="log.log")


class Job(object):
    def __init__(self, species, direc='test'):
        self.name = None
        self.species = species
        self.direc = direc
        self.requires = []
        self.outputs = []

    @property
    def sp_dir(self):
        return '{}/{}/'.format(self.direc, self.species)

    def prep(self):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def check_input_files(self):
        for file in self.requires:
            assert glob.glob(file), "missing {}".format(file)
        logging.info("all input files found for job {} on {} in {}".format(self.name, self.species, self.direc))


class BuscoGenome(Job):
    def __init__(self, species, direc='test'):
        super().__init__(species, direc)
        self.name = "busco_genome"
        self.requires = ['{}*/assembly/*.fa'.format(self.sp_dir)]


class PrepGenome(Job):
    def __init__(self, species, direc="test"):
        super().__init__(species, direc)
        self.name = "prep_genome"
        self.requires = ['{}*/assembly/*.fa*'.format(self.sp_dir)]

    def prep(self):
        pass

    def run(self):
        # gunzip if necessary
        gzipped = '{}*/assembly/*.fa.gz'.format(self.sp_dir)

        gpath = glob.glob(gzipped)
        assert len(gpath) == 1
        if glob.glob(gzipped):
            s = subprocess.check_output(["zcat", gpath[0], '>', ])
            print(s)
        logging.info("ran")

def main():
    species = "Alyrata"
    direc = "test"
    job = PrepGenome(species, direc)
    job.check_input_files()
    job.run()

if __name__ == '__main__':
    main()