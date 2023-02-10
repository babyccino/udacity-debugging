#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# This provided, working code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the traceit
# function to work for function calls instead of lines. It should save the
# function name and the return value of the function for each function call.
# Use the mystery function that can be found at line TODO 155 and the
# test cases at line TODO 180 for this exercise.
# Modify the provided functions to use this information to calculate
# phi values for the function calls as described in the video.
# You should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
# When you have found out which function call and which return value type (bin)
# correlates the most with failure, fill in the following 3 variables,
# Do NOT set these values dynamically.

answer_function = "X"   # One of f1, f2, f3
answer_bin = 0         # One of 1, 0, -1
answer_value = 1.0000   # precision to 4 decimal places.

###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == tuple
    assert len(magic) == 3

    l, s, n = magic
    r1 = f1(l)
    r2 = f2(s)
    r3 = f3(n)

    if -1 in [r1, r2, r3]:
        return "FAIL"
    elif r3 < 0:
        return "FAIL"
    elif not r1 or not r2:
        return "FAIL"
    else:
        return "PASS"

# These are the input values you should test the mystery function with
inputs = [([1,2],"ab", 10),
          ([1,2],"ab", 2),
          ([1,2],"ab", 12),
          ([1,2],"ab", 21),
          ("a",1, [1]),
          ([1],"a", 1),
          ([1,2],"abcd", 8),
          ([1,2,3,4,5],"abcde", 8),
          ([1,2,3,4,5],"abcdefgijkl", 18),
          ([1,2,3,4,5,6,7],"abcdefghij", 5)]

def f1(ml):
    if type(ml) is not list:
        return -1
    elif len(ml) <6:
        return len(ml)
    else:
        return 0

def f2(ms):
    if type(ms) is not str:
        return -1
    elif len(ms) <6:
        return len(ms)
    else:
        return 0

def f3(mn):
    if type(mn) is not int:
        return -1
    if mn > 10:
        return -100
    else:
        return mn

# global variable to keep the coverage data in
coverage = {}  # :: f_name -> bin(-1,0,1) -> [r_val]
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    global coverage   # :: f_name -> bin(-1,0,1) -> [r_val]

    if event == "return":
        f_name = frame.f_code.co_name  # function name
        r_val = arg  # return value
        r_category = categorize(r_val)

        if f_name not in coverage:
            coverage[f_name] = {}
        # if r_category not in coverage[f_name]:
        #     coverage[f_name][r_category] = []
        coverage[f_name][r_category] = True

    return traceit

def categorize(r_val):
    """
    return value r_category
    =======================
    bin | meaning           | numeric | bool  | string   |special vaule
    ---------------------------------------------------------
    -1  | less than zero    | n<0     |       |          |None,NaN,Excptions
    0   | zero              | n=0     | False | len(n)=0 |
    1   | greater than zero | n>0     | True  | len(n)>0 |
    """
    if r_val is True:
        r_category = 1
    elif r_val is False:
        r_category = 0
    elif isinstance(r_val, (int, long, float, complex)):
        if r_val < 0:
            r_category = -1
        elif r_val == 0:
            r_category = 0
        else:
            r_category =1
    elif type(r_val) is str:
        r_category = 0 if len(r_val)==0 else 1
    else:
        r_category = -1
    return r_category

# Calculate phi coefficient from given values
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) /
            math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each covered line
def eval_print_table(tables):
    for f_name in tables:
        for bin in tables[f_name]:
            (n11, n10, n01, n00) = tables[f_name][bin]
            try:
                factor = phi(n11, n10, n01, n00)
                prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
            except:
                prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
            print prefix, f_name, bin

# These are the input values you should test the mystery function with
inputs = [([1,2],"ab", 10),
          ([1,2],"ab", 2),
          ([1,2],"ab", 12),
          ([1,2],"ab", 21),
          ("a",1, [1]),
          ([1],"a", 1),
          ([1,2],"abcd", 8),
          ([1,2,3,4,5],"abcde", 8),
          ([1,2,3,4,5],"abcdefgijkl", 18),
          ([1,2,3,4,5,6,7],"abcdefghij", 5)]
# Run the program with each test case and record
# input, outcome and coverage of lines
def run_tests(inputs):
    runs   = []
    for input in inputs:
        global coverage
        coverage = {}

        sys.settrace(traceit)
        outcome = mystery(input)
        sys.settrace(None)

        runs.append((input, outcome, coverage))
    return runs

# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for f_name,bins in coverage.iteritems():
            for bin in bins.keys():
                if f_name not in tables:
                    tables[f_name] = {}
                if bin not in tables[f_name]:
                    tables[f_name][bin] = (0, 0, 0, 0)

    return tables

# Compute n11, n10, etc. for each line
def compute_n(tables):
    for f_name, bins in tables.iteritems():
        for bin in bins.keys():
            (n11, n10, n01, n00) = tables[f_name][bin]
            for (input, outcome, coverage) in runs:
                if f_name in coverage and bin in coverage[f_name]:
                    # Covered in this run
                    if outcome == "FAIL":
                        n11 += 1  # covered and fails
                    else:
                        n10 += 1  # covered and passes
                else:
                    # Not covered in this run
                    if outcome == "FAIL":
                        n01 += 1  # uncovered and fails
                    else:
                        n00 += 1  # uncovered and passes
            tables[f_name][bin] = (n11, n10, n01, n00)
    return tables

# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

runs = run_tests(inputs)

tables = init_tables(runs)

tables = compute_n(tables)

eval_print_table(tables)