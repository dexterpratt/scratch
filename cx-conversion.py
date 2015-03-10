# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 22:34:42 2014

@author: dexter pratt
"""
import ndexClient as nc
import belUtil as util
import json
import sys

# open a connection to drh's account on test
myNdex = nc.Ndex("http://test.ndexbio.org", username="drh", password="drh")

#prod = nc.Ndex("http://www.ndexbio.org", username="dexterpratt", password="carbluegreen")

#myNet = myNdex.getNetworkByEdges("63177354-433b-11e4-9369-90b11c72aefa", 0 , 25)

#myNet = myNdex.getCompleteNetwork('02221e14-6ae6-11e4-b14b-000c29873918')

# 1b0d7c38-a10e-11e4-b590-000c29873918
# query the large corpus for a subnetwork
myNet = myNdex.getNeighborhood('1b0d7c38-a10e-11e4-b590-000c29873918', 'nras')

# myProv = myNdex.getProvenanceHistory('1b0d7c38-a10e-11e4-b590-000c29873918')

cx = {}

# print json.dumps(myNet.get("namespaces"), sort_keys=True, indent=4, separators=(',', ': '))


def writeCx(cxData, fileName = None):
    if fileName:
        output = open(fileName, 'w')
    else:
        output = sys.stdout
    jsonData = json.dumps(cxData, indent=4, separators=(',', ': '))
    output.write(jsonData)

def namespacesToLDContext(network):
    namespaces = network.get("namespaces")
    context = {}
    for id, namespace in namespaces.iteritems():
        prefix = namespace.get("prefix")
        uri = namespace.get("uri")
        # print " prefix = " + prefix + " uri = " + uri
        if prefix and uri:
            context[prefix] = uri
    return context

def blankNodeId(id):
    return "_" + str(id)

def nodesToNodes(network):
    nodesAspect = []
    for id in network.get("nodes"):
        nodesAspect.append({"@id" : blankNodeId(id)})
    return nodesAspect

def edgesToEdges(network):
    edgesAspect = []
    for id, edge in network.get("edges").iteritems():
        newEdge = {"@id" : blankNodeId(id),
                    "source" : blankNodeId(edge.get("subjectId")),
                    "target" : blankNodeId(edge.get("objectId"))
        }
        edgesAspect.append(newEdge)
    return edgesAspect

def createEdgeIdentityAspect(network):
    identityAspect = []
    for id, edge in network.get("edges").iteritems():
        predicate = str(edge.get("predicateId"))
        edgeIdentity = {"edge" : blankNodeId(id),
                        "relationship" : getBaseTerm(network, predicate)}
        identityAspect.append(edgeIdentity)
    return identityAspect

def getBaseTerm(network, idString):
    baseTerms = network.get("baseTerms")
    if baseTerms:
        term = baseTerms.get(idString)
        name = term.get("name")
        namespaceIdString = str(term.get("namespaceId"))
        prefix = getNamespacePrefix(network, namespaceIdString)
        return prefix + ":" + name
    return False

def getNamespacePrefix(network, namespaceIdString):
    namespaces = network.get("namespaces")
    if namespaces:
        namespace = namespaces.get(namespaceIdString)
        if namespace:
            return namespace.get("prefix")
    return False

def createFunctionTermAspect(network):
    functionTermBlankNodeIds = []
    functionTermAspect = []
    sourceFunctionTerms = network.get("functionTerms")
    if sourceFunctionTerms:
        for id, sft in sourceFunctionTerms.iteritems():
            resolveFunctionTerm(network, str(id), functionTermBlankNodeIds, functionTermAspect)
    return functionTermAspect

def resolveTerm(network, idString, functionTermBlankNodeIds, functionTermAspect):
    term = getBaseTerm(idString)
    if term:
        return term
    term = resolveFunctionTerm(network, idString, functionTermBlankNodeIds, functionTermAspect)
    return term

def resolveFunctionTerm(network, idString, functionTermBlankNodeIds, functionTermAspect):

    functionTermId = functionTermBlankNodeIds.get(idString)
    if functionTermId:
        return functionTermId

    # if it is NOT already made, then make it!
    functionTermId = blankNodeId(idString)
    functionTermBlankNodeIds[idString] = functionTermId
    sourceFunctionTerms = network.get("functionTerms")
    sft = sourceFunctionTerms.get(idString)

    functionBaseTermId = str(sft.get("functionTerm"))
    functionBaseTerm = getBaseTerm(network, functionBaseTermId);
    functionTerm = {"@id" : functionTermId}
    if functionBaseTerm:
        functionTerm["function"] = functionBaseTerm
        parameters = []
        for parameterId in sft.get("parameterIds"):
            term = resolveTerm(network, str(parameterId), functionTermBlankNodeIds, functionTermAspect)
            parameters.append(term)
        functionTermAspect.append(functionTerm)
    return functionTermId

def createNodeIdentityAspect(network):
    return {"status" : "TBD"}

def createCitationsAspect(network):
    sourceCitations = network.get("citations")
    citations = []

    for sc in sourceCitations.values():
        sc["nodes"] = []
        sc["edges"] = []

    for edgeId, edge in network.get("edges").iteritems():
        citationIds = edge.get("citationIds")
        if citationIds:
            for citationId in citationIds:
                citation = sourceCitations.get(str(citationId))
                citationEdges = citation.get("edges")
                citationEdges.append(blankNodeId(edgeId))

    for id, sc in sourceCitations.iteritems():
        citation = {"@id" : blankNodeId(id),
                    "edges" : sc.get("edges") ,
                    "nodes" : sc.get("nodes") ,
                    "type" : sc.get("type")
            }
        citations.append(citation)

    return citations

def createSupportsAspect(network):
    sourceSupports = network.get("supports")
    supports = []

    for ss in sourceSupports.values():
        ss["nodes"] = []
        ss["edges"] = []

    for edgeId, edge in network.get("edges").iteritems():
        supportIds = edge.get("supportIds")
        if supportIds:
            for supportId in supportIds:
                support = sourceSupports.get(str(supportId))
                supportEdges = support.get("edges")
                supportEdges.append(blankNodeId(edgeId))

    for id, ss in sourceSupports.iteritems():
        support = {"@id" : blankNodeId(id),
                   "edges" : ss.get("edges") ,
                   "nodes" : ss.get("nodes") ,
                   "text" : ss.get("text"),
                   }
        citationId = ss.get("citationId")
        if citationId:
            support["citation"] = blankNodeId(citationId)

        supports.append(support)

    return supports

def createProvenanceHistoryAspect(network):
    return {"status" : "TBD"}

cx["@context"] = namespacesToLDContext(myNet)
cx["nodes"] = nodesToNodes(myNet)
cx["edges"] = edgesToEdges(myNet)
cx["edgeIdentities"] = createEdgeIdentityAspect(myNet)
cx["nodeIdentities"] = createNodeIdentityAspect(myNet)
cx["citations"] = createCitationsAspect(myNet)
cx["supports"] = createSupportsAspect(myNet)
cx["provenanceHistory"] = createProvenanceHistoryAspect(myNet)

writeCx(cx, "cx-example.json")