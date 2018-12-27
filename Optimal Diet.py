# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:32:34 2018

@author: CEO
"""

from pulp import *
import pandas as pd


import pandas as pd
x = pd.read_csv('Nutri.csv', index_col='Food')

 
# declare your variables
#Food_Type = ['Bran Cereal', 'Dry Cereal', 'Oat Meal','Oat Bran','Egg',
#             "Bacon", "Orange", "Milk", "Orange Juice","Wheat" ]

#Feature_Type =['Calo','Fat','Chol','Iron','Calc','Prot','Fiber','Cost']


Food_Type =x.index.values
Feature_Type =x.columns.values
TotalCal = 420
TotalIron = 5
TotalCalc = 400
TotalProc = 20
TotalFiber= 12
TotalFat= 20
TotalChol =30



print("Sample: ",x['Cost']['Bran Cereal'])

Food_Plan = pulp.LpVariable.dicts("Food_DV",
                                     ((i) for i in Food_Type),
                                     lowBound=0,
                                     cat='Continuous') 

# defines the problem
prob = LpProblem("problem", LpMinimize)
 



# defines the objective function to maximize

prob += pulp.lpSum(Food_Plan[i]*x['Cost'][i] for i in Food_Type) 

# defines the constraints
prob += pulp.lpSum(Food_Plan[i]*x['Calo'][i] for i in Food_Type)>=TotalCal
prob += pulp.lpSum(Food_Plan[i]*x['Iron'][i] for i in Food_Type)>=TotalIron
prob += pulp.lpSum(Food_Plan[i]*x['Calc'][i] for i in Food_Type)>=TotalCalc
prob += pulp.lpSum(Food_Plan[i]*x['Prot'][i] for i in Food_Type)>=TotalProc
prob += pulp.lpSum(Food_Plan[i]*x['Fiber'][i] for i in Food_Type)>=TotalFiber
prob += pulp.lpSum(Food_Plan[i]*x['Fat'][i] for i in Food_Type)<=TotalFat
prob += pulp.lpSum(Food_Plan[i]*x['Chol'][i] for i in Food_Type)<=TotalChol




 
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
#value(x1)
#value(x2)