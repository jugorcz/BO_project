from lxml import etree
import sys
from guestGenerator import generateGuestsList

def createGuestsDictionary(root):
    guestsDictionary = dict()
    for el in root.getchildren():
        for guest in el.getchildren():
            pair = guest.attrib['name']
            value = guest.text
            guestsDictionary[pair] = value
    return guestsDictionary


def createGuestsList(root):
    guestsList = []
    firstPair = root[1][1].attrib['name']
    firstGuest = firstPair[1:-5]
    guestsNumber = int(root[0].attrib['name'])
    guestsList.append(firstGuest)

    for i in range(guestsNumber - 1):
        guest = root[1][i].attrib['name'][5:-1]
        guestsList.append(guest)
    return guestsList


def setGuestsInOrder(guestsDictionary, guestsList):
    resultFile = open("guestsInOrder.txt", "w")
    for guest in guestsList:
        guestsInOrder = guest
        leftGuests = guestsList.copy()
        leftGuests.remove(guest)
        doStaff(guestsInOrder, leftGuests, resultFile, 0, guestsDictionary)


def findBestFriend(person, leftGuests, guestsDictionary):
    bestFriend = ""
    maxFriendshipLevel = 0

    personNumber = person[1:]
    # print("\nszukam kolegi dla: " + personNumber)

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
        # print(pair + " = " + str(friendshipLevel))
        if friendshipLevel > maxFriendshipLevel:
            maxFriendshipLevel = friendshipLevel
            bestFriend = guest

    # print("<3 = " + bestFriend)
    return bestFriend, int(maxFriendshipLevel)


def doStaff(guestsInOrder, leftGuests, resultFile, sumOfFrienship, guestsDictionary):
    if len(leftGuests) > 0:
        people = guestsInOrder.split('-')
        person = people[len(people) - 1]
        bestFriend, friendshipLevel = findBestFriend(person, leftGuests, guestsDictionary)
        if int(friendshipLevel) > 0:
            leftGuestsWithoutFriend = leftGuests.copy()
            leftGuestsWithoutFriend.remove(bestFriend)
            doStaff(guestsInOrder + "-(" + str(friendshipLevel) + ")-" + bestFriend, leftGuestsWithoutFriend,
                    resultFile, sumOfFrienship + friendshipLevel, guestsDictionary)
    else:
        print(guestsInOrder + "  ->  " + str(sumOfFrienship))
        resultFile.write(guestsInOrder + "  ->  " + str(sumOfFrienship) + "\n")

def manageGuests(num):
    print("\n\n--> set guests in order")
    file = open("generatedData.xml")
    tree = file.read()
    root = etree.fromstring(tree)

    guestsDictionary = createGuestsDictionary(root)
    guestsList = createGuestsList(root)
    setGuestsInOrder(guestsDictionary, guestsList)

    file.close()
    return guestsDictionary, guestsList

if __name__ == "__main__":
    argNum = len(sys.argv)
    if argNum != 2:
        print("Error: missing number of guests")
        sys.exit(1)

    arg = int(sys.argv[1])
    if arg == 0:
        print("Error: wrong guests number")
        sys.exit(1)

    generateGuestsList(arg)
    manageGuests(arg)
