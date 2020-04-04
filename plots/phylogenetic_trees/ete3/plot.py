#!/usr/bin/env python3
import numpy as np
import ete3
from ete3 import ClusterTree, ProfileFace, ArrayTable, TreeStyle, AttrFace
from ete3.treeview.faces import add_face_to_node

# tree = ete3.PhyloTree("all_species.tre", sp_naming_function=lambda node: node.name)
data = ArrayTable("results.array")
ct = ete3.ClusterTree("all_species.tre", data)
data_max = np.max(ct.arraytable.matrix)
data_min = np.min(ct.arraytable.matrix)

def mylayout(node):
    if node.is_leaf():
        profile_face = ProfileFace(data_max, data_min, 0.0, 100, 14, "heatmap")
        ete3.treeview.faces.add_face_to_node(profile_face, node, 0, aligned=True)

ts = TreeStyle()
ts.layout_fn = mylayout
ct.show(tree_style=ts)
