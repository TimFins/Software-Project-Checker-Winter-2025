from __future__ import annotations
from typing import TYPE_CHECKING
import graphviz
import base64
from PIL import Image
from io import BytesIO
from itertools import permutations
from math import inf
from copy import deepcopy
import traceback
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from random import choice, sample, randint

if TYPE_CHECKING:
    from checker.datastructures.avltree._classes.AVLTreeNode import AVLTreeNode

######################### Visualization #############################################################################


def _get_tree_height(node: AVLTreeNode, show_nil_nodes: bool):
    left = node.left
    right = node.right
    left_height = (1 if show_nil_nodes else 0) if left is None else _get_tree_height(
        left, show_nil_nodes)
    right_height = (1 if show_nil_nodes else 0) if right is None else _get_tree_height(
        right, show_nil_nodes)
    return max(left_height, right_height) + 1


def _draw_subtree(dot: graphviz.Digraph, show_nil_nodes: bool, node: AVLTreeNode, maxdepth, parent_id="", parent_direction="_", depth=0):
    if node == "NIL":
        if depth < maxdepth:
            node_id = parent_id + parent_direction + "NIL"
            if show_nil_nodes:
                dot.node(node_id, "NIL", ordering="out", fixedsize="True", fillcolor="none",
                         style="filled", fontcolor="black", color="none", fontname="Arial Bold")
                dot.edge(parent_id, node_id, weight="0")
            else:
                dot.node(node_id, "", ordering="out",
                         fixedsize="True", style="invis")
                dot.edge(parent_id, node_id, weight="0", style="invis")
            _draw_subtree(dot, show_nil_nodes, "FILLER",
                          maxdepth, node_id, "<", depth+1)
            _draw_subtree(dot, show_nil_nodes, "FILLER",
                          maxdepth, node_id, "_", depth+1)
            _draw_subtree(dot, show_nil_nodes, "FILLER",
                          maxdepth, node_id, ">", depth+1)
        return
    elif node == "FILLER":
        if depth < maxdepth:
            node_id = parent_id + parent_direction + "FILLER"
            dot.node(node_id, "", ordering="out",
                     fixedsize="True", style="invis")
            dot.edge(parent_id, node_id, weight="1000", style="invis")
        return
    value = node.data
    balance = node.balance
    if balance > 0:
        sign = "+"
    elif balance < 0:
        sign = "-"
    else:
        sign = ""
    left = node.left
    right = node.right
    node_id = parent_id + parent_direction + str(value)
    try:
        color: str | None = str(node.get_color())
    except:
        color: str | None = None
    if (color):
        dot.node(node_id, f"{str(value)} ({sign}{abs(balance)})", ordering="out", fixedsize="True",
                 fillcolor=color, style="filled", fontcolor="white", fontname="Arial Bold")
    else:
        dot.node(node_id, f"{str(value)} ({sign}{abs(balance)})", ordering="out",
                 fixedsize="True", fontname="Arial Bold")
    if parent_id:
        dot.edge(parent_id, node_id, weight="0")
    _draw_subtree(dot, show_nil_nodes, "NIL" if not left else left,
                  maxdepth, node_id, "<", depth+1)
    _draw_subtree(dot, show_nil_nodes, "FILLER",
                  maxdepth, node_id, "_", depth+1)
    _draw_subtree(dot, show_nil_nodes, "NIL" if not right else right,
                  maxdepth, node_id, ">", depth+1)


def _generate_avl_tree_image(title, tree: AVLTreeNode, show_nil_nodes: bool) -> str | None:
    """Creates an image of the tree and returns it as a base64 encoded string of a pdf.
    """
    try:
        dot: graphviz.Digraph = graphviz.Digraph()
        dot.attr("graph", center="True", dpi="300", label=title, labelloc="t")
        treeroot = tree
        _draw_subtree(dot, show_nil_nodes, treeroot,
                      _get_tree_height(treeroot, show_nil_nodes))
        dot.format = "png"
        # Get image as binary
        tree_binary = dot.pipe()
        # Encode binary image as Base64
        return base64.b64encode(tree_binary).decode("utf-8")
    except Exception as e:
        raise e


def _visualize_tree(b64_image: str | None):
    if not b64_image:
        return
    img = Image.open(BytesIO(base64.b64decode(b64_image)))
    img.show()


def display_tree_image(title, tree: AVLTreeNode):
    _visualize_tree(_generate_avl_tree_image(
        title, tree, show_nil_nodes=False))

#####################################################################################################################


