class Node(object):
    nodeNumber = -1
    def __init__(self):
        self.children = {} 
        self.childrenHelper = {}
        self.suffixLink = None
        self.parents = []
        self.id = Node.nodeNumber 
        Node.nodeNumber += 1 

    def addChildren(self, node, start, end, ch):
        self.children[ch] = (node, start, end, [start])
        self.childrenHelper[node.id] = ch
    
    def updateChildrenOffest(self, ch, offset):
        offsets = self.children[ch][3]
        if offset not in offsets:
            offsets.append(offset)

    def fixChildrenHelper(self, node):
        if node.id in self.childrenHelper:
            del self.childrenHelper[node.id]
    
    def addParent(self, parent):
        self.parents.append(parent)
    
    def splitCopyNode(self, newNode):
        for parent in self.parents:
            newNode.parents.append(parent)
        self.addParent(newNode)
        
    def isLeaf(self):
        return len(self.children) == 0