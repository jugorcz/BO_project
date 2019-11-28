import random
import sys

from lxml import etree

from guestGenerator import generateGuestsList
from guestsManager import manageGuests

worstSolutions = 10
eliteBees = 3
eliteGenerations = 3
subEliteBees = 2
subEliteGenerations = 2
normalBees = worstSolutions - eliteBees - subEliteBees
normalGenerations = 1


def sort_by_sum(val):
    return val["sum"]


def take_worst_solutions_and_best_solution(number_of_solutions, file):
    sums_of_friendships = []
    for line in file:
        line_content = line.split("  ->  ")
        sums_of_friendships.append({
            "content":
            line_content[0].replace("(", "").replace(")", "").split("-"),
            "sum":
            int(line_content[1])
        })

    sums_of_friendships.sort(key=sort_by_sum)
    return sums_of_friendships[:number_of_solutions], sums_of_friendships[
        len(sums_of_friendships) - 1]


def write_solutions_to_file(solutions, file):
    for solution in solutions:
        content_with_hyphens = []
        for i in range(0, len(solution["content"]) - 1):
            content_with_hyphens.append(solution["content"][i] + "-")
        content_with_hyphens.append(
            solution["content"][len(solution["content"]) - 1])
        file.write("".join(content_with_hyphens) + "  ->  " +
                   str(solution["sum"]) + "\n")


def calculate_content_sum(content):
    count = 0
    for i in range(1, len(content) - 1, 2):
        count += int(content[i])
    return count


def improve_solution(solution, number_of_generations):
    new_solutions = []

    for i in range(0, number_of_generations):
        new_solution_content = solution["content"].copy()
        initialSize = len(new_solution_content)
        startingPersonIndex = random.randint(0, (initialSize - 1) /2) * 2
        if startingPersonIndex == initialSize - 1:
          startingPersonIndex = startingPersonIndex - 2
        part_to_change = new_solution_content[-(initialSize-startingPersonIndex):]
        new_solution_content = new_solution_content[:startingPersonIndex - 1]
        del part_to_change[1::2]
        guestsNewOrder = setGuestsInOrder(part_to_change)
        if startingPersonIndex != 0:
          new_solution_content.append(str(getFriendshipLevel(new_solution_content[startingPersonIndex - 2], part_to_change[1])))
        if guestsNewOrder != None:
          new_solution_content = new_solution_content + guestsNewOrder
        if len(new_solution_content) == initialSize:
          new_solutions.append({
            "content": new_solution_content,
            "sum": calculate_content_sum(new_solution_content)
          })

    if len(new_solutions) > 0:
      new_solutions.sort(key=sort_by_sum)
      return new_solutions[len(new_solutions) - 1]
    else:
      return solution


def setGuestsInOrder(guestsList):
      guestsInOrder = []
      secondGuest = guestsList[1]
      guestsInOrder.append(secondGuest)
      remainingGuests = guestsList.copy()
      remainingGuests.remove(secondGuest)
      return setInOrder(guestsInOrder, remainingGuests)

def setInOrder(guestsInOrder, remainingGuests):
    if len(remainingGuests) > 0:
        lastPersonIndex = len(guestsInOrder) - 1
        person = guestsInOrder[lastPersonIndex]
        bestFriend, friendshipLevel = findBestFriend(person, remainingGuests)
        if int(friendshipLevel) > 0:
            leftGuestsWithoutFriend = remainingGuests.copy()
            leftGuestsWithoutFriend.remove(bestFriend)
            guestsInOrder.append(str(friendshipLevel))
            guestsInOrder.append(bestFriend)
            return setInOrder(guestsInOrder, leftGuestsWithoutFriend)
    else:
      return guestsInOrder

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


def bees_algorithm(worst_solutions, best_solution):
    result_file = open("solutions.txt", "w")
    result_file.write("Initial " + str(worstSolutions) +
                      " worst solutions: \n")
    write_solutions_to_file(worst_solutions.copy(), result_file)

    new_solutions = worst_solutions.copy()
    while len(new_solutions) < worstSolutions:
        new_solutions.append(worst_solutions[random.randint(
            0,
            len(worst_solutions) - 1)])
    new_solutions.sort(key=sort_by_sum)

    counter = 0
    while new_solutions[len(new_solutions) - 1]["sum"] < (
            best_solution["sum"] + 1):
        for i in range(0, normalBees):
            new_solutions[i] = improve_solution(new_solutions[i],
                                                normalGenerations)
        for i in range(normalBees, subEliteBees):
            new_solutions[i] = improve_solution(new_solutions[i],
                                                subEliteGenerations)
        for i in range(subEliteBees, eliteBees):
            new_solutions[i] = improve_solution(new_solutions[i],
                                                eliteGenerations)
        counter += 1
        result_file.write("Iteration " + str(counter) + ". \n")
        print("Iteration " + str(counter) + ". \n")
        write_solutions_to_file(new_solutions.copy(), result_file)
        new_solutions.sort(key=sort_by_sum)
    write_solutions_to_file(new_solutions.copy(), result_file)
    result_file.close()
    pass


def main(guests):
    print("\n\n--> bees algorithm")
    guests_file = open("generatedData.xml")
    tree = guests_file.read()
    root = etree.fromstring(tree)

    global guestsDictionary
    guestsDictionary = guests

    guests_file.close()

    guests_order_file = open("guestsInOrder.txt")
    result = take_worst_solutions_and_best_solution(worstSolutions,
                                                    guests_order_file)
    guests_order_file.close()

    worst_solutions = result[0]
    best_solution = result[1]

    bees_algorithm(worst_solutions, best_solution)


if __name__ == "__main__":
    arg = 10

    generateGuestsList(arg)
    guestsDictionary, resultList = manageGuests(arg)
    #resultList = tablica tablic
    print(resultList)

    main(guestsDictionary)
