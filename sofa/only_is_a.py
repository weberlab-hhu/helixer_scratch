from collections import defaultdict


class Node:
    def __init__(self, lines):
        self.id_ = None
        self.name = None
        self.is_a = []
        self.other_tags = []
        self._init_frm_lines(lines)

    def _init_frm_lines(self, lines):
        ids = []
        names = []
        is_as = []
        for line in lines:
            line = line.rstrip()
            sline = line.split(':')
            tag = sline[0]
            val = ':'.join(sline[1:])
            val = val.lstrip()
            if tag == 'id':
                ids.append(val)
            elif tag == "name":
                names.append(val)
            elif tag == 'is_a':
                self.is_a.append(val)
            else:
                self.other_tags.append((tag, val))
        assert len(ids) == 1, lines
        self.id_ = ids[0]
        assert len(names) == 1
        self.name = names[0]

    @property
    def is_a_ids(self):
        out = []
        for item in self.is_a:
            id_, name = item.split('!')
            out.append(id_.rstrip().lstrip())
        return out


def obo_gen(f):
    first_term = False
    lines = []
    for line in f:
        line = line.rstrip()
        if line == '[Typedef]':
            break
        if line == '[Term]':
            if first_term:
                yield lines
            else:
                first_term = True
            lines = []
        else:
            if line:  # skip empty lines
                lines.append(line)
    yield lines


def obo_to_nodes_n_edges(filename):
    nodes = {}
    with open(filename) as f:
        for lines in obo_gen(f):
            node = Node(lines)
            nodes[node.id_] = node

    edges = defaultdict(list)
    for node_id in nodes:
        node = nodes[node_id]
        for ia in node.is_a_ids:
            edges[ia].append(node.id_)
    return nodes, edges


def get_all_is_as(edges, id_, output_set):
    output_set.add(id_)
    for d in edges[id_]:
        get_all_is_as(edges, d, output_set)


#ids_to_names = {x.id_: x.name for x in nodes.values()}
#names_to_ids = {x.name: x.id_ for x in nodes.values()}
#
#sl_level = set()
#get_all_is_as(downs, names_to_ids['transcript'], sl_level)
#for item in sl_level:
#    print(ids_to_names[item])