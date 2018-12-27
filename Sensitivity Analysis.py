# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:32:34 2018

@author: CEO
"""

from pulp import *
 
# declare your variables
x1 = LpVariable("x1", 0,None,LpContinuous)   # 0<= x1 <= Infinity
x2 = LpVariable("x2", 0,None,LpContinuous) # 0<= x2 <= Infinity
#x3 = LpVariable("x3", 0,None,LpContinuous) # 0<= x2 <= Infinity

 
# defines the problem
prob = LpProblem("problem", LpMaximize)
 



# defines the objective function to maximize
prob += 3*x1+5*x2 


# defines the constraints

prob += x1 <=4
prob += 2*x2<=12
prob += 3*x1+2*x2<=18



prob += x1>=0
prob += x2>=0

 
# solve the problem
#status = prob.solve(GLPK(msg=0))


prob.writeLP("Wyndor.lp")


prob.solve(GLPK(options=["--ranges test2.sen"]))
prob.solve()



for v in prob.variables():
	        print (v.name, "=", v.varValue, "\tReduced Cost =", v.dj)

print ("objective=", value(prob.objective))

print ("\nSensitivity Analysis\nConstraint\t\tShadow Price\tSlack")
for name, c in prob.constraints.items():
        print (name, ":", c, "\t", c.pi, "\t\t", c.slack)

print("Status:", LpStatus[prob.status])
 
# print the results x1 = 20, x2 = 60
value(x1)
value(x2)