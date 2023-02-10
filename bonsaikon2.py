#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code, using your code from
# first exercise and adding ability to infer assertions
# for variable type, set and relations
# Modify only the classes Range and Invariants,
# if you need additional functions, make sure
# they are inside the classes.

import sys
import math
import random

def square_root(x, eps = 0.00001):
    assert x >= 0
    y = math.sqrt(x)
    assert abs(square(y) - x) <= eps
    return y
    
def square(x):
    return x * x

def double(x):
    return abs(20 * x) + 10

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self, val = None):
        self.min  = val  # Minimum value seen
        self.max  = val  # Maximum value seen
        self.type = type(val)  # Type of variable
        if val is None:
            self.set = set()  # Set of values taken
        else:
            self.set = set([val])
    
    # Invoke this for every value
    def track(self, value):
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self.type = type(value)
        self.set.add(value)

        # YOUR CODE
            
    def __repr__(self):
        repr(self.type) + " " + repr(self.min) + ".." + repr(self.max)+ " " + repr(self.set)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}
        
    
        
    def track(self, frame, event, arg):
        if event == "call" or event == "return":
            locals = frame.f_locals
            fun = frame.f_code.co_name

            if fun not in self.vars:
                if event == "return":
                    # self.vars.update({fun: {event: {"ret": Range(arg)}}})
                    self.vars.update({fun: {"call": {"ret": Range(arg)}}})
                else:
                    dict = {}
                    for var in locals:
                        dict.update({var: Range(locals[var])})

                    self.vars.update({fun: {event: dict}})
                return

            if "call" not in self.vars[fun]:
                if event == "return":
                    # self.vars[fun].update({event: {"ret": Range(arg)}})
                    self.vars[fun].update({"call": {"ret": Range(arg)}})
                else:
                    dict = {}
                    for var in locals:
                        dict.update({var: Range(locals[var])})

                    self.vars.update[fun]({event: dict})
                return
            
            if event == "return":
                # self.vars[fun][event]["ret"].track(arg)
                if "ret" not in self.vars[fun]["call"]: self.vars[fun]["call"].update({"ret": Range(arg)})
                else: self.vars[fun]["call"]["ret"].track(arg)
            else:
                for var in locals:
                    val = locals[var]
                    if var in self.vars[fun][event]: 
                        self.vars[fun][event][var].track(val)
                    else:
                        self.vars[fun][event].update({var: Range(val)})
    
    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.items():
            for event, vars in events.items():
                s += event + " " + function + ":\n"

                items = list(vars.items())
        
                for var1, range1 in items:
                    s += "    assert isinstance(" + var1 + ", type(" + str(range1.min) + "))"
                    s += "    assert "
                    if range1.min == range1.max:
                        s += var1 + " == " + repr(range1.min)
                    else:
                        s += repr(range1.min) + " <= " + var1 + " <= " + repr(range1.max)
                    s += "\n"
                    s += "    assert " + var1 + " in " + str(range1.set)

                for i in range(len(items)):
                    var1, range1 = items[i]

                    for ii in range(i + 1, len(items)):
                        var2, range2 = items[ii]

                        if range1.min == range1.max and range2.min == range2.max:
                            comparison = " == "
                        elif range1.max <= range2.min:
                            comparison = " <= "
                        elif range1.min >= range2.max:
                            comparison = " >= "
                        else: continue
                        
                        s += "    assert " + var1 + comparison + var2
                                
        return s

invariants = Invariants()
    
def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
test_vars = [34.6363, 9.348, -293438.402]
for i in test_vars:
#for i in range(1, 10):
    z = double(i)
sys.settrace(None)
print (invariants)

# Example sample of a correct output:
"""
return double:
    assert isinstance(x, type(-293438.402))
    assert x in set([9.348, -293438.402, 34.6363])
    assert -293438.402 <= x <= 34.6363
    assert x <= ret
"""
