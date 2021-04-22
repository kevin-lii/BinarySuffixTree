import sys
import re
from RangeDict import * 
from Node import * 

# Suffix Tree
class SuffixTree(object):
    def __init__(self):
        self.text = [] 
        self.fileList = RangeDict() 
        self.files = {}
        self.initialStorageNode = Node() 
        self.root = Node() 
        self.root.suffixLink = self.initialStorageNode
        self.node = self.root
        self.k = 0
        self.i = -1 

    def addFile(self, text, fileName):
        ori_len = len(self.text)
        self.text += text
        self.fileList[range(ori_len, len(self.text))] = fileName
        self.files[fileName] = ori_len
        node = self.node
        k = self.k
        i = self.i
        for j in range(ori_len, len(self.text)):
            self.initialStorageNode.addChildren(self.root, j, j, self.text[j])
        while i < len(self.text) - 1:
            i += 1
            tempNode, tempK = self.update(node, k ,i)
            node, k = self.iterateOver(tempNode, tempK, i)
        self.node = node
        self.k = k
        self.i = i 

    def update(self, sNode, k , i):
        oldrNode = self.root
        endPoint, rNode = self.trySplitNode(sNode, k, i - 1, self.text[i])
        while not endPoint:
            tempNode, origK = Node(), k
            rNode.addChildren(tempNode, i, len(self.text) - 1, self.text[i])
            tempNode.addParent(rNode)
            if oldrNode != self.root:
                oldrNode.suffixLink = rNode
            oldrNode = rNode
            sNode, k = self.iterateOver(sNode.suffixLink, k, i - 1)
            endPoint, rNode = self.trySplitNode(sNode, k, i - 1, self.text[i])
            if oldrNode != self.root:
                for parent in sNode.parents:
                    if parent.id != self.root.id and len(self.text) > origK + 1 and sNode.id in parent.childrenHelper:
                        if self.text[origK + 1] in parent.children:
                            parent.updateChildrenOffest(self.text[origK + 1], origK + 1)
                        elif self.text[origK] in parent.children:
                            parent.updateChildrenOffest(self.text[origK], origK)

                oldrNode.suffixLink = sNode
        return sNode, k

    def trySplitNode(self, node, k, p, textChar):
        if k <= p:
            node2, k2, p2, _ = node.children[self.text[k]]
            if textChar == self.text[k2 + p - k + 1]:
                return True, node
            else:
                tempNode = Node()
                node.addChildren(tempNode, k2, k2 + p - k, self.text[k2])
                tempNode.addChildren(node2, k2 + p - k + 1, p2, self.text[k2 + p - k + 1])
                # Since we replaced the children of the node to reflect the change, we lost the original child
                node.updateChildrenOffest(self.text[k2], k)
                node.fixChildrenHelper(node2)
                node2.splitCopyNode(tempNode)
                tempNode.addParent(node)
                return False, tempNode
        else:
            if textChar in node.children:
                return True, node
            else:
                return False, node

    def iterateOver(self, node, k, p):
        if p < k:
            return node, k
        else:
            node2, k2, p2, _ = node.children[self.text[k]]
        origK, origNode, addNewNode = k, node, False
        while p2 - k2 <= p - k:
            addNewNode = True
            k = k + p2 - k2 + 1
            node = node2
            if k <= p:
                node2, k2, p2, _ = node.children[self.text[k]]
        if addNewNode:
            origNode.updateChildrenOffest(self.text[origK], origK)
        return node, k

    def dfs(self, children, visited, length, prevNodes):
        node, start, end, fileOffsets = children
        if node.id not in visited:
            visited.add(node.id)
            offsets, fileToOffset = self.checkFileList(fileOffsets, start, end, length)
            if len(fileToOffset) < 2:
                return 0, [], []
            length += (end - start + 1)
            prevNodes.append(node.id)
            longest, longestOffsets, nodeList = length, offsets, prevNodes
            if node.isLeaf():
                return length, fileToOffset, prevNodes
            for key in node.children:
                tempLength, tempFileToOffset, tempNodeList = self.dfs(node.children[key], visited, length, prevNodes)
                if tempLength > longest:
                    longest, longestOffsets, nodeList = tempLength, tempFileToOffset, tempNodeList
            return longest, longestOffsets, nodeList
        
    def longest_subsequence(self):
        longest, longestFilesAndOffsets, longestNodeList = 0, {}, []
        visited = set()
        for key in self.root.children:
            node, start, end, nodeFileOffsets = self.root.children[key]
            tempLongest, finalFileOffsets, nodeList = self.dfs(self.root.children[key], visited, 0, [])
            if tempLongest > longest:
                longest = tempLongest
                tempFilesAndOffsets = {}
                longestNodeList = nodeList
                for offset in finalFileOffsets:
                    file = self.fileList[offset]
                    offset -= self.files[file]
                    tempFilesAndOffsets[file] = offset
                longestFilesAndOffsets = tempFilesAndOffsets
                
        return longest, longestFilesAndOffsets, longestNodeList
    
    def checkFileList(self, fileOffset, nodeStart, nodeEnd, prevLength):
        length = nodeEnd - nodeStart + 1
        res, resFile = [], []
        for offset in fileOffset:
            if self.text[offset - prevLength : offset + length] == self.text[nodeStart - prevLength : nodeEnd + 1]:
                res.append(offset - prevLength)
                file = self.fileList[offset]
                if file not in resFile:
                    resFile.append(file)
        return res, resFile





