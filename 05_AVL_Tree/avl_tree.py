# AVL tree - insert, search, delete
#
# Software for educational purposes only. No warranty of any kind.
#
# Author: Jens Liebehenschel
# Copyright 2025

# Inspired by M. Nebel: Entwurf und Analyse von Algorithmen, 2012, p. 130-140
# recursive procedure, which simplifies rebalancing up to the root
# returns  tuple, the node and (True, if height increased, False otherwise)

# balance - allowed values
#  1 left subtree higher     [height(left subtree) = height(right subtree) + 1]
#  0 both subtrees same high [height(left subtree) = height(right subtree)]
# -1 right subtree higher    [height(left subtree) = height(right subtree) - 1]
# Note: balance := height (left subtree) - height (right subtree)

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.balance = 0
        # backlink to parent is necesarry for deletion but not used in insertion
        self.parent = None


class AVLT:
    def __init__(self, root=None):
        self.root = root


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


def search(node, data):
    if not node or data == node.data:
        return node  # not found or found
    elif data < node.data:
        return search(node.left, data)
    else:  # data >= node.data
        return search(node.right, data)


def delete(root, data):
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


def rebalance_after_delete(root, node_impacted_by_delete):
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
