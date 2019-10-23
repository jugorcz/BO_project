from lxml import etree
import random

def generateGuests(guestsNumber, document):
    counter = 0
    for i in range(guestsNumber):
        for j in range (i+1, guestsNumber):
            guestsPair = "[g" + str(i) + "][g" + str(j) + "]"
            guestsRelation = str(random.randint(0,5))
            #print(guestsPair + " = " + guestsRelation)
            etree.SubElement(document, "pair", name = guestsPair).text = guestsRelation
            counter+=1

def main():
    guestsNumber = 100
    root = etree.Element("root")
    etree.SubElement(root, "guestsNumber", name = str(guestsNumber))
    document = etree.SubElement(root, "guestsList")

    generateGuests(guestsNumber, document)

    et = etree.ElementTree(root)
    et.write("generatedData.xml", pretty_print=True)

if __name__ == "__main__":
    main()

