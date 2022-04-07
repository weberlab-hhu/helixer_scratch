from only_is_a import obo_to_nodes_n_edges, get_all_is_as
import sys
import re


DIGITS = [d for d in '0123456789']


def to_var(so_name):
    so_name = so_name.upper()
    if so_name[0] in DIGITS:
        so_name = '_' + so_name
    so_name = re.sub('-', '_', so_name)
    return so_name


def pythonize_features(features, name, id_to_name, f):
    seen = {}
    all_so_vars = []
    for so_id in features:
        so_name = id_to_name[so_id]
        so_name_var = to_var(so_name)
        if so_name_var in seen:
            seen[so_name_var] += 1
            so_name_var += str(seen[so_name_var])
            assert so_name_var not in seen
        else:
            seen[so_name_var] = 0
        all_so_vars.append(so_name_var)
        line = f'{so_name_var} = "{so_name}"\n'
        f.write(line)
    f.write('\n')
    enum_decl = f'{name} = make_enum('
    f.write(f'{enum_decl}"{name}",\n')
    for so_var in all_so_vars:
        pad = ' ' * len(enum_decl)
        f.write(f'{pad}{so_var},\n')
    f.write(')\n\n')


def main():
    nodes, edges = obo_to_nodes_n_edges('so_2_5_3.obo')
    id_to_name = {x.id_: x.name for x in nodes.values()}
    name_to_id = {x.name: x.id_ for x in nodes.values()}

    # sequence_features
    seq_features = set()
    get_all_is_as(edges, 'SO:0000110', seq_features)
    seq_features.add('SO:0000110')
    print(f'All of sequence ontology 2_5_3 --> Nodes {len(nodes)}, Edges {len(edges)}', file=sys.stderr)
    e_count = sum([len(es) for id_, es in edges.items() if id_ in seq_features])
    print(f'predecessors / is a sequence_feature/SO:0000110 --> Nodes {len(seq_features)}, Edges {e_count}',
          file=sys.stderr)
    print('exporting the latter to so.py', file=sys.stderr)

    # gene / super_locus
    sl_features = set()
    get_all_is_as(edges, name_to_id['gene'], sl_features)

    # transcripts
    transcript_features = set()
    get_all_is_as(edges, name_to_id['transcript'], transcript_features)

    # exon
    exon_features = set()
    get_all_is_as(edges, name_to_id['exon'], exon_features)

    # CDS
    cds_features = set()
    get_all_is_as(edges, name_to_id['CDS'], cds_features)
    lengths = [len(x) for x in [sl_features, transcript_features, exon_features, cds_features]]
    print(f'further exporting gene, transcript, exon, and CDS features with none lengths of {lengths}, respectively')

    with open('so.py', 'w') as f:
        f.write('from .helpers import make_enum\n\n')
        f.write("_so_version = '2.5.3'\n\n")
        pythonize_features(seq_features, 'SOSequenceFeatures', id_to_name, f)
        pythonize_features(sl_features, 'SOSuperLocusFeatures', id_to_name, f)
        pythonize_features(transcript_features, 'SOTranscriptFeatures', id_to_name, f)
        pythonize_features(exon_features, 'SOExonFeatures', id_to_name, f)
        pythonize_features(cds_features, 'SOCDSFeatures', id_to_name, f)


if __name__ == '__main__':
    main()
