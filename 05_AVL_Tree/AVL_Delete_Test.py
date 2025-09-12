try:
    import graphviz
    from PIL import Image
except:
    pass
import base64
from io import BytesIO
from itertools import permutations
from math import inf
from copy import deepcopy
import traceback
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from random import choice, sample, randint

######################### Visualization #############################################################################


def _get_tree_height(node, show_nil_nodes: bool):
    left = node.left
    right = node.right
    left_height = (1 if show_nil_nodes else 0) if left is None else _get_tree_height(
        left, show_nil_nodes)
    right_height = (1 if show_nil_nodes else 0) if right is None else _get_tree_height(
        right, show_nil_nodes)
    return max(left_height, right_height) + 1


def _draw_subtree(dot: graphviz.Digraph, show_nil_nodes: bool, node, maxdepth, parent_id="", parent_direction="_", depth=0):
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


def _generate_avl_tree_image(title, tree, show_nil_nodes: bool) -> str | None:
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
    try:
        if not b64_image:
            return
        img = Image.open(BytesIO(base64.b64decode(b64_image)))
        img.show()
    except:
        pass


def display_tree_image(title, tree):
    try:
        _visualize_tree(_generate_avl_tree_image(
            title, tree, show_nil_nodes=False))
    except:
        pass

#####################################################################################################################


class Node:
    def __init__(self, data):
        self.data = data
        self.left: Node | None = None
        self.right: Node | None = None
        self.balance = 0
        # backlink to parent is necesarry for deletion but not used in insertion
        self.parent = None

    def __repr__(self):
        return f"Node[{self.data},{self.balance}]"


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


def delete(root: Node, data):
    # keep track of which node is the first node that requires an adjustment and how it should be adjusted
    impacted_by_delete = (None, 0)
    predecessor = None
    node = root
    # search for node to be deleted
    while (node and data != node.data):  # not found
        predecessor = node
        if data < node.data:
            node = node.left
        else:  # data >= node.data
            node = node.right
    if node:  # node is the element to be deleted
        if node.left and node.right:  # node with two children
            # find minimum in right subtree
            pred_min_elem = node
            min_elem = pred_min_elem.right
            while min_elem.left:
                pred_min_elem = min_elem
                min_elem = min_elem.left
            # keep track of whether the minimum was taken from its parent's left or right side
            # the balance has to be adjusted accordingly later, since the given side shrunk
            # and therefore the balance shifts
            if min_elem.data < pred_min_elem.data:
                impacted_by_delete = (pred_min_elem, -1)
            else:
                impacted_by_delete = (pred_min_elem, +1)
            # put minimum as root of current subtree
            # exchange values. Balance and connections remain unaffected
            node.data, min_elem.data = min_elem.data, node.data
            # delete element from subtree
            if pred_min_elem == node:
                node.right = min_elem.right
                if min_elem.right:
                    min_elem.right.parent = node
            else:
                pred_min_elem.left = min_elem.right
                if min_elem.right:
                    min_elem.right.parent = pred_min_elem
        else:
            if node.left:  # node with left child only
                predecessor_link = node.left
                impacted_by_delete = (predecessor_link, -1)
            elif node.right:  # node with right child only
                predecessor_link = node.right
                impacted_by_delete = (predecessor_link, +1)
            else:  # leaf, not node.left and not node.right
                predecessor_link = None
                impacted_by_delete = (predecessor_link, 0)
            if predecessor:
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
                if predecessor_link:
                    predecessor_link.balance = root.balance
                    predecessor_link.parent = None
                root = predecessor_link
    # first affected node and how its balance is to be shifted
    node_impacted_by_delete, balance_adjustment = impacted_by_delete
    # if there is no balance adjustment, then the deletion had no impact and
    # no further rebalancing is required
    if balance_adjustment == 0:
        return root
    # adjust balance value
    node_impacted_by_delete.balance += balance_adjustment
    # node impacted by delete is now fixed. All that is left to do, is fix all its ancesors
    root = rebalance_after_delete(root, node_impacted_by_delete)
    return root


