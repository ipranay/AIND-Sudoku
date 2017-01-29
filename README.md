# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
**How do we use constraint propagation to solve the naked twins problem?**

To solve the naked twins problem:

* We start with iterating over the unit list find boxes that have ony two digits in them `two_boxes`.
* Then we look at these boxes to find the boxes that have the same value `twin_boxes`.
* Next we remove any duplicates in `twin_boxes`.
* Now, we find all peers for these `twin_boxes`, within the `unit`.
* And remove the twin digits from those.


# Question 2 (Diagonal Sudoku)
**How do we use constraint propagation to solve the diagonal sudoku problem?**

Solving diagonal sudoku was very, given that all the other peices were in place

* We create a new function called `zip_strings` to create the diagonal units
* Once we have these units `diagonal_units` in place, we add them to the list of units `unit_list`

And that's it. Our `reduce_puzzle` function, automatically takes this new constraint into account.

### Steps

1. Activate conda environment

  ```bash
  source activate aind
  ```

2. Write a program for constraint propagation for:

  a. naked twins problem

  b. diagonal sudoku problem

### Visualizing

To visualize the solution, we use the `assign_values` function whenever changing values.

To run the visualization, use 

```bash
python solution.py
```

### Data

The data consists of a text file of diagonal sudokus for you to solve.
