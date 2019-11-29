import random
import sys

from lxml import etree

import guestsManager
from guestGenerator import generateGuestsList
from guestsManager import manageGuests, findBestFriend, getFriendshipLevel

worstSolutions = 10
eliteBees = 3
eliteGenerations = 3
subEliteBees = 2
subEliteGenerations = 2
normalBees = worstSolutions - eliteBees - subEliteBees
normalGenerations = 1

desiredImprovement = 750


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
    improved_solutions = []

    for i in range(0, number_of_generations):
        new_solution_content = solution["content"].copy()
        initial_size = len(new_solution_content)
        starting_person_index = random.randint(0, (initial_size - 1) / 2) * 2
        if starting_person_index == initial_size - 1:
            starting_person_index = starting_person_index - 2
        part_to_change = new_solution_content[-(initial_size - starting_person_index):]
        new_solution_content = new_solution_content[:starting_person_index - 1]
        del part_to_change[1::2]
        guests_new_order = setGuestsInOrder(part_to_change)
        if starting_person_index != 0:
            new_solution_content.append(
                str(getFriendshipLevel(new_solution_content[starting_person_index - 2], part_to_change[1])))
        if guests_new_order is not None:
            new_solution_content = new_solution_content + guests_new_order
        if len(new_solution_content) == initial_size:
            improved_solutions.append({
                "content": new_solution_content,
                "sum": calculate_content_sum(new_solution_content)
            })

    if len(improved_solutions) > 0:
        improved_solutions.sort(key=sort_by_sum)
        return improved_solutions[len(improved_solutions) - 1]
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
            best_solution["sum"] + desiredImprovement):
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
    if guests is not None:
        guestsDictionary = guests
    else:
        guestsDictionary = guestsManager.createGuestsDictionary(root)

    guests_file.close()

    guests_order_file = open("guestsInOrder.txt")
    result = take_worst_solutions_and_best_solution(worstSolutions,
                                                    guests_order_file)
    guests_order_file.close()

    worst_solutions = result[0]
    best_solution = result[1]

    bees_algorithm(worst_solutions, best_solution)


if __name__ == "__main__":
    arguments_number = len(sys.argv)
    if arguments_number < 2:
        main(None)
    elif arguments_number == 2:
        guests_number = int(sys.argv[1])
        if guests_number <= 0:
            print("Error: wrong guests number.")
            sys.exit(1)
        generateGuestsList(guests_number)
        guestsDictionary, resultList = manageGuests(guests_number)
        main(guestsDictionary)
    else:
        print("Error: too many arguments.")
        sys.exit(1)