class Node:
    def __init__(self, data):
        self.data = data
        self.left: Node | None = None
        self.right: Node | None = None
        self.balance = 0

        self.parent = None

    def __repr__(self):
        return f"Node[{self.data},{self.balance}]"


class AVLT:
    def __init__(self, root=None):
        self.root: Node = root


def insert(node, data):
    curr_height_increased = False
    if not node:
        node = Node(data)
        curr_height_increased = True
    elif data < node.data:
        (node.left, child_height_increased) = insert(node.left, data)
        if child_height_increased:
            if node.balance == 1:
                if node.left.balance == 1:  # right rotation
                    # print("Right rotation at", node.data)
                    new_root = node.left
                    node.left = new_root.right
                    new_root.right = node
                    node = new_root
                    node.balance, node.right.balance = 0, 0
                else:  # left-right rotation
                    # print("Left-right rotation at", node.data)
                    new_root = node.left.right
                    node.left.right = new_root.left
                    new_root.left = node.left
                    node.left = new_root.right
                    new_root.right = node
                    node = new_root
                    node.left.balance = 1 if node.balance == -1 else 0
                    node.right.balance = -1 if node.balance == 1 else 0
                    node.balance = 0
            else:  # node.balance in [-1,0]:
                node.balance += 1
                if node.balance == 1:
                    curr_height_increased = True
    else:  # data >= node.data
        (node.right, child_height_increased) = insert(node.right, data)
        if child_height_increased:
            if node.balance == -1:
                if node.right.balance == -1:  # left rotation
                    # print("Left rotation at", node.data)
                    # Note for all four cases
                    # parallel assignment (in one line) does not work here
                    # - there are side effects due to the nested structure
                    # - parallel assignment works only for "primitive" data types (which can be calculated without side effects)
                    # this approach (which does not work) would look as follows:
                    # node, node.right, node.right.left = node.right, node.right.left, node
                    new_root = node.right
                    node.right = new_root.left
                    new_root.left = node
                    node = new_root
                    node.balance, node.left.balance = 0, 0
                else:  # right-left rotation
                    # print("Right-left rotation at", node.data)
                    new_root = node.right.left
                    node.right.left = new_root.right
                    new_root.right = node.right
                    node.right = new_root.left
                    new_root.left = node
                    node = new_root
                    node.left.balance = 1 if node.balance == -1 else 0
                    node.right.balance = -1 if node.balance == 1 else 0
                    node.balance = 0
            else:  # node.balance in [0,1]:
                node.balance -= 1
                if node.balance == -1:
                    curr_height_increased = True
    return (node, curr_height_increased)


def search(node, data) -> Node | None:
    if not node or data == node.data:
        return node  # not found or found
    elif data < node.data:
        return search(node.left, data)
    else:  # data >= node.data
        return search(node.right, data)


