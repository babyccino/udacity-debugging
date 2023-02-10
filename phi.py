#!/usr/bin/env python
import sys
import math
import numbers
# INSTRUCTIONS !
# This provided, working code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the traceit 
# function to work for function calls instead of lines. It should save the 
# function name and the return value of the function for each function call. 
# Use the mystery function that can be found at line 155 and the
# test cases at line 180 for this exercise.
# Modify the provided functions to use this information to calculate
# phi values for the function calls as described in the video.
# You should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
# When you have found out which function call and which return value type (bin)
# correlates the most with failure, fill in the following 3 variables,
# Do NOT set these values dynamically.

answer_function = "X"   # One of f1, f2, f3
answer_bin = 42         # One of 1, 0, -1
answer_value = 1.0000   # precision to 4 decimal places.

# The buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:

        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out


# global variable to keep the coverage data in
coverage = {}
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in 
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    global coverage

    if not (event == "line" or event == "return"):
        return traceit
    
    filename = frame.f_code.co_filename
    if not filename in coverage:
        coverage[filename] = {"lines": {}, "function_calls": {}}

    if event == "line":
        lineno = frame.f_lineno
        coverage[filename]["lines"][lineno] = True
    elif event == "return":
        function_name = frame.f_code.co_name
        coverage[filename]["function_calls"][function_name] = arg
        
    return traceit

# Calculate phi coefficient from given values            
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) / 
             math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each covered line
def print_tables(tables):
    for filename in tables.keys():
        lines = open(filename).readlines()
        covered_lines = tables[filename]["lines"].keys()
        covered_lines.sort()
        for line_no in covered_lines: # lines of the remove_html_markup in this file
            (n11, n10, n01, n00) = tables[filename]["lines"][line_no]
            try:
                factor = phi(n11, n10, n01, n00)
                prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
            except:
                prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
                    
            print(prefix, lines[line_no - 1].replace('\n', ""))

        for function, tuples in tables[filename]["function_calls"].items():
            for cat in ("lt", "eq", "gt"):
                (n11, n10, n01, n00) = tuples[cat]
                try:
                    factor = phi(n11, n10, n01, n00)
                    prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
                except:
                    prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
                
                print(prefix, function, cat)

                            
# Run the program with each test case and record 
# input, outcome and coverage of lines
def run_tests(inputs):
    runs   = []
    for input in inputs:
        global coverage
        coverage = {}
        sys.settrace(traceit)
        result = remove_html_markup(input)
        sys.settrace(None)
        
        if result.find('<') == -1:
            outcome = "PASS"
        else:
            outcome = "FAIL"

        # print coverage
        
        runs.append((input, outcome, coverage))
    return runs

# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for filename in coverage:
            if not filename in tables:
                tables[filename] = {"lines": {}, "function_calls": {}}

            table = tables[filename]

            for line in coverage[filename]["lines"]:
                table["lines"][line] = (0, 0, 0, 0)

            for function in coverage[filename]["function_calls"]:
                table["function_calls"][function] = {
                    "lt": [0, 0, 0, 0],
                    "eq": [0, 0, 0, 0],
                    "gt": [0, 0, 0, 0]
                }

    return tables

# Compute n11, n10, etc. for each line
def compute_n(runs):
    tables = init_tables(runs)

    for filename in tables:
        table = tables[filename]
        lines = table["lines"]
        function_calls = table["function_calls"]

        for (input, outcome, coverage) in runs:
            for line, tup in lines.items():
                (n11, n10, n01, n00) = tup
                if line in coverage[filename]["lines"]:
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
                lines[line] = (n11, n10, n01, n00)

            for function, tuples in function_calls.items():
                if not function in coverage[filename]["function_calls"]: continue

                arg = coverage[filename]["function_calls"][function]

                if arg == None or (isinstance(arg, numbers.Number) and arg < 0):
                    cat = "lt"
                    others = ("eq", "gt")
                elif arg == 0 or ((isinstance(arg, str) or isinstance(arg, list)) and len(arg) == 0):
                    cat = "eq"
                    others = ("lt", "gt")
                else:
                    cat = "gt"
                    others = ("lt", "eq")
                    
                if outcome == "FAIL":
                    # n11
                    tuples[cat][0] += 1

                    # n01
                    for other_cat in others:
                        tuples[other_cat][2] += 1
                else:
                    # n10
                    tuples[cat][1] += 1

                    # n00
                    for other_cat in others:
                        tuples[other_cat][3] += 1

    return tables
      
# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

# These are the test cases          
inputs_line = ['foo', 
          '<b>foo</b>', 
          '"<b>foo</b>"', 
          '"foo"', 
          "'foo'", 
          '<em>foo</em>', 
          '<a href="foo">foo</a>',
          '""',
          "<p>"]
# runs = run_tests(inputs_line)

# tables = compute_n(runs)

# print_tables(tables)      
            
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
inputs2 = [([1,2],"ab", 10), 
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
    elif len(ml) <6 :
        return len(ml)
    else:
        return 0
    
def f2(ms):    
    if type(ms) is not str:
        return -1
    elif len(ms) <6 :
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

def run_tests2(inputs):
    runs   = []
    for input in inputs:
        global coverage
        coverage = {}
        sys.settrace(traceit)
        result = mystery(input)
        sys.settrace(None)
        
        runs.append((input, result, coverage))
    return runs

runs2 = run_tests2(inputs2)

tables2 = compute_n(runs2)

print_tables(tables2)
