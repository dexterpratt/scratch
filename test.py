# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 22:34:42 2014

@author: dexter pratt
"""
import ndexClient as nc
import belUtil as util

# open a connection to drh's account on test
myNdex = nc.Ndex("http://test.ndexbio.org", username="drh", password="drh")

prod = nc.Ndex("http://www.ndexbio.org", username="dexterpratt", password="carbluegreen")

#myNet = myNdex.getNetworkByEdges("63177354-433b-11e4-9369-90b11c72aefa", 0 , 25)

#myNet = myNdex.getCompleteNetwork('02221e14-6ae6-11e4-b14b-000c29873918')

# 1b0d7c38-a10e-11e4-b590-000c29873918
# query the large corpus for a subnetwork
myNet = myNdex.getNeighborhood('1b0d7c38-a10e-11e4-b590-000c29873918', 'nras')

bn = util.BELNetwork(myNet)

filterEdges = []
for edgeId, edge in bn.getEdges().iteritems():
    if util.hasProperty(edge, "species", "9606"):
        print "keeping edge " + edgeId
    else:
        print "removing " + edgeId
        filterEdges.append(edgeId)

for edgeId in filterEdges:
    bn.removeEdge(edgeId)

bn.writeSummary()

bn.setName("nras signaling, human")

myNdex.saveNewNetwork(bn.network)



##newBEL = util.BELNetwork()

# make a filtered copy
##newBEL.copyNetwork(originalBELNetwork, {"species": "9606"})

##newBEL.writeSummary()

# update provenance






# < do a layout?>

# export the network back to JSON

# write KAML network back to NDEx

