"""Example usage of the AVLTreeNode class.
This file guides you through the most important methods of the AVLTreeNode class. Including how to create it, modify it and more.

To avoid the output from being overwhelming, after each console output you have to confirm by pressing the 'Enter' key before new output is shown.
For that purpose the '_wait_for_user_confirmation()' function is used here. Please ignore it.
"""

# Import the AVLTreeNode class
from datastructures.avltree import AVLTreeNode
# Import the json module for parsing the JSON string into a dictionary
import json


def _wait_for_user_confirmation(output_text):
    input(
        f"Please press 'Enter' to continue to continue past output {output_text}")


##############################
# 1. Creating an AVLTreeNode #
##############################

# This is an example for an input JSON, where there is just one node (hence balancing factor 0).
example_json = r"""{"value": 5, "balance": 0, "left": null, "right": null}"""

# Parse the JSON string into a Python dictionary using 'json.loads()'.
example_dictionary = json.loads(example_json)

# Now the dictionary needs to be converted into an AVLTreeNode object.
# For that, use the 'from_dict()' class method.
root = AVLTreeNode.from_dict(example_dictionary)

# If Graphviz is installed, the AVL tree can be visualized by calling 'display_avl_image(title)'
root.display_avl_image(
    "1.1 This is the initial AVL tree\ncontaining just '5' with balance value '0'.")
_wait_for_user_confirmation("1.1")


#############################
# 2. Modifying the AVL tree #
#############################

# If you want to add a node to the tree, create a new node and add it as a child of the root.
new_right_child = AVLTreeNode(value=10, balance=0)
root.set_right_child(new_right_child)

# The root's balance value is now wrong, since it is no longer zero.
# The balance value is not handled automatically and instead must be handled in the corresponding algorithms.
# So the balance value has to be adjusted manually (-1, since right subtree is now larger than left subtree by one).
# Note: balance := height (left subtree) - height (right subtree)
root.set_balance(-1)

root.display_avl_image(
    "2.1 Now a right child was added.\nThe root's balance was adjusted accordingly.")
_wait_for_user_confirmation("2.1")

# Now two nodes are added at the correct positions.
# One to the left of the root and one to the left of the root's right child.
# The balancing values are adjusted accordingly.
new_left_child = AVLTreeNode(value=1, balance=0)
root.set_left_child(new_left_child)

new_right_left_child = AVLTreeNode(value=7, balance=0)
root.get_right_child().set_left_child(new_right_left_child)

# The balance value of the root's right child is now outdated
root.get_right_child().set_balance(1)

root.display_avl_image(
    "2.2 Two nodes were added and the balance values were adjusted accordingly.")
_wait_for_user_confirmation("2.2")


#################################################
# 3. Creating a copy and comparing for equality #
#################################################

# Now create a copy, so it can be modified without affecting the original. Use the deep_copy() method for that.
root_copy = root.deep_copy()

# Change the value of the root's right child in the copy. 7 -> 8
root_copy.get_right_child().set_value(8)

# One can use the regular comparison operators to check if two nodes are equal (have the same value and balance value)
print("3.1 root.get_right_child() == root_copy.get_right_child() =",
      root.get_right_child() == root_copy.get_right_child())
# The result is: False. The node was modified and is therefore not equal to the original.
_wait_for_user_confirmation("3.1")

print("3.2 root == root_copy =", root == root_copy)
# The result is: True. While the right child of the root was modified, the root itself was not changed.
# So the roots are still equal.
_wait_for_user_confirmation("3.2")

# If you want to check whether two trees are equal (both nodes have the same value, balance value and all the children are the same),
# you can use the is_equal_including_subtrees() method.
print("3.3 root.is_equal_including_subtrees(root_copy) =",
      root.is_equal_including_subtrees(root_copy))
# The result is: False. While the root was not changed, it's right child was modified, therefore the two trees are no longer equal.
_wait_for_user_confirmation("3.3")


################
# 4. Traversal #
################

# You can traverse the tree manually by calling 'get_left_child()', 'get_right_child()' or 'get_parent()',
# but you can also traverse it in one the three traversal orders, which are methods returning a list of all nodes in the given order.
# The orders are preorder, inorder and postorder.
nodes_in_preorder = root.preorder_traverse()
nodes_in_inorder = root.inorder_traverse()
nodes_in_postorder = root.postorder_traverse()

print("4.1 Nodes in preorder:")
print(nodes_in_preorder)
