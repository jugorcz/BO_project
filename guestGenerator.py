from lxml import etree
import random

guestsNumber = 10

def generateGuests(guestsNumber, document):
    fivesLeft = guestsNumber/2
    counter = 0
    for i in range(guestsNumber):
        for j in range (i+1, guestsNumber):
            guestsPair = "[g" + str(i) + "][g" + str(j) + "]"

            guestsRelation = random.randint(0,5)
            if guestsRelation == 5:
                if fivesLeft <= 0:
                    while guestsRelation == 5:
                        guestsRelation = random.randint(0,5)
                else:
                    fivesLeft -= 1

            etree.SubElement(document, "pair", name = guestsPair).text = str(guestsRelation)
            counter+=1

def main():

    root = etree.Element("root")
    etree.SubElement(root, "guestsNumber", name = str(guestsNumber))
    document = etree.SubElement(root, "guestsList")

    generateGuests(guestsNumber, document)

    et = etree.ElementTree(root)
    et.write("generatedData.xml", pretty_print=True)

if __name__ == "__main__":
    main()

