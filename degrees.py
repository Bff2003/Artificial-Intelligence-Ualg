import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main(source: str = None, target: str = None, directory: str = "large"):
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else directory

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    if source == None:
        source = input("Name: ")
    if target == None:
        target = input("Name: ")
    source = person_id_for_name(source)
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(target)
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    print("Source:", source, "Target:", target) 
    print("Source:", people[source]["name"], "Target:", people[target]["name"])
    # movies[movie_id]["title"]
    # people[person_id]["name"]

    if source == target:
        return []

    # create a set to store visited nodes
    visited = set()
    visited.add(source)

    # create a frontier to nodes to explore
    to_explore = QueueFrontier()
    to_explore.add(Node(state=source, parent=None, action=None))

    last_node = None
    while True:
        # If there are no more nodes to explore, return None
        # if all nodes have been visited and the target was not found, it is not connected
        if to_explore.empty():
            return None

        node = to_explore.remove()

        to_explore, visited, found = explore(node, to_explore, visited, target)
        if type(found) is Node:
            last_node = found
            break
    
    return mount_path(last_node)

def mount_path(node: Node) -> list:
    path = []
    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path

def explore(node: Node, to_explore: QueueFrontier, visited: set, target: str) -> (QueueFrontier, set, Node|None):
    """
    returns a tuple of the new to_explore, visited, and if the target was found
    """
    neighbors = neighbors_for_person(node.state)
    print("Start Neighbors:", len(neighbors))
    for movie_id, person_id in neighbors: # for each neighbor
        if person_id == target:
            print("Found Target")
            return to_explore, visited, Node(state=person_id, parent=node, action=movie_id)

        if person_id not in visited: # if the neighbor has not been visited, add it to the to_explore list
            visited.add(person_id)
            to_explore.add(Node(state=person_id, parent=node, action=movie_id))
    print("End Visited:", visited)
    return to_explore, visited, None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main("Kevin Bacon", "Tom Hanks", "small")
