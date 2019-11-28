from lxml import etree
import random
import sys

limit = [0 for i in range(6)]

def setLimits(percentageRelationList):
    if len(percentageRelationList) != 6:
        limit[0] = 30
        limit[1] = 30
        limit[2] = 15
        limit[3] = 10
        limit[4] = 8
        limit[5] = 7
    else:
        limit[0] = int(percentageRelationList[0])
        limit[1] = int(percentageRelationList[1])
        limit[2] = int(percentageRelationList[2])
        limit[3] = int(percentageRelationList[3])
        limit[4] = int(percentageRelationList[4])
        limit[5] = int(percentageRelationList[5])


def getCustomRandom():
    limitsSum = limit[0] + limit[1] + limit[2] + limit[3] + limit[4] + limit[5]

    rand = random.randint(0,limitsSum)
    base = 0
    for i in range(6):
        if rand in range(base, base + limit[i]):
            return i 
        else:
            base += limit[i]
    return 0

def generateGuests(guestsNumber, document):
    for i in range(guestsNumber):
        for j in range(i + 1, guestsNumber):
            guestsPair = "[g" + str(i) + "][g" + str(j) + "]"
            guestsRelation = getCustomRandom()
            print(guestsPair + " relation: " + str(guestsRelation))
            etree.SubElement(document, "pair", name=guestsPair).text = str(guestsRelation)


def generateGuestsList(num, percentageRelationList=[]):
    print("--> generate guests list")
    guestsNumber = num
    root = etree.Element("root")
    etree.SubElement(root, "guestsNumber", name=str(guestsNumber))
    document = etree.SubElement(root, "guestsList")
    setLimits(percentageRelationList)
    generateGuests(guestsNumber, document)

    et = etree.ElementTree(root)
    et.write("generatedData.xml", pretty_print=True)

if __name__ == "__main__":
    argNum = len(sys.argv)
    if argNum < 2:
        print("Error: missing number of guests")
        sys.exit(1)

    arg = int(sys.argv[1])
    if arg == 0:
        print("Error: wrong guests number")
        sys.exit(1)

    percentageRelationList = []
    if argNum == 8: 
        percentageRelationList = sys.argv[2:]

    generateGuestsList(arg, percentageRelationList)
