# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:10:59 2014

@author: Dexter Pratt
"""
import sys
import networkx as nx

# Convert NDEx property graph json to a trivial networkx network
def ndexPropertyGraphNetworkToNetworkX(ndexPropertyGraphNetwork):
        g = nx.MultiDiGraph()
        for node in ndexPropertyGraphNetwork['nodes'].values():
            g.add_node(node['id'])
        for edge in ndexPropertyGraphNetwork['edges'].values():
            g.add_edge(edge['subjectId'], edge['objectId'])
        return g

# This is specific to summarizing a BEL network. 
# Need to generalize
def stripBELPrefixes(input):
    st = input.lower()
    if st.startswith('bel:'):
        return input[4:input.len()]
    elif st.startswith('hgnc:'):
         return input[5:input.len()]
    else:
         return input

# This is BEL specific, since BEL is the only current user of funciton terms
def getFunctionAbbreviation(input):
    st = input.lower()
    fl = stripBELPrefixes(st)
    if fl == "abundance":
        return "a"
    elif fl == "biological_process":
        return "bp"
    elif fl ==  "catalytic_activity":
        return "cat"
    elif fl ==  "complex_abundance":
        return "complex"
    elif fl ==  "pathology":
        return "path"
    elif fl ==  "peptidase_activity":
        return "pep"
    elif fl ==  "protein_abundance":
        return "p"
    elif fl ==  "rna_abundance":
        return "r"
    elif fl ==  "protein_modification":
        return "pmod"
    elif fl ==  "transcriptional_activity":
        return "tscript"
    elif fl ==  "molecular_activity":
        return "act"
    elif fl ==  "degradation":
        return "deg"
    elif fl ==  "kinase_activity":
        return "kin"
    elif fl ==  "substitution":
        return "sub"
    else:
        return fl

class BELNetwork:
    def __init__ (self):
        self.initializeBlankNdexNetwork()
        self.initializeMaps()

    def initializeBlankNdexNetwork(self):
        self.network = {'nodes' : {},
                        'edges' : {},
                        'baseTerms' : {},
                        'functionTerms' : {},
                        'reifiedEdgeTerms' : {},
                        'citations' : {},
                        'supports' : {},
                        'provenance' : {}
        }

    def initializeMaps(self):
        self.supportToEdgeMap = {}
        self.citationToSupportMap = {}
        self.nodeLabelMap = {}
        self.termLabelMap = {}
        self.correspondingElementIdMap = {}

    def initializeCorrespondingElementIdMap(self):
        self.correspondingElementIdMap = {}

    def __init__(self, ndexNetwork):
        self.network = ndexNetwork
        self.initializeMaps()

        for nodeId, node in self.getNodes().iteritems():
            self.nodeLabelMap[int(nodeId)] = self.getNodeLabel(node)

        for edge in self.getEdges().values():
            for supportId in edge['supportIds']:
                support = self.getSupport(supportId)
                if supportId in self.supportToEdgeMap:
                    edgeList = self.supportToEdgeMap[supportId]
                else:
                    edgeList = []
                edgeList.append(edge)
                self.supportToEdgeMap[supportId] = edgeList

        for supportId in self.supportToEdgeMap.keys():
            support = self.getSupport(supportId)
            citationId = support['citationId']
            if citationId in self.citationToSupportMap:
                supportIdList = self.citationToSupportMap[citationId]
            else:
                supportIdList = []
            supportIdList.append(supportId)
            self.citationToSupportMap[citationId] = supportIdList

    #----------------------------------------------------------
    # Basic Element Access
    #----------------------------------------------------------

    def getEdges(self):
         return self.network['edges']

    def getEdge(self, edgeId):
        return self.network["edges"][str(edgeId)]

    def getNodes(self):
        return self.network["nodes"]

    def getNode(self, nodeId):
        return self.network["nodes"][str(nodeId)]

    def getCitations(self):
        return self.network["citations"]

    def getCitation(self, citationId):
        return self.network["citations"][str(citationId)]

    def getSupports(self):
        return self.network["supports"]

    def getSupport(self, supportId):
        return self.network["supports"][str(supportId)]

    def getBaseTerms(self):
        return self.network["baseTerms"]

    def getBaseTerm(self, baseTermId):
        return self.network["baseTerms"][str(baseTermId)]

    def getFunctionTerms(self):
        return self.network['functionTerms']

    def getFunctionTerm(self, functionTermId):
        return self.network["functionTerms"][str(functionTermId)]

    def getReifiedEdgeTerms(self):
        return self.network['reifiedEdgeTerms']

    def getReifiedEdgeTerm(self, reifiedEdgeTermId):
        return self.network["reifiedEdgeTerms"][str(reifiedEdgeTermId)]

    def getNamespaces(self):
        return self.network['namespaces']

    def getNamespace(self, namespaceId):
        return self.network["namespaces"][str(namespaceId)]

    #----------------------------------------------------------
    # Basic Element Creation
    #----------------------------------------------------------

    def nextElementId(self):

    def createEdge(self, sourceId, predicateId, targetId, citationIds, supportIds, properties):
        elementId = self.nextElementId();
        newEdge = {"sourceId"}

    def createNode(self, representsId, citationIds, supportIds, properties):
        elementId = self.nextElementId();

    def createFunctionTerm(self, predicateId, parameterIds):
        elementId = self.nextElementId();

    def createBaseTerm(self, namespaceId, identifier):
        elementId = self.nextElementId();

    def createReifiedEdgeTerm(self, edgeId):
         elementId = self.nextElementId();

    def createCitation(self, text, citationId):

    def createSupport(self, text, citationId):

    #----------------------------------------------------------
    # Copy operations
    #----------------------------------------------------------

    def getCorrespondingElementId(self, sourceId):
        return self.correspondingElementIdMap[str(sourceId)]

    def setCorrespondingElementId(self, sourceId, targetId):
        self.correspondingElementIdMap[str(sourceId), str(targetId)]

    def copyNetwork(self, sourceNetwork, filter):
        self.initializeCorrespondingElementIdMap()

        # edges
        for sourceEdgeId in sourceNetwork.getEdges().keys():
            self.copyEdge(sourceNetwork, sourceEdgeId)

        # nodes
        for sourceNodeId, sourceNode in self.getNodes().iteritems():
            self.copyNode(sourceNetwork, sourceEdgeId)

    # create a new edge in this network based on the source edge
    # skip if we have already copied it
    def copyEdge(self, sourceNetwork, sourceEdgeId):
        edgeId = self.getCorrespondingElementId(sourceEdgeId)
        if edgeId:
            return edgeId
        else:
            sourceEdge = sourceNetwork.getEdge(sourceEdgeId);
            subjectId = self.copyNode(sourceNetwork, sourceEdge["subjectId"])
            predicateId = self.copyBaseTerm(sourceNetwork, sourceEdge["predicateId"])
            objectId = self.copyNode(sourceNetwork, sourceEdge["objectId"])
            citationIds = []
            for sourceCitationId in sourceEdge['citationIds']:
                citationId = self.copyCitation(sourceNetwork, sourceCitationId)
                citationIds.append(citationId)
            supportIds = []
            for sourceSupportId in sourceEdge['supportIds']:
                supportId = self.copySupport(sourceNetwork, sourceSupportId)
                supportIds.append(supportId)
            # skipping properties for now
            properties = []
            edgeId = self.createEdge(subjectId, predicateId, objectId, citationIds, supportIds, properties)
            self.setCorrespondingElementId(sourceEdgeId, edgeId)
            return edgeId


    def copyNode(self, sourceNetwork, sourceNodeId):
        nodeId = self.getCorrespondingElementId(sourceNodeId)
        if nodeId:
            return nodeId
        else:
            sourceNode = sourceNetwork.getNode(sourceNodeId)
            representsId = self.copyTerm(sourceNetwork, sourceNode['represents'])
            #
            # Skip everything else for now !!
            #
            nodeId = self.findNodeIdByRepresentsId(representsId)
            if nodeId == False:
                nodeId = self.createNode(representsId)
            self.setCorrespondingElementId(sourceNodeId, nodeId)
            return nodeId

    def findNodeIdByRepresentsId(self, representsId):
        for nodeId, node in self.getNodes.iteritems():
            if representsId == node["represents"]:
                return nodeId
        return False

    def copyTerm(self, sourceNetwork, sourceTermId):

    def copyFunctionTerm(self, sourceNetwork, sourceTermId):

    def copyBaseTerm(self, sourceNetwork, sourceTermId):

    def copyReifiedEdgeTerm(self, sourceNetwork, sourceTermId):

    def copyCitation(self, sourceNetwork, sourceCitationId):

    def copySupport(self, sourceNetwork, sourceSupportId):

    def copyNamespace(self, sourceNetwork, sourceNamespaceId):

    #----------------------------------------------------------
    # Merge operations
    #----------------------------------------------------------

    def mergeNetwork(self, sourceNetwork, filter):
        return False

    def mergeEdge(self, sourceNetwork, sourceEdgeId):
        # checks to see if there is a matching edge
        targetEdgeId = self.findMatchingEdge(sourceNetwork, sourceEdgeId)
        if targetEdgeId:
            self.mergeEdgeContext(targetEdgeId, sourceNetwork, sourceEdgeId)
        # if no match, simply copy the edge
        else:
            targetEdgeId = self.copyEdge(sourceNetwork, sourceEdgeId)
        return targetEdgeId

    # matching edge
    #   node represents match
    #   edge predicate match
    #       Special case: direct relationships will subsume indirect.
    #   copy citations and supports to target edge
    def findMatchingEdge(self, sourceNetwork, sourceEdgeId):
        sourceEdge = sourceNetwork.getEdge(sourceEdgeId)
        return False

    # add the citations, supports, and properties of the source edge to the target edge
    def mergeEdgeContext(self, targetEdgeId, sourceNetwork, sourceEdgeId):
        return False

    #----------------------------------------------------------
    # Label Methods
    #----------------------------------------------------------

    def getEdgeLabel(self, edge):
        subjectLabel = "missing"
        objectLabel = "missing"
        predicateLabel = "missing"
        subjectId = edge['subjectId']
        objectId = edge['objectId']
        if subjectId in self.nodeLabelMap:
            subjectLabel = self.nodeLabelMap[subjectId]
        if objectId in self.nodeLabelMap:
            objectLabel = self.nodeLabelMap[objectId]
        predicateId = edge['predicateId']
        predicateLabel = stripBELPrefixes(self.getTermLabel(predicateId))
        label = "%s %s %s" % (subjectLabel, predicateLabel, objectLabel)
        return label

    def getNodeLabel(self, node):
        if 'name' in node and node['name']:
            return node['name']

        elif 'represents' in node:
            return self.getTermLabel(node['represents'])

        else:
            return "node %s" % (node['id'])

    def getTermById(self, termId):
        termIdStr = str(termId)
        if termIdStr in self.network['baseTerms']:
            return self.network['baseTerms'][termIdStr]
        elif termIdStr in self.network['functionTerms']:
            return self.network['functionTerms'][termIdStr]
        elif termIdStr in self.network['reifiedEdgeTerms']:
            return self.network['reifiedEdgeTerms'][termIdStr]
        else:
            return None

    def getTermLabel(self, termId):
        if termId in self.termLabelMap:
            return self.termLabelMap[termId]
        else:
            label = "error"
            term = self.getTermById(termId)
            type = term['type'].lower()
            if type == "baseterm":
                name = term['name']
                if 'namespaceId' in term and term['namespaceId']:
                    namespaceId = term['namespaceId']
                    namespace = self.network['namespaces'][namespaceId]

                    if namespace:
                        if namespace['prefix']:
                            label = "%s:%s" % (namespace['prefix'], name)
                        elif namespace['uri']:
                            label = "%s%s" % (namespace['uri'], name)
                        else:
                            label = name
                    else:
                        label = name
                else:
                    label = name

            elif type == "functionterm":
                functionTermId = term['functionTermId']
                functionLabel = self.getTermLabel(functionTermId)
                functionLabel = getFunctionAbbreviation(functionLabel)
                parameterLabels = []
                for parameterId in term['parameterIds']:
                    parameterLabel = self.getTermLabel(parameterId)
                    parameterLabels.append(parameterLabel)
                label = "%s(%s)" % (functionLabel, ",".join(parameterLabels))

            elif type == "reifiededgeterm":
                edgeId = term['edgeId']
                edges = self.network['edges']
                if edgeId in edges:
                    reifiedEdge = edges[edgeId]
                    label = "(%s)" % (self.getEdgeLabel(reifiedEdge))
                else:
                    label = "(reifiedEdge: %s)" % (edgeId)

            else:
                label = "term: %s" % (termId)

            self.termLabelMap[termId] = label
            return label

    #----------------------------------------------------------
    # Label Methods
    #----------------------------------------------------------

    def writeSummary(self, fileName = None):
        if fileName:
            output = open(fileName, 'w')
        else:
            output = sys.stdout

        # nodes
        for nodeId, node in self.getNodes().iteritems():


        # edges
        for edgeId, edge in self.getEdges().iteritems():

    def writeSummaryByCitation(self, fileName = None):
        if fileName:
            output = open(fileName, 'w')
        else:
            output = sys.stdout
            
        for citationId, supportIdList in self.citationToSupportMap.iteritems():
            citations = self.network['citations']
            citation = citations[str(citationId)]
            citationId = citation['identifier']
            # Write Citation
            output.write("\n=========================================================================\n")
            output.write("        Citation: %s\n" % (citationId))
            output.write("=========================================================================\n\n")

            for supportId in supportIdList:
                support = self.network['supports'][str(supportId)]
                # Write Support
                output.write("_______________________________\n")
                output.write("Evidence: %s\n\n" % support['text'])

                edgeList = self.supportToEdgeMap[supportId]
                for edge in edgeList:
                    # Write Edge
                    output.write("       %s\n" % self.getEdgeLabel(edge))
                    for pv in edge['properties']:
                        output.write("                %s: %s\n" % (pv['predicateString'], pv['value']))

        if fileName:
            output.close()


