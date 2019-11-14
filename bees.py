import random

from lxml import etree

import guestsManager

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
        sums_of_friendships.append(
            {
                "content": line_content[0].replace("(", "").replace(")", "").split("-"),
                "sum": int(line_content[1])
            }
        )

    sums_of_friendships.sort(key=sort_by_sum)
    return sums_of_friendships[:number_of_solutions], sums_of_friendships[len(sums_of_friendships) - 1]


def write_solutions_to_file(solutions, file):
    for solution in solutions:
        content_with_hyphens = []
        for i in range(0, len(solution["content"]) - 1):
            content_with_hyphens.append(solution["content"][i] + "-")
        content_with_hyphens.append(solution["content"][len(solution["content"]) - 1])
        file.write("".join(content_with_hyphens) + "  ->  " + str(solution["sum"]) + "\n")


def calculate_content_sum(content):
    count = 0
    for i in range(1, len(content) - 1, 2):
        count += int(content[i])
    return count


def calculate_relation(guest1, guest2):
    relation_value = 0
    if int(guest1.replace("g", "")) < int(guest2.replace("g", "")):
        relation_value = guestsDictionary["[" + guest1 + "][" + guest2 + "]"]
    else:
        relation_value = guestsDictionary.get("[" + guest2 + "][" + guest1 + "]")
    return relation_value


def update_relations(content, guest_index):
    content[guest_index - 1] = calculate_relation(content[guest_index], content[guest_index - 2])
    content[guest_index + 1] = calculate_relation(content[guest_index], content[guest_index + 2])


def improve_solution(solution, number_of_generations):
    new_solutions = []
    indexes_of_not_optimal_values = [i for i, value in enumerate(solution["content"]) if value == "1"] + \
                                    [i for i, value in enumerate(solution["content"]) if value == "2"] + \
                                    [i for i, value in enumerate(solution["content"]) if value == "3"]

    for i in range(0, number_of_generations):
        new_solution_content = solution["content"].copy()
        guest1_index = indexes_of_not_optimal_values[
                           random.randint(0, len(indexes_of_not_optimal_values) - 1)
                       ] - 1
        guest2_index = indexes_of_not_optimal_values[
                           random.randint(0, len(indexes_of_not_optimal_values) - 1)
                       ] - 1

        # swap two guests
        new_solution_content[guest1_index], new_solution_content[guest2_index] = \
            new_solution_content[guest2_index], new_solution_content[guest1_index]
        # update list with new relations
        update_relations(new_solution_content, guest1_index)
        update_relations(new_solution_content, guest2_index)
        new_solutions.append({"content": new_solution_content, "sum": calculate_content_sum(new_solution_content)})

    new_solutions.sort(key=sort_by_sum)

    return new_solutions[len(new_solutions) - 1]


def bees_algorithm(worst_solutions, best_solution):
    result_file = open("solutions.txt", "w")
    result_file.write("Initial " + str(worstSolutions) + " worst solutions: \n")
    write_solutions_to_file(worst_solutions.copy(), result_file)

    new_solutions = worst_solutions.copy()
    counter = 0
    while new_solutions[len(new_solutions) - 1]["sum"] < best_solution["sum"]:
        for i in range(0, normalBees):
            new_solutions[i] = improve_solution(new_solutions[i], normalGenerations)
        for i in range(normalBees, subEliteBees):
            new_solutions[i] = improve_solution(new_solutions[i], subEliteGenerations)
        for i in range(subEliteBees, eliteBees):
            new_solutions[i] = improve_solution(new_solutions[i], eliteGenerations)
        counter += 1
        result_file.write("Iteration " + str(counter) + ". \n")
        # print("Iteration " + str(counter) + ". \n")
        write_solutions_to_file(new_solutions.copy(), result_file)
        new_solutions.sort(key=sort_by_sum)
    write_solutions_to_file(new_solutions.copy(), result_file)
    result_file.close()
    pass


def main():
    guests_file = open("generatedData.xml")
    tree = guests_file.read()
    root = etree.fromstring(tree)

    global guestsDictionary
    guestsDictionary = guestsManager.createGuestsDictionary(root)

    guests_file.close()

    guests_order_file = open("guestsInOrder.txt")
    result = take_worst_solutions_and_best_solution(worstSolutions, guests_order_file)
    guests_order_file.close()

    worst_solutions = result[0]
    best_solution = result[1]

    bees_algorithm(worst_solutions, best_solution)


if __name__ == "__main__":
    main()
