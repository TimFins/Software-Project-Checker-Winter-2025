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


def delete(avlt, data):
    print("Not implemented")
    return None
