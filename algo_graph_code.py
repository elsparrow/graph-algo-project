import math
from collections import deque


def tree_attributes(adj_matrix: list[list[bool]]) -> list[list[float | int] | float | int]:
    """
    Problem 1:
    Find center, radius, and diameter of a tree
    Input:  adj_matrix (representing a tree)
        entries of adj_matrix will be true if exists an edge between vertex i and j
    Output:  [[center], radius, diameter]
    """
    # Step 1:
    # Choose arbitrary node, in this case 0.
    dim = len(adj_matrix)  # matrix dimension
    distance = [0] + [math.inf] * (dim - 1)  # list of distances from the beginning node
    queue = deque([0])  # queue the next nodes to check (FIFO)
    # Find the furthest node from the node we chose.
    while queue:  # while not all distances found
        curr = queue.popleft()  # current node = first element in queue, then pop (remove) dequeue that element.
        for i in range(dim):
            if adj_matrix[curr][i] and distance[i] == math.inf:
                # if value of matrix[curr][i] is true (exists an edge between current node and the node at location i)
                # and distance to node i hasn't been found.
                queue.append(i)  # add to queue sons of current node.
                distance[i] = distance[curr] + 1  # assign distance to sons.
    v = 0  # furthest node from node at 0.
    for i in range(dim):  # Find v
        if distance[i] > distance[v]:
            v = i
    # Step 2:
    # we found node v, now we will find the furthest node from v while tracking parents to be able to determine center.
    # we'll run a similar algorithm but track parents this time.
    distance = [math.inf] * dim  # reassign distance list because we want the furthest path from v.
    distance[v] = 0
    queue = deque([v])   # reassign queue to start at v
    parents = [None] * dim  # list to track the parent of each node.
    while queue:
        curr = queue.popleft()
        for i in range(dim):
            if adj_matrix[curr][i] and distance[i] == math.inf:
                queue.append(i)
                distance[i] = distance[curr] + 1
                parents[i] = curr  # the sons parent is curr and curr is parent of his sons
    # Step 3:
    # we found the longest path.  now, we assign diameter and radius.
    diameter = 0
    for i in range(dim):  # find the greatest distance and assign it as diameter
        if diameter < distance[i]:
            diameter = distance[i]
            v = i
    rad = math.ceil(diameter/2)
    # Step 4:
    # find center.
    center = []
    count = 0
    prev = None
    while count < rad:
        prev = v
        v = parents[v]
        count += 1
    center.append(v)
    if diameter % 2 == 1:
        center.append(prev)
    return [center, rad, diameter]


def is_tree(adj_matrix: list[list[bool]]) -> bool:
    """
    function to check if graph is a tree
    :param adj_matrix:
    :return:  True if graph is a tree, False otherwise.
    """
    dim = len(adj_matrix)  # number of nodes
    checked = [True] + [False] * (dim - 1)  # list of nodes checked
    parent = [None] * dim  # track parent of each node if node has two fathers that is haram
    queue = deque([0])  # self-explanatory

    while queue:  # while queue isn't empty.
        curr = queue.popleft()  # current node is next queued item (now removed from queue).
        for i in range(dim):
            if adj_matrix[curr][i]:  # if exist an edge between current node and ith node.
                if i == curr:
                    return False  # self loop
                if not checked[i]:
                    checked[i] = True
                    parent[i] = curr
                    queue.append(i)
                else:
                    if parent[curr] != i:
                        return False  # loop found.
    return all(checked)  # if all nodes were checked (no node left behind).


def num_of_components(adj_mat):
    """
    :param adj_mat:  adjacency matrix representing a graph
    :return: number of connected components
    """
    dim = len(adj_mat)
    checked = [False] * dim
    count = 0  # number of components.

    for i in range(dim):
        if not checked[i]:
            count += 1
            queue = deque([i])
            checked[i] = True
            # check what nodes are connected to the next queued node
            while queue:
                curr = queue.popleft()
                for node in range(dim):
                    if adj_mat[curr][node] and not checked[node]:  # if edge exists and node not checked yet
                        checked[node] = True
                        queue.append(node)
    return count

def is_forest (adj_matrix: list[list[bool]]) -> bool:
    """
    function to check if graph is a forrest
    :param adj_matrix:
    :return:  True if graph is a forrest, False otherwise.
    """
    dim = len(adj_matrix)
    edges = 0  # number of edges
    for i in range(dim):
        for j in range(i , dim):
            if adj_matrix[i][j]:
                if i == j:  # self loop
                    return False
                else:
                    edges += 1
    comps = num_of_components(adj_matrix)  # count components with function from outer scope
    return edges == dim - comps



if __name__ == '__main__':

    # ----------------------------
    # Test graphs (adjacency matrices)
    # ----------------------------

    graphs = {
        "1) single node": (
            [[0]],
            True,  # is_tree
            True  # is_forest
        ),

        "2) two connected nodes": (
            [
                [0, 1],
                [1, 0]
            ],
            True,
            True
        ),

        "3) simple path (0-1-2-3)": (
            [
                [0, 1, 0, 0],
                [1, 0, 1, 0],
                [0, 1, 0, 1],
                [0, 0, 1, 0]
            ],
            True,
            True
        ),

        "4) star graph": (
            [
                [0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0]
            ],
            True,
            True
        ),

        "5) unbalanced tree (branching)": (
            [
                [0, 1, 0, 0, 0, 0],
                [1, 0, 1, 1, 0, 0],
                [0, 1, 0, 0, 1, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1],
                [0, 0, 0, 0, 1, 0]
            ],
            True,
            True
        ),

        "6) unconnected graph (one edge + isolated)": (
            [
                [0, 1, 0],
                [1, 0, 0],
                [0, 0, 0]
            ],
            False,
            True
        ),

        "7) connected graph with self loop": (
            [
                [1, 1, 0],
                [1, 0, 1],
                [0, 1, 0]
            ],
            False,
            False
        ),

        "8) cycle with tail": (
            [
                [0, 1, 1, 0],
                [1, 0, 1, 0],
                [1, 1, 0, 1],
                [0, 0, 1, 0]
            ],
            False,
            False
        ),

        "9) two trees (unconnected)": (
            [
                [0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0]
            ],
            False,
            True
        ),

        "10) three disconnected nodes": (
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ],
            False,
            True
        )
    }


    # ----------------------------
    # Test runner
    # ----------------------------

    def print_matrix(mat):
        for row in mat:
            print(row)


    print("\n===== GRAPH TEST RESULTS =====\n")

    for name, (mat, exp_tree, exp_forest) in graphs.items():
        print(name)
        print("Adjacency Matrix:")
        print_matrix(mat)

        try:
            ta = tree_attributes(mat)
        except Exception as e:
            ta = f"ERROR: {e}"

        try:
            it = is_tree(mat)
        except Exception as e:
            it = f"ERROR: {e}"

        try:
            iff = is_forest(mat)
        except Exception as e:
            iff = f"ERROR: {e}"

        print("tree_attributes:", ta)
        print(f"is_tree:    {it}  | expected: {exp_tree}  | correct: {it == exp_tree}")
        print(f"is_forest:  {iff} | expected: {exp_forest} | correct: {iff == exp_forest}")
        print("-" * 45)

    print("\n===== END TESTS =====\n")
