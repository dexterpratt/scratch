# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:10:59 2014

@author: Dexter Pratt
"""
import sys

# This is specific to summarizing a BEL network. 
# Need to generalize
def stripBELPrefixes(input):
    st = input.lower()
    inputLength = len(input)
    if st.startswith('bel:'):
        return input[4:inputLength]
    elif st.startswith('hgnc:'):
         return input[5:inputLength]
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

def hasProperty(ndexObject, property, value):
    properties = ndexObject.get("properties")
    pred = property.lower()
    if properties:
        for item in properties:
            p = item.get("predicateString")
            if p and p.lower() == pred:
                v = item.get("value")
                if v and v == value:
                    return True
    return False

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
            for supportId in edge.get('supportIds'):
                support = self.getSupport(supportId)
                if supportId in self.supportToEdgeMap:
                    edgeList = self.supportToEdgeMap.get(supportId)
                else:
                    edgeList = []
                edgeList.append(edge)
                self.supportToEdgeMap[supportId] = edgeList

        for supportId in self.supportToEdgeMap.keys():
            support = self.getSupport(supportId)
            citationId = support['citationId']
            if citationId in self.citationToSupportMap:
                supportIdList = self.citationToSupportMap.get(citationId)
            else:
                supportIdList = []
            supportIdList.append(supportId)
            self.citationToSupportMap[citationId] = supportIdList


    def setName(self, name):
        self.network["name"] = name

    #----------------------------------------------------------
    # Basic Element Access
    #----------------------------------------------------------

    def getEdges(self):
         return self.network.get('edges')

    def getEdge(self, edgeId):
        return self.network.get("edges").get(str(edgeId))

    def getNodes(self):
        return self.network.get("nodes")

    def getNode(self, nodeId):
        return self.network.get("nodes").get(str(nodeId))

    def getCitations(self):
        return self.network.get("citations")

    def getCitation(self, citationId):
        return self.network.get("citations").get(str(citationId))

    def getSupports(self):
        return self.network.get("supports")

    def getSupport(self, supportId):
        return self.network.get("supports").get(str(supportId))

    def getTerm(self, termId):
        termIdStr = str(termId)
        if termIdStr in self.getBaseTerms():
            return self.getBaseTerm(termIdStr)
        elif termIdStr in self.getFunctionTerms():
            return self.getFunctionTerm(termIdStr)
        elif termIdStr in self.getReifiedEdgeTerms():
            return self.getReifiedEdgeTerm(termIdStr)
        else:
            return None

    def getBaseTerms(self):
        return self.network.get("baseTerms")

    def getBaseTerm(self, baseTermId):
        return self.network.get("baseTerms").get(str(baseTermId))

    def getFunctionTerms(self):
        return self.network.get('functionTerms')

    def getFunctionTerm(self, functionTermId):
        return self.network.get("functionTerms").get(str(functionTermId))

    def getReifiedEdgeTerms(self):
        return self.network.get('reifiedEdgeTerms')

    def getReifiedEdgeTerm(self, reifiedEdgeTermId):
        return self.network.get("reifiedEdgeTerms").get(str(reifiedEdgeTermId))

    def getNamespaces(self):
        return self.network.get('namespaces')

    def getNamespace(self, namespaceId):
        return self.network.get("namespaces").get(str(namespaceId))

    #----------------------------------------------------------
    # Basic Element Creation
    #----------------------------------------------------------

    def nextElementId(self):
        return "0000"

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
        elementId = self.nextElementId();

    def createSupport(self, text, citationId):
        elementId = self.nextElementId();

    #----------------------------------------------------------
    # Element removal
    #----------------------------------------------------------

    def removeEdge(self, edgeId):
        edges = self.getEdges()
        if edgeId in edges:
            del edges[edgeId]

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

    # def copyTerm(self, sourceNetwork, sourceTermId):
    #
    # def copyFunctionTerm(self, sourceNetwork, sourceTermId):
    #
    # def copyBaseTerm(self, sourceNetwork, sourceTermId):
    #
    # def copyReifiedEdgeTerm(self, sourceNetwork, sourceTermId):
    #
    # def copyCitation(self, sourceNetwork, sourceCitationId):
    #
    # def copySupport(self, sourceNetwork, sourceSupportId):
    #
    # def copyNamespace(self, sourceNetwork, sourceNamespaceId):

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
        subjectId = edge.get('subjectId')
        objectId = edge.get('objectId')

        if subjectId :
            subjectLabel = self.nodeLabelMap.get(subjectId, "missing node")
        else:
            subjectLabel = "(no subject)"

        if objectId:
            objectLabel = self.nodeLabelMap.get(objectId, "missing")
        else:
            objectLabel = "(no object)"

        predicateId = edge.get('predicateId')
        if predicateId:
            predicateLabel = stripBELPrefixes(self.getTermLabel(predicateId))
        else:
            predicateLabel = "(no predicate)"

        label = "%s %s %s" % (subjectLabel, predicateLabel, objectLabel)
        return label

    def getNodeLabel(self, node):
        label = node.get('name')
        if label:
            return label

        elif 'represents' in node:
            return self.getTermLabel(node.get('represents'))

        else:
            return "node %s" % (node.get('id'))

    def getTermLabel(self, termId):
        label = self.termLabelMap.get(termId)
        if label:
            return label
        else:
            label = "error"
            term = self.getTerm(termId)
            type = term['type'].lower()
            if type == "baseterm":
                name = term.get('name')
                namespaceId = term.get('namespaceId')
                if namespaceId:
                    namespace = self.getNamespace(namespaceId)

                    if namespace:
                        prefix = namespace.get('prefix')
                        if prefix and prefix.upper() == "BEL":
                            label = name
                        elif prefix:
                            label = "%s:%s" % (prefix, name)
                        elif namespace.get('uri'):
                            label = "%s%s" % (namespace.get('uri'), name)
                        else:
                            label = name
                    else:
                        label = name
                else:
                    label = name

            elif type == "functionterm":
                functionTermId = term.get('functionTermId')
                functionLabel = self.getTermLabel(functionTermId)
                functionLabel = getFunctionAbbreviation(functionLabel)
                parameterLabels = []
                for parameterId in term.get('parameterIds'):
                    parameterLabel = self.getTermLabel(parameterId)
                    parameterLabels.append(parameterLabel)
                label = "%s(%s)" % (functionLabel, ",".join(parameterLabels))

            elif type == "reifiededgeterm":
                edgeId = term.get('edgeId')
                reifiedEdge = self.getEdge(edgeId)
                if reifiedEdge:
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
            output.write("       %s\n" % self.getNodeLabel(node))

        # edges
        for edgeId, edge in self.getEdges().iteritems():
            self.writeEdgeSummary(edge, output)

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
                    self.writeEdgeSummary(edge, output)


        if fileName:
            output.close()

    def writeEdgeSummary(self, edge, output):
        # Write Edge
        output.write("       %s\n" % self.getEdgeLabel(edge))
        for pv in edge.get('properties'):
            output.write("                %s: %s\n" % (pv.get('predicateString'), pv.get('value')))
