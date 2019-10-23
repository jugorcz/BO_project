from lxml import etree

guestsDictionary = dict()
guestsList = []

def createGuestsDictionary(root):
    for el in root.getchildren():
        for guest in el.getchildren():
            pair = guest.attrib['name']
            value = guest.text
            guestsDictionary[pair] = value

def createGuestsList(root):
    firstPair = root[1][1].attrib['name']
    firstGuest = firstPair[1:-5]
    guestsNumber = int(root[0].attrib['name'])
    guestsList.append(firstGuest)

    for i in range(guestsNumber-1):
        guest = root[1][i].attrib['name'][5:-1]
        guestsList.append(guest)

def setGuestsInOrder():
    resultFile = open("guestsInOrder.txt", "w")
    for guest in guestsList:
        guestsInOrder = guest
        leftGuests = guestsList.copy()
        leftGuests.remove(guest)
        doStaff(guestsInOrder, leftGuests, resultFile, 0)

def findBestFriend(person, leftGuests):
    bestFriend = ""
    maxFriendshipLevel = 0

    personNumber = person[1:]
    #print("\nszukam kolegi dla: " + personNumber)

    for guest in leftGuests:
        if person == guest:
            continue

        if maxFriendshipLevel == 5:
           break

        guestNumber = guest[1:]

        if int(personNumber) > int(guestNumber):
            pair = "[" + guest + "][" + person + "]"
        else:
            pair = "[" + person + "][" + guest + "]"

        friendshipLevel = int(guestsDictionary[pair])
        #print(pair + " = " + str(friendshipLevel))
        if friendshipLevel > maxFriendshipLevel:
            maxFriendshipLevel = friendshipLevel
            bestFriend = guest

    #print("<3 = " + bestFriend)
    return bestFriend, int(maxFriendshipLevel)

def doStaff(guestsInOrder, leftGuests, resultFile, sumOfFrienship):
    if len(leftGuests) > 0:
        people = guestsInOrder.split('-')
        person = people[len(people)-1]
        bestFriend, friendshipLevel = findBestFriend(person, leftGuests)
        if int(friendshipLevel) > 0:
            leftGuestsWithoutFriend = leftGuests.copy()
            leftGuestsWithoutFriend.remove(bestFriend)
            doStaff(guestsInOrder + "-(" + str(friendshipLevel) + ")-" + bestFriend, leftGuestsWithoutFriend, resultFile, sumOfFrienship + friendshipLevel)
    else:
        print(guestsInOrder + "  ->  " + str(sumOfFrienship))
        resultFile.write(guestsInOrder + "  ->  " + str(sumOfFrienship) + "\n")

def main():
    file = open("generatedData.xml")
    tree = file.read()
    root = etree.fromstring(tree)

    createGuestsDictionary(root)
    createGuestsList(root)
    setGuestsInOrder()

    file.close()

if __name__ == "__main__":
    main()