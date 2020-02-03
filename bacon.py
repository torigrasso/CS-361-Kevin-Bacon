#!/usr/bin/env python3
# ----------------------------------------------------------------------
# bacon.py
# Tori Grasso
# 10/28/2019
# ----------------------------------------------------------------------

import os.path
import sys


def main(argv):
    print("This program will create the shortest path to any actor and Kevin Bacon, Press enter to stop.")

    # check if there is command line argument
    if len(argv) > 1:
        filename = argv[1]
        exist = True
    else:
        while True:
            print("Please enter the file name: ")
            filename = input()
            # check if filename is valid, and if not then tell user it doesn't exist and ask for it again
            if os.path.isfile(filename):
                exist = True
                break
            elif filename == "":
                exist = False
                break
            else:
                print("This file does not exist, try again.")

    # create the graph (multi-layered dictionary) from reading in the file
    graph = graphCreator(filename)

    # call the shortest path algorithm to get the parent dictionary
    parent = shortestPath(graph)

    # ask for the actors and output the results using the graph and parent dictionaries
    while exist:
        # asking user for input
        print("")
        print("Enter the actor's name: ")
        actor = input()

        # if the user hits enter the program will stop
        if actor == "":
            break

        # if user enter kevin bacon then tell them they did it wrong lol
        elif actor == "Kevin Bacon" or actor == "kevin bacon":
            print("You can not enter Kevin Bacon, try another actor")

        # if user enters an actor that is not in the file
        elif actor not in graph or actor not in parent:
            print("This actor is not in the file given")

        # outputting the shortest path
        else:
            while True:
                # if the actor's parent is not kevin bacon then keep going
                if parent[actor] != "Kevin Bacon":
                        # store actor
                        child = actor
                        # get the parent of the actor and set actor to it for the next time through the loop
                        actor = parent[child]
                        # get the film that links the actor and its parent
                        film = graph[child][actor]
                        print(child + " was in " + film + " with " + actor)

                # where the parent of the actor is kevin bacon
                else:
                    # get the film and actor that was with Kevin bacon
                    film = graph["Kevin Bacon"][actor]
                    print(actor + " was in " + film + " with Kevin Bacon")
                    break

               
# figure out the shortest path and return the output in a string
def shortestPath(graph):

    # keep track of the vertices' parents
    parents = {}
    # keep track of the Queue
    queue = []
    # insert first vertex into queue
    queue.append('Kevin Bacon')

    # while the queue is not empty
    while queue != []:
        v1 = queue[0]
        # remove first v1 from the queue
        queue.remove(queue[0])
        # iterate through the adjacent vertices to get each parent
        for v2 in graph[v1]:
            if v2 not in parents and v2 != "Kevin Bacon":
                # add v2 to the queue
                queue.append(v2)
                # set v2s parent to v1
                parents[v2] = v1

    return parents


def graphCreator(filename):
    # open file
    file = open(filename, 'r')

    # set the state to start at film
    state = "film"
    # setting up dictionary and list to empty before putting anything in them
    graph = {}
    actors = []

    # read through each line in the file
    for line in file:
        # save line as film
        if state == "film":
            edge = line.rstrip("\n")
            state = "actor"

        elif state == "actor":
            vertices = line.rstrip("\n")
            # if there is a blank line, that film is done
            if vertices == "":
                # iterate through the actors and add to the graph
                for actor1 in actors:
                    # so there are no duplicates
                    if actor1 not in graph:
                        graph[actor1] = {}
                    # nested loop because each actor needs the other actors and film
                    for actor2 in actors:
                        # so it does not add itself
                        if actor2 != actor1:
                            # multi valued dictionary
                            graph[actor1][actor2] = edge

                # reset the actors list for the next film
                actors = []
                # change state back for the next film
                state = "film"

            # save line as the actor
            else:
                # add the vertices to the list
                actors.append(vertices)
                state = "actor"

    # close file
    file.close()

    return graph


if __name__ == "__main__":
    main(sys.argv)
