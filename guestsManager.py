from lxml import etree

def main():
    file = open("generatedData.xml")
    tree = file.read()
    root = etree.fromstring(tree)

    guestsDictionary = dict()
    for el in root.getchildren():
        for guest in el.getchildren():
            pair = guest.attrib['name']
            value = guest.text
            guestsDictionary[pair] = value

    guestsList = []
    firstPair = root[1][1].attrib['name']
    firstGuest = firstPair[1:-5]
    guestsNumber = int(root[0].attrib['name'])
    guestsList.append(firstGuest)

    for i in range(guestsNumber-1):
        guest = root[1][i].attrib['name'][5:-1]
        guestsList.append(guest)

    for el in guestsList:
        print(el)
    print(len(guestsList))

if __name__ == "__main__":
    main()