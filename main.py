from SuffixTree import *

# main function
# python -c 'from main import *; print(longest_subsequence(["hard/1.bin", "hard/2.bin"]))'
# python -c 'from main import *; print(longest_subsequence(["sample.3", "sample.2", "sample.4", "sample.5", "sample.6", "sample.7", "sample.8", "sample.9", "sample.10", "sample.1"]))'
# python -c 'from main import *; print(longest_subsequence(["hard/" + str(x) + ".bin" for x in range(20)]))'
def longest_subsequence(fileNames):
    suffix_tree = SuffixTree()
    longest = 0
    files = {}
    for fileName in fileNames:
        x_bytes = open_binary_file(fileName)
        x = convert_bytes_to_int(x_bytes)
        x.append(fileName)
        suffix_tree.addFile(x, fileName)
    return suffix_tree.longest_subsequence()[0:2]

def longest_subsequence_partial(fileNames):
    suffix_tree = SuffixTree()
    longest = 0
    files = {}
    for fileName in fileNames.keys():
        x_bytes = open_binary_file(fileName)
        x = convert_bytes_to_int(x_bytes, fileNames[fileName])
        x.append(fileName)
        suffix_tree.addFile(x, fileName)
    return suffix_tree.longest_subsequence()

def open_binary_file(fileName):
    with open(fileName, mode='rb') as file:
        fileContent = file.read()
    file.close()
    return fileContent

def convert_bytes_to_int(x_bytes, bounds=None):
    lst = []
    start = 0
    end = len(x_bytes)
    if bounds is not None:
        start = bounds[0] - 2000
        end = bounds[1] + 2000
    for i in range(start, end):
        lst.append(x_bytes[i])
    return lst