def delete(avlt: AVLT, data, DEBUG):
    if DEBUG:
        display_tree_image("Start", avlt.root)
    # Either parent of inorder successor of node to be deleted or previous left child of node to be deleted.
    impacted_by_delete = (None, 0)
    node = avlt.root
    predecessor = None
    # search for node to be deleted
    while (node and data != node.data):  # not found
        predecessor = node
        if data < node.data:
            node = node.left
        else:  # data >= node.data
            node = node.right
    if node:  # node is the element to be deleted
        if node.left and node.right:  # node with two children
            # if DEBUG:
            #    print("Case 1: Node with left and right children")
            # find minimum in right subtree
            pred_min_elem = node
            min_elem = pred_min_elem.right
            while min_elem.left:
                pred_min_elem = min_elem
                min_elem = min_elem.left
            # put minimum as root of current subtree
            # if DEBUG:
            #    print("Node:", node)
            #    print("Minimum:", min_elem)
            #    print("Pred Min Element", pred_min_elem)
            impacted_by_delete = (
                pred_min_elem, -1 if min_elem.data < pred_min_elem.data else +1)
            # (exchange values, unused node is returned)
            # if DEBUG:
            #    print("Case 1: BEFORE SWAP")
            #    display_tree_image("Case 1: BEFORE Swap", avlt.root)
            node.data, min_elem.data = min_elem.data, node.data
            # if DEBUG:
            #    print("Case 1: AFTER SWAP")
            #    display_tree_image("Case 1: After Swap", avlt.root)
            # delete element from subtree
            if pred_min_elem == node:
                node.right = min_elem.right
            else:
                pred_min_elem.left = min_elem.right
            # pred_min_elem.left = min_elem.right # TODO: Why? Line below should be correct
            # node.right = min_elem.right # TODO: Tried to fix line above by adding this but idk
            # min_elem.parent = pred_min_elem ### WRONG
            # return value
            # node = min_elem
        else:
            if node.left:  # node with left child only
                # if DEBUG:
                #    print("Case 2: Node with only left child")
                predecessor_link = node.left
                impacted_by_delete = (predecessor_link, -1)
            elif node.right:  # node with right child only
                # if DEBUG:
                #    print("Case 3: Node with only right child")
                predecessor_link = node.right
                impacted_by_delete = (predecessor_link, +1)
            else:  # leaf, not node.left and not node.right
                # if DEBUG:
                #    print("Case 4: Node with no children")
                predecessor_link = None
                impacted_by_delete = (predecessor_link, 0)
            if predecessor:
                # if DEBUG:
                #    print("Predecessor available")
                #    print("Node:", node)
                #    print("Predecessor:", predecessor)
                if node.data < predecessor.data:
                    impacted_by_delete = (predecessor, -1)
                    predecessor.left = predecessor_link
                    if predecessor_link:
                        predecessor_link.parent = predecessor
                else:
                    impacted_by_delete = (predecessor, +1)
                    predecessor.right = predecessor_link
                    if predecessor_link:
                        predecessor_link.parent = predecessor
            else:  # no predecessor available -> root
                # if DEBUG:
                #    print("No predecessor available --> root")
                # impacted_by_delete = (None, 0)
                if avlt.root:
                    previous_balance = avlt.root.balance
                avlt.root = predecessor_link
                if avlt.root:
                    avlt.root.balance = previous_balance
                    avlt.root.parent = None
    # Deleted node
    # if DEBUG:
    #    display_tree_image("Before Affected Node Adjustment", avlt.root); print("Before Affected Node Adjustment")
    #    print(impacted_by_delete)
    node_impacted_by_delete, balance_adjustment = impacted_by_delete
    if balance_adjustment == 0:
        return node
    node_impacted_by_delete.balance += balance_adjustment
    # node_impacted by delete is now fixed. All that is left to do, is fix all its ancesors.
    if DEBUG:
        display_tree_image("Before Rebalancing", avlt.root)
        print("Before Rebalancing")
    rebalance_after_delete(avlt, node_impacted_by_delete, DEBUG)
    if DEBUG:
        display_tree_image("Final", avlt.root)
        print("Final")
    return node


def rebalance_after_delete(avlt: AVLT, impacted_by_delete_node: Node, DEBUG):
    if DEBUG:
        print("Impacted by delete node:", impacted_by_delete_node)
    create_parent_links(avlt.root)  # TODO: Remove later
    node = impacted_by_delete_node
    while node is not None:
        if DEBUG:
            display_tree_image("While Loop Run Start", avlt.root)
            print("While Loop Run Start")
        predecessor = node.parent
        if node.balance == +1 or node.balance == -1:
            if DEBUG:
                print("Balance is +1 or -1. Should have no more effect above.")
            break
        elif node.balance == 0:
            if DEBUG:
                print("No need to rebalance this node, but bubble up changes.")
            if not predecessor:  # Node is root. Nothing to do
                break
            # Node is left child. Height of parent's left subtree was decreased by one.
            elif node.data < predecessor.data:
                predecessor.balance -= 1
                if DEBUG:
                    print("Bubbled up -1")
            else:  # Node is right child. Height of parent's right subtree was decreased by one.
                predecessor.balance += 1
                if DEBUG:
                    print("Bubbled up +1")
            node = node.parent
        else:  # Balance value is +2/-2 --> Rebalancing required
            if node.balance == 2:
                if node.left.balance >= 0:  # right rotation
                    is_case_one = node.left.balance == 0
                    if DEBUG:
                        print(
                            f"Node {node}: Rebalancing required. Right rotation required.")
                    new_root = node.left
                    node.left = new_root.right
                    new_root.right = node
                    node = new_root
                    if is_case_one:
                        node.balance = -1
                        node.right.balance = +1
                    else:
                        node.balance = 0
                        node.right.balance = 0
                else:  # left-right rotation
                    # TODO: Probably wrong? Have not checked
                    if DEBUG:
                        print(
                            f"Node {node}: Rebalancing required. Left-right rotation required.")
                    new_root = node.left.right
                    node.left.right = new_root.left
                    new_root.left = node.left
                    node.left = new_root.right
                    new_root.right = node
                    node = new_root
                    node.left.balance = 1 if node.balance == -1 else 0
                    node.right.balance = -1 if node.balance == 1 else 0
                    node.balance = 0
            elif node.balance == -2:
                if node.right.balance <= 0:  # Left rotation
                    is_case_one = node.right.balance == 0
                    if DEBUG:
                        print(
                            f"Node {node}: Rebalancing required. Left rotation required.")
                        display_tree_image("Before left rotation", avlt.root)
                        print("Before left rotation")
                    new_root = node.right
                    node.right = new_root.left
                    new_root.left = node
                    node = new_root
                    # node.balance, node.left.balance = 0, 0
                    if is_case_one:
                        node.balance = +1
                        node.left.balance = -1
                    else:
                        node.balance = 0
                        node.left.balance = 0
                else:  # right-left rotation
                    if DEBUG:
                        print(
                            f"Node {node}: Rebalancing required. Right-left rotation required.")
                        display_tree_image(
                            "Before right-left rotation", avlt.root)
                        print("Before right-left rotation")
                    new_root = node.right.left
                    node.right.left = new_root.right
                    new_root.right = node.right
                    node.right = new_root.left
                    new_root.left = node
                    node = new_root
                    node.left.balance = 1 if node.balance == -1 else 0
                    node.right.balance = -1 if node.balance == 1 else 0
                    node.balance = 0
            if predecessor is None:
                avlt.root = new_root
            elif new_root.data < predecessor.data:
                predecessor.left = new_root
            else:
                predecessor.right = new_root
        create_parent_links(avlt.root)
        # node = predecessor


