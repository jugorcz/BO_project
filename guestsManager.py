from lxml import etree
import sys
from guestGenerator import generateGuestsList

guestsDictionary = dict()
resultList = []

def createGuestsDictionary(root):
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


def setGuestsInOrder(guestsList):
    resultFile = open("guestsInOrder.txt", "w")
    for guest in guestsList:
        guestsInOrder = []
        guestsInOrder.append(guest)
        remainingGuests = guestsList.copy()
        remainingGuests.remove(guest)
        setInOrder(guestsInOrder, remainingGuests, resultFile)


def findBestFriend(person, remainingGuests):
    bestFriend = ""
    maxFriendshipLevel = 0

    #print("\nszukam kolegi dla: " + person)

    for guest in remainingGuests:
        if person == guest:
            continue

        if maxFriendshipLevel == 5:
            break

        friendshipLevel = getFriendshipLevel(person, guest)
        if friendshipLevel > maxFriendshipLevel:
            maxFriendshipLevel = friendshipLevel
            bestFriend = guest

    #print("<3 = " + bestFriend)
    return bestFriend, int(maxFriendshipLevel)

def findFriend(person, remainingGuests):
    friend = ""
    friendshipLevel = 0

    for guest in remainingGuests:
        friendshipLevel = getFriendshipLevel(person, guest)
        if friendshipLevel > 0:
            friend = guest
            break;

    return friend, friendshipLevel

def getFriendshipLevel(person1, person2):
    pair1 = "[" + person2 + "][" + person1 + "]"
    pair2 = "[" + person1 + "][" + person2 + "]"

    if pair1 in guestsDictionary:
        friendshipLevel = int(guestsDictionary[pair1])
    elif pair2 in guestsDictionary:
        friendshipLevel = int(guestsDictionary[pair2])
    else:
        friendshipLevel = 0

    #print(pair1 + " = " + str(friendshipLevel))
    return friendshipLevel

def getsumOfFriendshipLevel(guestsInOrder):
    guest1 = guestsInOrder[0]
    sumOfFrienship = 0
    for i in range(1, leng ):
        guest2 = guestsInOrder[i]
        friendshipLevel = getFriendshipLevel(guest1, guest2)
        sumOfFrienship += friendshipLevel
        guest1 = guest2
    return sumOfFrienship

def createGuestsInOrderText(guestsInOrder):
    guest1 = guestsInOrder[0]
    guestsInOrderText = ""
    leng = len(guestsInOrder)
    sumOfFrienship = 0
    for i in range(1, leng ):
        guestsInOrderText += guest1  + "-("
        guest2 = guestsInOrder[i]
        friendshipLevel = getFriendshipLevel(guest1, guest2)
        sumOfFrienship += friendshipLevel
        guestsInOrderText += str(friendshipLevel) + ")-"
        guest1 = guest2
    guestsInOrderText += guest1
    guestsInOrderText += "  ->  " + str(sumOfFrienship)
    print(guestsInOrderText)
    return guestsInOrderText

def setInOrder(guestsInOrder, remainingGuests, resultFile):
    if len(remainingGuests) > 0:
        lastPersonIndex = len(guestsInOrder) - 1
        person = guestsInOrder[lastPersonIndex]
        bestFriend, friendshipLevel = findFriend(person, remainingGuests)
        if int(friendshipLevel) > 0:
            leftGuestsWithoutFriend = remainingGuests.copy()
            leftGuestsWithoutFriend.remove(bestFriend)
            guestsInOrder.append(bestFriend)
            setInOrder(guestsInOrder, leftGuestsWithoutFriend,
                    resultFile)
    else:
        guestsInOrderText = createGuestsInOrderText(guestsInOrder)
        resultList.append(guestsInOrder)
        resultFile.write(guestsInOrderText + "\n")

def manageGuests(num):
    print("\n\n--> set guests in order")
    file = open("generatedData.xml")
    tree = file.read()
    root = etree.fromstring(tree)

    createGuestsDictionary(root)
    guestsList = createGuestsList(root)
    setGuestsInOrder(guestsList)

    file.close()

    return guestsDictionary, resultList

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
