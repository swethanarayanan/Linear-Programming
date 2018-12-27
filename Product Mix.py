# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:32:34 2018

@author: CEO
"""

from pulp import *
 
# declare your variables
x1 = LpVariable("x1", 0,None,LpContinuous)   # 0<= x1 <= Infinity
x2 = LpVariable("x2", 0,None,LpContinuous) # 0<= x2 <= Infinity
x3 = LpVariable("x3", 0,None,LpContinuous)   # 0<= x3 <= Infinity
x4 = LpVariable("x4", 0,None,LpContinuous) # 0<= x4 <= Infinity

 
# defines the problem
prob = LpProblem("problem", LpMaximize)
 



# defines the objective function to maximize
prob += 54*x1+ 77*x2+20*x3 + 30*x4
 


# defines the constraints
prob += 0.1*x1+0.25*x2+0.08*x3+0.21*x4<=72

prob += 3*(x1+x2)+x3+x4<=1200

prob += x1+x2+x3+x4<=500

prob += x3+x4<=500
prob += 36*x1+48*x2+25*x3+35*x4<=25000


 
# solve the problem
#status = prob.solve(GLPK(msg=0))


prob.writeLP("Wyndor.lp")

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