################# Validating result ###############################

def create_parent_links(node: Node, backlink: Node | None = None):
    node.parent = backlink
    if node.left:
        create_parent_links(node.left, node)
    if node.right:
        create_parent_links(node.right, node)


def create_avl_tree(elements):
    avlt = AVLT()
    for elem in elements:
        avlt.root, _ = insert(avlt.root, elem)
    create_parent_links(avlt.root)
    return avlt


def count_nodes(node: Node) -> int:
    left_count = count_nodes(node.left) if node.left else 0
    right_count = count_nodes(node.right) if node.right else 0
    return left_count + right_count + 1


def check_node_count(avlt: AVLT, expected_node_count):
    if not avlt.root:
        if expected_node_count != 0:
            raise Exception(
                f"Expected node count was {expected_node_count} but there was no root")
    else:
        real_node_count = count_nodes(avlt.root)
        if expected_node_count != real_node_count:
            raise Exception(
                f"Mismatch between expected node count ({expected_node_count}) and real node count ({real_node_count})")
        return True


def check_values(node: Node, minimum=-inf, maximum=+inf) -> bool:
    if node.data <= minimum or node.data > maximum:
        raise Exception(
            f"Node {node.data} does not fit in ({str(minimum)}, {str(maximum)}]")
    is_left_correct = check_values(
        node.left, minimum, node.data) if node.left else True
    is_right_correct = check_values(
        node.right, node.data, maximum) if node.right else True
    return is_left_correct and is_right_correct


def get_height_of_subtree(node: Node, size=0) -> int:
    left_height = get_height_of_subtree(
        node.left, size+1) if node.left else size+1
    right_height = get_height_of_subtree(
        node.right, size+1) if node.right else size+1
    return max(left_height, right_height)


def check_balance(node: Node) -> bool:
    if node.balance > 1 or node.balance < -1:
        raise Exception(
            f"Node {node.data} does not have a balance value in [-1, +1]: {node.balance}")
    left_size = get_height_of_subtree(node.left) if node.left else 0
    right_size = get_height_of_subtree(node.right) if node.right else 0
    real_balance = left_size - right_size
    if node.balance != real_balance:
        raise Exception(
            f"Node {node.data} has a mismatch between assigned balance ({str(node.balance)}) and real balance ({str(real_balance)})")
    is_left_correct = check_balance(node.left) if node.left else True
    is_right_correct = check_balance(node.right) if node.right else True
    return is_left_correct and is_right_correct


def validate_tree(avlt: AVLT, expected_node_count) -> bool:
    node_count_ok = check_node_count(avlt, expected_node_count)
    if expected_node_count == 0:
        return node_count_ok
    values_ok = check_values(avlt.root)
    balance_ok = check_balance(avlt.root)
    return node_count_ok and values_ok and balance_ok

###################################################################


############### Checking permutations and sampling #########################################

