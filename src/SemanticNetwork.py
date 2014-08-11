'''
Created on 11 Aug 2014

@author: mark
'''
# This is the semantic network, it's a static (i.e. does not change during runtime) data structure
# which stores the potential entities and relationships that may be instanciated, and their attributes.
# The terminology used is appropriate to semantic networks rather than graphs as this is what this is, thus
# vertices are referred to as nodes and edges as relations. This preserves the meaning of the network elements

# imitates enum to make control attribute actions clear, the actions control
# what action the instanciator takes when it traverses a relation
# - Associate: keeps a reference to the target node, does not continue down that path
# - Inherit: accumulates the attributes of the target node into the instance and continues down that path.
# - Instanciate: Creates a new instance and accumulates any attributes into the created instance
class ControlAttributeActions:
    Associate, Inherit, Instanciate = range(3)

# Classes to specify the networks elements; nodes and relations.

# Base class stores label and attributes as all network elements possess these 
class NetworkElement(object):
    def __init__(self, label, attributes):
        self.label = label
        self.attributes = attributes

    # returns a formatted string representing all the attributes. The level of indent is used to indent
    # the attributes of relations deeper than those for nodes for clarity        
    def AttributesToString(self, indentLevel):
        indentStr = ""
        for _ in range(indentLevel):
            indentStr = indentStr + "\t"
        outStr = indentStr + "Attributes\n"
        if self.attributes:
            for name, attr in self.attributes.iteritems():
                outStr = outStr + indentStr + "\t" + name + " : " + attr + "\n"
        else:
            outStr = outStr + indentStr + "\tNone\n"
        return outStr
        
# We use a relation class rather than just keeping a list of destination nodes in each mode 
# because each relation need to store its attributes
class Relation(NetworkElement):
    def __init__(self, label, destination, action, attributes):
        super(Relation, self).__init__(label, attributes)
        self.destination = destination
        self.type = action
        
    def __str__(self):
        outStr = self.label + " " + self.destination.label + "\n" + self.AttributesToString(2)
        return outStr

# Nodes use an adjacency list to store connected nodes, the adjacency list stores a relation class rather than nodes
# to allow the relations to store attributes (see comment above)
class Node(NetworkElement):
    def __init__(self, label, attributes):
        super(Node, self).__init__(label, attributes)
        self.relations = []
        
    def AddRelation(self, label, destination, action, attributes):
        self.relations.append(Relation(label, destination, action, attributes))

    def __str__(self):
        outStr = "Node " + self.label + "\n"
        outStr = outStr + self.AttributesToString(1) + "\tRelations\n"
        if self.relations:
            for rel in self.relations:
                outStr = outStr + "\t\t" + str(rel)
        else:
            outStr = outStr + "\t\tNone\n"
        return outStr
        
class Network(object):
    def __init__(self):
        self.nodes = []
        self.nodes.append(Node("base", {}))
        self.nodes.append(Node("world", {}))
        
    def AddNode(self, node):
        self.nodes.append(node)
        
    def GetBase(self):
        return self.nodes[0]
    
    def GetWorld(self):
        return self.nodes[1]
                
    def __str__(self):
        outStr = ""
        for node in self.nodes:
            outStr = outStr + str(node) + "\n"
        return outStr
