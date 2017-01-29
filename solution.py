assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def zip_strings(a, b):
    "Combine the array of strings into one array with respective elements merged."
    combined = list(a)
    for i in range(len(a)):
        combined[i] = a[i] + b[i]
    return combined

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [zip_strings(rows, cols), zip_strings(rows, cols[::-1])]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        two_boxes = [box for box in unit if len(values[box]) == 2]
        twin_boxes = []
        for box1 in two_boxes:
            for box2 in two_boxes:
                if box1 != box2 and values[box1] == values[box2]:
                    twin_boxes.append(box1)

        twin_boxes = list(set(twin_boxes))
        if len(twin_boxes) == 2:
            digits = values[twin_boxes[0]]
            for unit_box in unit:
                new_value = ''.join(sorted(list(set(values[unit_box]) - set(digits))))
                if(len(new_value) > 0 and len(values[unit_box]) != len(new_value)):
                    values = assign_value(values, unit_box, new_value)

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    "Uses the solved boxes' values to eliminate the digits from the peers."
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """
    Looks through the boxes in each unit for digits that only
    appear once and assigns that value to the box.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Repeats the eliminate, only_choice and naked_twins steps
    untill the puzzle cannot be reduced any further.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    new_values = values.copy()
    # print(sorted(new_values, key=lambda k: len(new_values[k])))
    new_values = reduce_puzzle(new_values)
    # sorted = sorted(new_values, key=lambda k: len(new_values[k]))
    if new_values:
        # Choose one of the unfilled squares with the fewest possibilities
        unsolved_boxes = [box for box in new_values.keys() if len(new_values[box]) > 1]
        if len(unsolved_boxes) == 0:
            return new_values

        # Now use recursion to solve each one of the resulting sudokus,
        else:
            # sort by length of options
            chosen_box = unsolved_boxes[0]
            for d in new_values[chosen_box]:
                # pick a value
                new_values = assign_value(new_values, chosen_box, d)
                # do it again
                resulting_values = search(new_values)

                # and if one returns a value (not False), return that answer!
                if resulting_values:
                    return resulting_values
    else:
        return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