def test_deletion_case(elements, node_to_be_deleted, allow_debug_information=False) -> bool:
    avlt = create_avl_tree(elements)
    original = deepcopy(avlt)
    try:
        delete(avlt, node_to_be_deleted, allow_debug_information)
    except Exception as e:
        print("Deletion Error:", str(e))
        print(traceback.format_exc())
        print(f"elements: {elements}; Deleted: {node_to_be_deleted}")
        exit()
    try:
        return validate_tree(avlt, expected_node_count=len(elements)-1)
    except Exception as e:
        print("Validation Error:", str(e))
        print(traceback.format_exc())
        print(f"elements: {elements}; Deleted: {node_to_be_deleted}")
        exit()


def test_specific(elements, node_to_be_deleted):
    print("TESTING SPECIFIC PERMUTATION!")
    test_deletion_case(elements, node_to_be_deleted,
                       allow_debug_information=True)


def test_permutations_single_threaded(max_size):
    print(
        f"Checking all permutations up until size {max_size} (Single-threaded)")
    for permutation_size in range(1, max_size+1):
        perms = list(permutations(
            range(1, permutation_size+1), permutation_size))
        for perm in perms:
            for node in perm:
                test_deletion_case(perm, node, allow_debug_information=False)
    print(f"Everything seems okay up until a permutation size of {max_size}")
    exit()


def test_permutations_multi_threaded(max_size, start_from=1):
    print(
        f"Checking permutations from {start_from} up until size {max_size} (Multi-threaded)")
    if start_from <= 6:
        for permutation_size in range(start_from, min(max_size, 6)+1):
            perms = list(permutations(
                range(1, permutation_size+1), permutation_size))
            for perm in perms:
                for node in perm:
                    test_deletion_case(
                        perm, node, allow_debug_information=False)
            print(f"Permutation size {permutation_size} okay")
    if max_size > 6:
        for permutation_size in range(max(7, start_from), max_size+1):
            combos = []
            perms = list(permutations(
                range(1, permutation_size+1), permutation_size))
            for perm in perms:
                for node in perm:
                    combos.append((perm, node))
            with Pool(processes=cpu_count()) as pool:
                results = []
                for (perm, node) in combos:
                    result = pool.apply_async(
                        test_deletion_case,
                        args=(perm, node, False),
                    )
                    results.append(result)
                with tqdm(total=len(results)) as pbar:
                    pbar.set_description_str(
                        f"Checking permutation size {permutation_size}")
                    for r in results:
                        r.get()
                        pbar.update(1)
            print(f"Permutation size {permutation_size} okay")
    print(
        f"Everything seems okay for permutation size(s) [{start_from}, {max_size}]")
    exit()


def test_random_samples(count, min_permutation_size, max_permutation_size):
    combos = []
    for _ in range(count):
        random_permutation_size = randint(
            min_permutation_size, max_permutation_size)
        elements = sample(
            list(range(1, random_permutation_size+1)), random_permutation_size)
        node_to_be_deleted = choice(elements)
        combos.append((elements, node_to_be_deleted))
    with Pool(processes=cpu_count()) as pool:
        results = []
        for (perm, node) in combos:
            result = pool.apply_async(
                test_deletion_case,
                args=(perm, node, False),
            )
            results.append(result)
        with tqdm(total=len(results)) as pbar:
            pbar.set_description_str(f"Checking random samples")
            for r in results:
                r.get()
                pbar.update(1)
    print(f"{count} operations were tested and there was no problem.")
    exit()

############################################################################################


if __name__ == "__main__":
    # Test all permutations of size [1, 9]
    # test_permutations_multi_threaded(9)

    # Test a specific operation. First argument is list of elements in order to be inserted into an initially empty AVL-tree using insert().
    # Second argument is the value to be deleted
    # test_specific([3, 10, 15, 25, 17, 2, 20, 6, 14, 16, 7, 24, 23, 19, 13, 8, 5, 26, 21, 12, 22, 4, 1, 18, 11, 9], 10)

    # Generate one million random samples where each sample has 10-50 elements and where one random element is to be deleted
    test_random_samples(1_000_000, 10, 50)

# Checked all permutations up until (including) 9
# Permutations of size >= 10 cannot even be calculated (not enough computational resources to generate all permutations)
# Checked many random samples with sizes [10, 50]


# TODO:
# - Remove reliance on create_parent_links()
#   - Right now this function is called multiple times to avoid problems of outdated parent-links
#   - Check all places where left-/right child is changed and update parent accordingly
# - Cleanup code
#   - Make code more concise, summarize parts, add comments, refactor parts
#   - Remove Debug statements
# - Add deletion algorithm itself into original file (once it is done) and keep this file for testing
