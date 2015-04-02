import gzip
from sets import Set

def getAsin(filename):
  f = gzip.open(filename, 'r')
  for l in f:
    l = l.strip()
    colonPos = l.find(' ')
    nodeId = l[:colonPos]
    yield nodeId
    

def createNodeIdFile2():
  asinSet = Set(getAsin('related.txt.gz'))
  # print len(asinSet)
  ifile = gzip.open('related.txt.gz', 'r')
  for l in ifile:
    lineLength = len(l)-9
    colPos = 26
    while colPos < lineLength:
      asin = l[colPos:colPos+10]
      if asin[0] == 'r':
        break
      asinSet.add(asin)
      colPos += 11
  ifile.close()

  i = 0
  of = open('nodeIdDict2.txt', 'w')
  for e in asinSet:
    of.write(e + ' ' +str(i) + '\n')
    i += 1
  of.close()


def getNodeId(asin):
  # print asin
  idfile = open('nodeIdDict2.txt', 'r')
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


def createGraph2():
  ifile = gzip.open('related.txt.gz', 'r')
  ofile = open('linkList2.txt', 'w')

  nodeIdDict = getNodeIdDict('nodeIdDict2.txt')
  for l in ifile:
    lineLength = len(l)-9
    colPos = 26
    while colPos < lineLength:
      startAsin = l[:10]
      startId = nodeIdDict[startAsin]
      destineAsin = l[colPos:colPos+10]
      if destineAsin[0] == 'r':
        break

      destineId = nodeIdDict[destineAsin]
      ofile.write(str(startId)+' '+str(destineId)+'\n')
      colPos += 11
    # if nodeId > 5:
    #   break

  ifile.close()
  ofile.close()   

createNodeIdFile2()
createGraph2()