def rebalance_after_delete(root: Node, node_impacted_by_delete: Node):
    node = node_impacted_by_delete
    while node is not None:
        predecessor = node.parent
        # height did not change and there are no further effects upstream --> rebalancing complete
        if node.balance == +1 or node.balance == -1:
            break
        # node does not need to be rebalanced but height decreased, therefore bubble up changes to parent
        elif node.balance == 0:
            if not predecessor:  # node is root --> rebalancing complete
                break
            # node is left child, therefore height of parent's left subtree was decreased by one
            elif node.data < predecessor.data:
                predecessor.balance -= 1
            # node is right child, therefore height of parent's right subtree was decreased by one
            else:
                predecessor.balance += 1
            node = node.parent
        else:  # balance value is +2/-2 --> rebalancing required
            if node.balance == 2:  # subtree is left-leaning
                if node.left.balance >= 0:  # right rotation
                    new_root = node.left
                    node.left = new_root.right
                    if new_root.right:
                        new_root.right.parent = node
                    new_root.right = node
                    node.parent = new_root
                    node = new_root
                    # case 1: balance of new subtree root was zero --> cannot be balanced evenly
                    if node.balance == 0:
                        node.balance = -1
                        node.right.balance = +1
                    # case 2: balance of new subtree root was 1 --> can be balanced evenly
                    else:
                        node.balance = 0
                        node.right.balance = 0
                else:  # left-right rotation
                    new_root = node.left.right
                    node.left.right = new_root.left
                    if new_root.left:
                        new_root.left.parent = node.left
                    new_root.left = node.left
                    if node.left:
                        node.left.parent = new_root
                    node.left = new_root.right
                    if new_root.right:
                        new_root.right.parent = node
                    new_root.right = node
                    node.parent = new_root
                    node = new_root
                    node.left.balance = 1 if node.balance == -1 else 0
                    node.right.balance = -1 if node.balance == 1 else 0
                    node.balance = 0
            elif node.balance == -2:  # subtree is right-leaning
                if node.right.balance <= 0:  # Left rotation
                    new_root = node.right
                    node.right = new_root.left
                    if new_root.left:
                        new_root.left.parent = node
                    new_root.left = node
                    node.parent = new_root
                    node = new_root
                    # case 1: balance of new subtree root was zero --> cannot be balanced evenly
                    if node.balance == 0:
                        node.balance = +1
                        node.left.balance = -1
                    # case 2: balance of new subtree root was -1 --> can be balanced evenly
                    else:
                        node.balance = 0
                        node.left.balance = 0
                else:  # right-left rotation
                    new_root = node.right.left
                    node.right.left = new_root.right
                    if new_root.right:
                        new_root.right.parent = node.right
                    new_root.right = node.right
                    if node.right:
                        node.right.parent = new_root
                    node.right = new_root.left
                    if new_root.left:
                        new_root.left.parent = node
                    new_root.left = node
                    node.parent = new_root
                    node = new_root
                    node.left.balance = 1 if node.balance == -1 else 0
                    node.right.balance = -1 if node.balance == 1 else 0
                    node.balance = 0
            # Since the root of the subtree changed after rebalancing,
            # the new root has to be properly connected to its ancestors
            if predecessor is None:  # no predecessor --> root of subtree is root of tree
                root = node
                node.parent = None
            # connect root of subtree as left child of predecessor
            elif new_root.data < predecessor.data:
                predecessor.left = node
                node.parent = predecessor
            # connect root of subtree as right child of predecessor
            else:
                predecessor.right = node
                node.parent = predecessor
    return root

################# Validating result ###############################


def create_parent_links(node: Node, backlink: Node | None = None):
    node.parent = backlink
    if node.left:
        create_parent_links(node.left, node)
    if node.right:
        create_parent_links(node.right, node)


def create_avl_tree(elements):
    root = None
    for elem in elements:
        root, _ = insert(root, elem)
    create_parent_links(root)
    return root


def count_nodes(node: Node) -> int:
    left_count = count_nodes(node.left) if node.left else 0
    right_count = count_nodes(node.right) if node.right else 0
    return left_count + right_count + 1


def check_node_count(root: Node, expected_node_count):
    if not root:
        if expected_node_count != 0:
            raise Exception(
                f"Expected node count was {expected_node_count} but there was no root")
    else:
        real_node_count = count_nodes(root)
        if expected_node_count != real_node_count:
            raise Exception(
                f"Mismatch between expected node count ({expected_node_count}) and real node count ({real_node_count})")
        return True


