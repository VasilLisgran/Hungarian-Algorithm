def hungarian_method_simplest(R):
    n = len(R)
    
    # Initial budgets (Cover)
    a = [max(R[i][j] for j in range(n)) for i in range(n)]
    b = [max(R[i][j] for i in range(n)) for j in range(n)]

    # If sum а <= sum b
    if sum(a) <= sum(b):
        u, v = a.copy(), [0] * n
    else:
        u, v = [0] * n, b.copy()

    # match_row[i] = j means, that in (i, j) is 1*
    match_row = [-1] * n  # On which job human i is assigned
    match_col = [-1] * n  # Which job j is assigned to human

    # Building the increasing sequence 
    def construct_sequence(j_curr, visited_rows, Q):
        for i in range(n):
            # If qualified and not checked yet 
            if Q[i][j_curr] == 1 and not visited_rows[i]:
                visited_rows[i] = True
                # "The routine then divides into two cases..." 
                # Is the employee busy right now?
                if match_row[i] != -1:
                    # His job now
                    j_next = match_row[i]
                    # We consider whether we can swap two people and whether we have already considered them
                    if construct_sequence(j_next, visited_rows, Q):
                        match_row[i] = j_curr
                        match_col[j_curr] = i
                        return True
                        # We’re inverting the 1 and 1* here, in the sense that we’re assigning someone to a new role and freeing them up from the old one.
                else:
                    # CASE 2: NO 1* in the row
                    # We’ve found the end of the path! We are converting 1 into 1* 
                    match_row[i] = j_curr
                    match_col[j_curr] = i
                    return True
        return False

    while True:
        # Creating a qualification matrix
        Q = [[1 if u[i] + v[j] == R[i][j] else 0 for j in range(n)] for i in range(n)]

        while True:
            augmented = False
            
            # "The computation begins with the search of each column of Q in turn for a 1*."
            for j0 in range(n):
                
                if match_col[j0] != -1:
                    # "If a 1* is found, we proceed to the next column"
                    continue
                
                # "If a 1* is not found... the column is eligible and is searched for a 1."
                found_one = False
                for i in range(n):
                    if Q[i][j0] == 1:
                        found_one = True
                        break
                
                if not found_one:
                    # "If a 1 is not found, we proceed to the next column"
                    continue
                
                # "If a 1 is found ... start a process that constructs a sequence"
                visited_rows = [False] * n
                if construct_sequence(j0, visited_rows, Q):
                    # If sequence built, start againg
                    augmented = True
                    break 

            if not augmented:
                break 

        # If a column has been assigned to all rows, the algorithm terminates.
        if -1 not in match_row:
            break

        # --- ROUTINE II
        visited_rows = [False] * n
        for j0 in range(n):
            if match_col[j0] == -1:
                construct_sequence(j0, visited_rows, Q) 
                # The person can be reached from a free job, meaning they are not critical
                # There exists a chain in which this person can participate in a rearrangement

        # Important row (person) – involved in the transfer
        ess_rows = [r for r in range(n) if visited_rows[r]]
        iness_rows = [r for r in range(n) if not visited_rows[r]]
        ess_cols = [match_row[r] for r in iness_rows if match_row[r] != -1]
        iness_cols = [c for c in range(n) if c not in ess_cols]

        d = min(u[r] + v[c] - R[r][c] for r in iness_rows for c in iness_cols)

        if all(u[r] > 0 for r in iness_rows): # Case 1
            m = min([d] + [u[r] for r in iness_rows])
            for r in iness_rows: u[r] -= m
            for c in ess_cols: v[c] += m
        else:                                 # Case 2
            m = min([d] + [v[c] for c in iness_cols])
            for r in ess_rows: u[r] += m
            for c in iness_cols: v[c] -= m

    return [(i + 1, match_row[i] + 1) for i in range(n)]

R = [[92, 64, 17, 83, 45, 71, 38, 56],
[23, 88, 45, 12, 67, 34, 89, 41],
[77, 35, 91, 28, 54, 66, 19, 73],
[44, 59, 12, 87, 33, 68, 92, 27],
[81, 16, 74, 45, 90, 22, 55, 68],
[33, 77, 54, 69, 28, 83, 41, 95],
[66, 43, 88, 31, 76, 59, 27, 84],
[50, 92, 35, 77, 43, 68, 71, 19]]
print(hungarian_method_simplest(R))