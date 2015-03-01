# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 22:34:42 2014

@author: dexter pratt
"""
import ndexClient as nc
import belUtil as util

# open a connection to drh's account on test
myNdex = nc.Ndex("http://test.ndexbio.org", "drh", "drh")
#myNet = myNdex.getNetworkByEdges("63177354-433b-11e4-9369-90b11c72aefa", 0 , 25)

# query the large corpus for a subnetwork
myNet = myNdex.getNeighborhood('1ada3330-45cc-11e4-a9e5-000c29873918', 'BRAF RAF1')

originalBELNetwork = util.BELNetwork(myNet)

originalBELNetwork.writeSummary()

newBEL = util.BELNetwork()

# make a filtered copy
newBEL.copyNetwork(originalBELNetwork, {"species": "9606"})

newBEL.writeSummary()

# update provenance






# < do a layout?>

# export the network back to JSON

# write KAML network back to NDEx

