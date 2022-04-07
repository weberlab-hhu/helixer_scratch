import obonet
import networkx
import sys
import re

graph = obonet.read_obo('so_2_5_3.obo')
print(networkx.descendants(graph, 'SO:0000110'))
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
print(id_to_name['SO:0000110'])
for u in graph:
    if graph.has_predecessor('SO:0000110', u):
        print(u)
#print(np.sum([graph.has_predecessor(u, 'SO:0000110') for u in graph]))
seq_features = set()


def get_all_predecessors(graph, so_id):
    for p in graph.predecessors(so_id):
        seq_features.add(p)
        get_all_predecessors(graph, p)

get_all_predecessors(graph, 'SO:0000110')
print('All of sequence ontology 2_5_3 -->', graph, file=sys.stderr)
print('predecoessors / is a sequence_feature/SO:0000110 -->', graph.subgraph(seq_features), file=sys.stderr)
print('exporting the latter to so.py', file=sys.stderr)

DIGITS = [d for d in '0123456789']

def to_var(so_name):
    so_name = so_name.upper()
    if so_name[0] in DIGITS:
        so_name = '_' + so_name
    so_name = re.sub('-', '_', so_name)
    return so_name

seen = {}
with open('so.py', 'w') as f:
    f.write("_so_version = '2.5.3'\n")
    all_so_vars = []
    for so_id in seq_features:
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
    f.write('SOSequenceFeatures = make_enum("SOSequenceFeatures",\n')
    for so_var in all_so_vars:
        f.write(f'                               {so_var},\n')
    f.write(')')

#print(seq_features)

#for p in [x for x in graph.predecessors('SO:0000110')]:
#    print(list(graph.predecessors(p)))