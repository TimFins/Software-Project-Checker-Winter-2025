from binarytrees import RedBlackTreeNode, RedBlackTreeColor


class RedBlackTree():
    def __init__(self, root: RedBlackTreeNode | None):
        self.root = root


def insert_values_into_red_black_tree(existing_tree: RedBlackTreeNode, values: list[int]) -> RedBlackTreeNode:
    solution = RedBlackTree(existing_tree)
    for value in values:
        insert_into_red_black_tree(solution, value)
    return solution.root


def insert_into_red_black_tree(rbt: RedBlackTree, data: int):
    if not rbt.root:
        # root is always black, no rebalancing required
        rbt.root = RedBlackTreeNode(data, RedBlackTreeColor.BLACK)
    else:
        node = rbt.root
        predecessor = None
        while (node):
            predecessor = node
            if data < node._value:
                node = node._left
            else:  # data >= node._value
                node = node._right
        new_node = RedBlackTreeNode(data, RedBlackTreeColor.RED)
        if data < predecessor._value:
            predecessor._left = new_node
        else:  # data >= predecessor._value
            predecessor._right = new_node
        new_node._parent = predecessor
        red_black_tree_balance(rbt, new_node)


def red_black_tree_balance(rbt: RedBlackTree, node: RedBlackTreeNode):
    if not node._parent:
        rbt.root = node
        node.set_color(RedBlackTreeColor.BLACK)  # node is root of tree
        return
    if node._color == RedBlackTreeColor.RED and node._parent._color == RedBlackTreeColor.RED:
        if node._parent._value < node._parent._parent._value:
            if node._value < node._parent._value:  # case 1
                x, y, z = node, node._parent, node._parent._parent
                y._right, z._left = z, y._right
                y._parent, z._parent = z._parent, y
            else:  # node._value >= node._parent._value, case 2
                x, y, z = node._parent, node, node._parent._parent
                x._right, y._left, y._right, z._left = y._left, x, z, y._right
                x._parent, y._parent, z._parent = y, z._parent, y
                if x._right:  # subtree b
                    x._right._parent = x
            if z._left:  # subtree c
                z._left._parent = z
        else:  # node._parent._value >= node._parent._parent._value
            if node._value < node._parent._value:  # case 3
                x, y, z = node._parent._parent, node, node._parent
                x._right, y._left, y._right, z._left = y._left, x, z, y._right
                x._parent, y._parent, z._parent = y, x._parent, y
                if z._left:  # subtree c
                    z._left._parent = z
            else:  # node._value >= node._parent._value, case 4
                x, y, z = node._parent._parent, node._parent, node
                x._right, y._left = y._left, x
                x._parent, y._parent = y, x._parent
            if x._right:  # subtree b
                x._right._parent = x
        # for all cases
        x.set_color(RedBlackTreeColor.BLACK)
        y.set_color(RedBlackTreeColor.RED)
        z.set_color(RedBlackTreeColor.BLACK)
        if y._parent:
            if y._value < y._parent._value:
                y._parent._left = y
            else:
                y._parent._right = y
        red_black_tree_balance(rbt, y)


def get_red_black_tree_repair_checkpoints(existing_tree: RedBlackTreeNode) -> list[RedBlackTreeNode]:
    """Get the checkpoints of the repair process as a list. The first element is is the existingTree. 
    The second element is having one repair step applied to the existing tree. And so on.
    The last element is the actual solution.
    """
    rbt = RedBlackTree(existing_tree)
    checkpoints = []
    node_to_balance, _ = find_node_causing_violation(rbt.root)
    further_rebalancing_needed = True
    while further_rebalancing_needed:
        further_rebalancing_needed, node_to_balance = red_black_tree_balance_with_checkpoints(
            rbt, node_to_balance)
        checkpoints.append(rbt.root.deep_copy())
    return checkpoints


def find_node_causing_violation(root: RedBlackTreeNode) -> tuple[RedBlackTreeNode, str]:
    """Finds the node responsible for a RBT violation.
    If the violation is a red-red violation, then node to search for should always be the deepest red-red violation,
    since red-red violations are bubbled up, the fixing has to start with the violation deepest in the tree.
    The only other violation would be having a red root.
    """
    nodes = root.postorder_traverse()
    for node in nodes:
        if node.get_parent():
            if node.get_color() == RedBlackTreeColor.RED and node.get_parent().get_color() == RedBlackTreeColor.RED:
                return node, "RED_RED"
    if root.get_color() == RedBlackTreeColor.RED:
        return root, "RED_ROOT"
    raise ValueError("No red-black property violation found...")


def red_black_tree_balance_with_checkpoints(rbt: RedBlackTree, node: RedBlackTreeNode) -> tuple[bool, (RedBlackTreeNode | None)]:
    """Red-black tree rebalancing function, which does not work recursively.
    Instead it returns a flag whether further rebalancing is necessary and if so, which node it should be called on.
    """
    if not node._parent:
        rbt.root = node
        node.set_color(RedBlackTreeColor.BLACK)  # node is root of tree
        return False, None
    if node._color == RedBlackTreeColor.RED and node._parent._color == RedBlackTreeColor.RED:
        if node._parent._value < node._parent._parent._value:
            if node._value < node._parent._value:  # case 1
                x, y, z = node, node._parent, node._parent._parent
                y._right, z._left = z, y._right
                y._parent, z._parent = z._parent, y
                # Check whether there is a new root.
                if y._parent is None:
                    rbt.root = y
                if z._parent is None:
                    rbt.root = z
            else:  # node._value >= node._parent._value, case 2
                x, y, z = node._parent, node, node._parent._parent
                x._right, y._left, y._right, z._left = y._left, x, z, y._right
                x._parent, y._parent, z._parent = y, z._parent, y
                # Check whether there is a new root.
                if x._parent is None:
                    rbt.root = x
                if y._parent is None:
                    rbt.root = y
                if z._parent is None:
                    rbt.root = z
                if x._right:  # subtree b
                    x._right._parent = x
            if z._left:  # subtree c
                z._left._parent = z
        else:  # node._parent._value >= node._parent._parent._value
            if node._value < node._parent._value:  # case 3
                x, y, z = node._parent._parent, node, node._parent
                x._right, y._left, y._right, z._left = y._left, x, z, y._right
                x._parent, y._parent, z._parent = y, x._parent, y
                # Check whether there is a new root.
                if x._parent is None:
                    rbt.root = x
                if y._parent is None:
                    rbt.root = y
                if z._parent is None:
                    rbt.root = z
                if z._left:  # subtree c
                    z._left._parent = z
            else:  # node._value >= node._parent._value, case 4
                x, y, z = node._parent._parent, node._parent, node
                x._right, y._left = y._left, x
                x._parent, y._parent = y, x._parent
                # Check whether there is a new root.
                if x._parent is None:
                    rbt.root = x
                if y._parent is None:
                    rbt.root = y
            if x._right:  # subtree b
                x._right._parent = x
        # for all cases
        x.set_color(RedBlackTreeColor.BLACK)
        y.set_color(RedBlackTreeColor.RED)
        z.set_color(RedBlackTreeColor.BLACK)
        if y._parent:
            if y._value < y._parent._value:
                y._parent._left = y
            else:
                y._parent._right = y
        return True, y
    else:
        return False, None
