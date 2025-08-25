# Priority Queues – Overview

Within this directory you will find a python implementation for priority queues which you can later on use to create your implementation. Please note that probably not all functions listed below, which are typically used for priority queues, are implemented. Additionally, the implementation of the priority queue in this directory will be different to the one you will create later on because the data structure you will be using is predefined and different to the one in here. Logically, it will be exactly the same.

Please have a look into the implementation and play around with it.

A **priority queue** is an abstract data structure similar to a regular queue,  
but each element has a *priority*.  
Instead of strictly FIFO order, elements with higher priority are dequeued first.

## Key Properties
- Each element is associated with a **priority**. In our scenario the **value and the priority are equal**.
- Higher (or lower, depending on implementation) priority determines order of removal.
- Implemented as a **binary heap** stored in a tree-like structure. In this code example it is implemented via an array but later on, you will implement it via **binary heaps**.
- Maintains the **heap property**:
  - **Max-Heap**: Parent ≥ Children  
    - Used to implement a **Max-Priority-Queue**, where the element with the **highest priority value** is always at the root and is removed first.
  - **Min-Heap**: Parent ≤ Children  
    - Used to implement a **Min-Priority-Queue**, where the element with the **lowest priority value** is always at the root and is removed first.

## Core Functions

### 1. `insert(value)`
- Adds a new element with the given priority.
- In a heap-based implementation:  
  - Add at the end and bubble up to maintain heap order.

### 2. `extract_max()` / `extract_min()`
- Removes and returns the element with the **highest** (or lowest) priority.  
- In a heap:
  - Replace root with last element.
  - Bubble down to restore heap property.

### 3. `increase_priority(element, new_priority)`
- Updates the priority of an existing element.