import gzip

def getAsin(filename):
  f = gzip.open(filename, 'r')
  for l in f:
    l = l.strip()
    colonPos = l.find(' ')
    nodeId = l[:colonPos]
    yield nodeId
    

def createNodeIdFile():
  i = 0
  of = open('nodeIdDict.txt', 'w')
  for e in getAsin("related.txt.gz"):
    of.write(e + ' ' +str(i) + '\n')
    i += 1
    # if i > 10:
    #   break
  of.close()


def getNodeId(asin):
  # print asin
  idfile = open('nodeIdDict.txt', 'r')
  for l in idfile:
    if asin == l[:10] :
      l = l.strip()
      nodeId = int(l[11:])
      return nodeId
  return -1

def getNodeIdDict(filename):
  f = open(filename, 'r')
  entry = {}
  for l in f:
    l = l.strip()
    asin = l[:10]
    nodeId = int(l[11:])
    entry[asin] = nodeId
  f.close()
  return entry


def createGraph():
  ifile = gzip.open('related.txt.gz', 'r')
  ofile = open('linkList.txt', 'w')
  omittedLink = 0
  nodeId = 0
  nodeIdDict = getNodeIdDict('nodeIdDict.txt')
  for l in ifile:
    lineLength = len(l)-9
    colPos = 26
    while colPos < lineLength:
      destineAsin = l[colPos:colPos+10]
      if destineAsin[0] == 'r':
        break
      # destineId = getNodeId(destineAsin)
      if destineAsin in nodeIdDict:
        destineId = nodeIdDict[destineAsin]
        ofile.write(str(nodeId)+' '+str(destineId)+'\n')
      else:
        omittedLink += 1
      colPos += 11
    nodeId += 1
    # if nodeId > 5:
    #   break

  ifile.close()
  ofile.close()   
  print omittedLink

createNodeIdFile()
createGraph()

