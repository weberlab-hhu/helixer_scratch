import pandas as pd
import argparse


class BlastLine:
    def __init__(self, line):
        line = line.rstrip()
        sline = line.split('\t')
        self.bitscore = float(sline[11])
        self.length = float(sline[3])
        self.pident = float(sline[2])
        self.qseqid = sline[0]
        self.oriseq = self.qseqid.split(':')[0]
        self.sseqid = sline[1]
        self.subj_class = self.sseqid[:self.sseqid.find('::')]
        assert self.subj_class in ["nucl", "mt", "pt"]

    def as_list(self):
        return [self.oriseq, self.qseqid, self.subj_class, self.sseqid, self.pident, self.length, self.bitscore]

    def __repr__(self):
        return '\t'.join([str(x) for x in self.as_list()])


def best_per_query(ori_grp):
    """breaks up blast lines objs by those from a subsequence (blast query); assumes sorted"""
    iter_grp = iter(ori_grp)
    previous = next(iter_grp)
    yield previous
    for current in iter_grp:
        if current.qseqid != previous.qseqid:
            yield current
        previous = current


def split_by_original_sequence(filein):
    """breaks up blast results to those from original sequence (prior to split_genome.py)"""
    with open(filein) as f:
        previous = BlastLine(next(f))
        oriseq_group = [previous]
        for line in f:
            current = BlastLine(line)
            if previous.oriseq != current.oriseq:
                yield oriseq_group
                oriseq_group = []
            oriseq_group.append(current)
            previous = current
        yield oriseq_group


def stats_for_original_sequence(best_ori_grp, targ_subj_class="nucl"):
    """calculates best & median top blast hit stats (%id, len, bitscore) for all subseqs in a sequence"""
    assert targ_subj_class in ["nucl", "pt", "mt"]
    df = pd.DataFrame(best_ori_grp)
    df = df.loc[df.loc[:, 2] == targ_subj_class, :]
    df = df.sort_values(by=6, ascending=False)
    if df.shape[0]:
        best = df.iloc[0, [4, 5, 6]].to_list()
        total_len = sum(df.loc[:, 5])
        total_bitscore = sum(df.loc[:, 6])
        weighted_pident = sum(df.loc[:, 4] * df.loc[:, 5]) / total_len
        # single best hit [pident, len, bitscore] + aggregated [pident, len, bitscore, count]
        organized = best + [weighted_pident, total_len, total_bitscore, df.shape[0]]
    else:
        organized = [None, None, None, None, None, None, 0]

    return {"besthit_pident": organized[0],
            "besthit_length": organized[1],
            "besthit_bitscore": organized[2],
            "aggregated_pident": organized[3],
            "aggregated_length": organized[4],
            "aggregated_bitscore": organized[5],
            "count": organized[6]}


def main(filein, fileout):
    # '/mnt/data/ali/nemicolopterus/ali/Ankylosaurus/Core_projects/Puma/data/Phytozome_dump/Phytozome/ready/organellar_labelling/species/Creinhardtii/split-known.m8'
    out = []
    for grp in split_by_original_sequence(filein):
        besties = list(best_per_query(grp))
        print(grp[0].oriseq, len(grp), len(besties))
        for tsc in ["nucl", "pt", "mt"]:
            stats = {"query": grp[0].oriseq,
                     "subject": tsc}
            stats.update(stats_for_original_sequence([x.as_list() for x in besties], targ_subj_class=tsc))
            out.append(stats)

    with open(fileout, 'w') as f:
        pd.DataFrame(out).to_csv(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_m8', required=True,
                        help="blast output file (m8 / outfmt 6) of split query genome to annotated ref")
    parser.add_argument('-o', '--out', required=True, help='output csv')
    args = parser.parse_args()
    main(args.input_m8, args.out)