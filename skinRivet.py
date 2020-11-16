'''
Very fast and simple rivet-like solution for attaching objects to skinned meshes in Autodesk Maya
author: Marin Petrov marin@hey.com
'''


import maya.cmds as mc
sel = mc.ls(sl=True)

driver = sel[0].split('.')[0]

# find the shape of the selected vertex
shapes = mc.listRelatives(driver)
if not shapes:
    raise RuntimeError("For some reason there were no shapes found on {}".format(sel[0]))

# find the skinCluster
skin_cluster = mc.listConnections(shapes[0], s=True, d=True, type="skinCluster")[0]

# get all influences of the selected vertex
influences = mc.skinPercent(skin_cluster, sel[0], q=True, transform=None)
inf_lookup = {}
for i in influences:
    inf_lookup[i] = mc.skinPercent(skin_cluster, sel[0], transform=i, q=True)

# create a parentConstraint from the influences to the driven object
pc = mc.parentConstraint(influences, sel[-1], mo=True)[0]

# set the weights on the constraint
for idx, inf in enumerate(influences):
    mc.setAttr('{}.{}W{}'.format(pc, inf, idx), inf_lookup[inf])
