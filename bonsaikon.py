#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code around lines 28 and 44
# Do not modify the __repr__ functions.
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

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self, val = None):
        self.min  = val  # Minimum value seen
        self.max  = val  # Maximum value seen
    
    # Invoke this for every value
    def track(self, value):
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        # YOUR CODE
            
    def __repr__(self):
        return repr(self.min) + ".." + repr(self.max)


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
                    self.vars.update({fun: {event: {"ret": Range(arg)}}})
                else:
                    dict = {}
                    for var in locals:
                        dict.update({var: Range(locals[var])})

                    self.vars.update({fun: {event: dict}})
                return

            if event not in self.vars[fun]:
                if event == "return":
                    self.vars[fun].update({event: {"ret": Range(arg)}})
                else:
                    dict = {}
                    for var in locals:
                        dict.update({var: Range(locals[var])})

                    self.vars.update[fun]({event: dict})
                return
            
            if event == "return":
                self.vars[fun][event]["ret"].track(arg)
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
                # continue
                
                for var, range in vars.items():
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"
                
        return s

invariants = Invariants()
    
def traceit(frame, event, arg = None):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
for i in range(1, 10):
    r = int(random.random() * 1000) # An integer value between 0 and 999.99
    z = square_root(r, eps)
    z = square(z)
sys.settrace(None)
print(invariants)