def check_values(node: Node, minimum=-inf, maximum=+inf) -> bool:
    if node.data < minimum or node.data > maximum:
        raise Exception(
            f"Node {node.data} does not fit in [{str(minimum)}, {str(maximum)}]")
    is_left_correct = check_values(
        node.left, minimum, node.data-1) if node.left else True
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


def validate_tree(root: Node, expected_node_count) -> bool:
    node_count_ok = check_node_count(root, expected_node_count)
    if expected_node_count == 0:
        return node_count_ok
    values_ok = check_values(root)
    balance_ok = check_balance(root)
    return node_count_ok and values_ok and balance_ok

###################################################################


############### Checking permutations and sampling #########################################

def test_deletion_case(elements, node_to_be_deleted) -> bool:
    root = create_avl_tree(elements)
    original = deepcopy(root)
    try:
        root = delete(root, node_to_be_deleted)
    except Exception as e:
        print("Deletion Error:", str(e))
        print(traceback.format_exc())
        print(f"elements: {elements}; Deleted: {node_to_be_deleted}")
        exit()
    try:
        return validate_tree(root, expected_node_count=len(elements)-1)
    except Exception as e:
        print("Validation Error:", str(e))
        print(traceback.format_exc())
        print(f"elements: {elements}; Deleted: {node_to_be_deleted}")
        exit()


def test_specific(elements, node_to_be_deleted):
    print("TESTING SPECIFIC PERMUTATION!")
    test_deletion_case(elements, node_to_be_deleted)


def test_permutations_single_threaded(max_size):
    print(
        f"Checking all permutations up until size {max_size} (Single-threaded)")
    for permutation_size in range(1, max_size+1):
        perms = list(permutations(
            range(1, permutation_size+1), permutation_size))
        for perm in perms:
            for node in perm:
                test_deletion_case(perm, node)
    print(f"Everything seems okay up until a permutation size of {max_size}")


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
                        perm, node)
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
                        args=(perm, node),
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


def test_random_samples(count, min_permutation_size, max_permutation_size):
    print("Generating random samples...")
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
                args=(perm, node),
            )
            results.append(result)
        with tqdm(total=len(results)) as pbar:
            pbar.set_description_str(
                f"Checking random samples (Multi-threaded)")
            for r in results:
                r.get()
                pbar.update(1)
    print(f"{count} operations were tested and there was no problem.")

############################################################################################


if __name__ == "__main__":
    # Simple example of usage
    elements = [1, 2, 3]
    # Tree is initially empty (None)
    root = None
    # Insert values
    for element in elements:
        # It is very important to write the assignment as "root, _" because insert()
        # returns a tuple but only the first return value (the root) is of relevance
        root, _ = insert(root, element)
    # The insert() function does not create .parent backlinks for the nodes
    # But the deletion algorithm requires them to be present
    # So either modify insert() to update parent links or set them all at once after insertion
    create_parent_links(root)
    # Now delete the desired value
    root = delete(root, 2)

    # Test all permutations of size [1, 9]
    # test_permutations_multi_threaded(9)

    # Test a specific operation. First argument is list of elements in order to be inserted into an initially empty AVL-tree using insert().
    # Second argument is the value to be deleted
    # test_specific([3, 10, 15, 25, 17, 2, 20, 6, 14, 16, 7, 24, 23, 19, 13, 8, 5, 26, 21, 12, 22, 4, 1, 18, 11, 9], 10)

    # Generate 100,000 random samples where each sample has 1-100 elements and where one random element is to be deleted
    test_random_samples(100_000, 1, 100)


# NOTE:
# - Checked all permutations up until (including) a size of 9
# - Permutations of size >= 10 cannot even be calculated (not enough computational resources to generate all permutations)
# - Checked many (in the millions) random samples with sizes [10, 100]
# - The deletion code could probably be simplified further
# - Duplicates should be illegal. Just inserting the values (1, 1, 1) violates either AVL-tree rules or duplicate rules
#   - With two different values 1 and 2, 1 <= 2 and 2 > 1 holds
#   - With two duplicates 1 and 1, 1 <= 1 hold but 1 > 1 does not hold
#   - Values must ALWAYS be the right child of their respective duplicate parent
