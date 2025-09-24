# AVL Trees – Overview

Within this directory you will find a python implementation for AVL trees which you can later use to create your implementation. Additionally, the implementation of AVL trees in this directory will be different to the one you will create later because the data structure you will be using is predefined and slightly more complex compared to the one in here. Logically, it will be exactly the same.

Please have a look into the implementation and try to solve the exercises with it. There is no need to solve all exercises if you already understand how AVL trees work.

An **AVL tree** is a type of self-balancing binary search tree (BST).  
It maintains the property that for every node, the height difference (balance value) between its left and right subtree is at most **1**.

## Key Properties
- **Binary Search Tree (BST) property**:  
    `Left child < Parent <= Right child`
- **Balance property**:  
    `|height(left) – height(right)| ≤ 1`

## Core Functions

### 1. `insert(value)`
- Insert a new node like in a BST.
- Update heights and balance values.
- Perform rotations if the balance values of any node becomes `-2` or `+2`.

### 2. `search(value)`
- Standard BST search:
    - Traverse left if value < current node.
    - Traverse right if value > current node.
    - Return node if found.

### 3. `delete(value)`
- Delete a given value from the tree
- Adjust balance values accordingly
- Perform rotations if necessary
- You can use the document `AVL_Delete_Idea.md` to get a clearer view of how deletion in AVL trees works conceptually.
