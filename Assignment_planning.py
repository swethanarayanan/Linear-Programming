# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:32:34 2018

@author: CEO
"""

from pulp import *
 


Production_Type = ['Normal', 'OT', 'Inv']
Periods = ['Jan', 'Feb', 'Mar','Apr', 'May', 'Jun']
Capacity_Normal = 50000;
Capacity_OT = Capacity_Normal*0.5
Inventory_Initial = 4500

Prod_Plan = pulp.LpVariable.dicts("Product_DV",
                                     ((i, j) for i in Production_Type for j in Periods),
                                     lowBound=0,
                                     cat='Continuous')
Cost = {Production_Type[0]:32000,Production_Type[1]:40000,Production_Type[2]:5000}
Demand = {Periods[0]:50000,Periods[1]:25000,Periods[2]:25000,Periods[3]:42000,Periods[4]:55000,Periods[5]:67000}
# declare your variables


 
# defines the problem
prob = LpProblem("problem", LpMinimize)
 



# defines the objective function to maximize
prob += pulp.lpSum([Prod_Plan[(i,j)]*Cost[i]] for i in Production_Type for j in Periods) 


# defines the constraints
prob +=(Prod_Plan[('Normal','Jan')]+Prod_Plan[('OT','Jan')] +  Inventory_Initial == (Demand['Jan'] + Prod_Plan[('Inv','Jan')]))

for j in range (1,6):
    prob +=Prod_Plan[('Normal',Periods[j])]+Prod_Plan[('OT',Periods[j])] +  Prod_Plan[('Inv',Periods[j-1])] == Demand[Periods[j]] + Prod_Plan[('Inv',Periods[j])]
#capacity constraint

for j in Periods:
    prob += (Prod_Plan[('Normal',j)]<=Capacity_Normal )
        
for j in Periods:
    prob += (Prod_Plan[('OT',j)]<=Capacity_OT )


#non-negative constraint
for i in Production_Type:
    for j in Periods:
        prob += (Prod_Plan[(i,j)]>=0 )

 
# solve the problem
#status = prob.solve(GLPK(msg=0))


prob.writeLP("test.lp")

#prob.solve(GLPK(options=["--ranges test.sen"]))
prob.solve()


for v in prob.variables():
	        print (v.name, "=", v.varValue, "\tReduced Cost =", v.dj)

print ("objective=", value(prob.objective))

print ("\nSensitivity Analysis\nConstraint\t\tShadow Price\tSlack")
for name, c in prob.constraints.items():
        print (name, ":", c, "\t", c.pi, "\t\t", c.slack)

print("Status:", LpStatus[prob.status])
 
# print the results x1 = 20, x2 = 60
for i in Production_Type:
    for j in Periods:
        print(i, j, value(Prod_Plan[(i,j)]))


Periods