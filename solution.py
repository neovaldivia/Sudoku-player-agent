assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
 
diagonal1 = [[a[0]+a[1] for a in zip(rows,cols)]]
diagonal2 = [[a[0]+a[1] for a in zip(rows,cols[::-1])]]
diagonals = diagonal1 + diagonal2
#print(diagonals)

unitlist = row_units + column_units + square_units + diagonals
print(unitlist)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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

    # Find lists of boxes in the same *unit, with *len()=2 
    unit_boxes_2digits = [[box for box in unit if len(values[box]) == 2] for unit in unitlist]
    #print(unit_boxes_2digits)
    
    #only units with 2 boxes presenting 2 digits can be twins if they have the same digits
    unit_2boxes_2digits = [i for i in unit_boxes_2digits if len(i)==2]
    #print(unit_2boxes_2digits)
    
    #Now we need to compare values
    naked_twins = [i for i in unit_2boxes_2digits if values[i[0]]==values[i[1]]]
    #print(naked_twins)
            
    # Eliminate the naked twins as possibilities for their peers
    for box1,box2 in naked_twins:
        digits = values[box1]
        common_peers = list(peers[box1] & peers[box2])
        for peer in common_peers:
            if len(values[peer])>1 and peer!=box1 and peer!=box2:
                values[peer]= values[peer].replace(digits[0],'')
                values[peer]= values[peer].replace(digits[1],'')

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
    grid = ['123456789' if i=='.' else i for i in  list(grid)]
    return dict(zip(boxes,grid))

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
    return

def eliminate(values):
    single_boxes = [i for i in values.keys() if len(values[i])==1]
    
    for box in single_boxes:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            d_place = [box for box in unit if digit in values[box]]
            if len(d_place)==1:
                values[d_place[0]]=digit
    return values

def reduce_puzzle(values):
    #reduce with eliminate and only_choice ********************should I use naked twins?
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        # Your code here: Use the Eliminate Strategy
        values=eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values=only_choice(values)
        
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values=grid_values(grid)
    return search(values)
    
    


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
