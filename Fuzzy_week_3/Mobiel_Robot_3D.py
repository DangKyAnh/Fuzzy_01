import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl 
from mpl_toolkits.mplot3d import Axes3D as ax
import math 

universe = np.linspace(-math.pi/2, math.pi/2, 101)  # Chia ra tu 0->10 co 61 do phan giai 
universe_2 = np.linspace(-math.pi/4, math.pi/4, 101)
universe_1 = np.linspace(0,100,101)

alpha = ctrl.Antecedent(universe, 'alpha')
dedt = ctrl.Antecedent(universe_2, 'dedt')
Force_1 = ctrl.Consequent(universe_1, 'Force_1')

names_1 = ['LN', 'N', 'ZR', 'P', 'VP']
names_2 = ['-2', '-1', '0', '1', '2']
alpha.automf(names = names_1)               # Ham chi tao ra membership function la mot so le
dedt.automf(names = names_1)
Force_1.automf(names  = names_2)

Rule_2_ = ctrl.Rule(antecedent = ((alpha['LN']&dedt['LN']) |   (alpha['LN']&dedt['N']) |  (alpha['N']&dedt['LN'])   ), consequent=Force_1['-2'], label= 'Very LOW' )
Rule_1_ = ctrl.Rule(antecedent = ((alpha['LN']&dedt['ZR']) |   (alpha['LN']&dedt['P']) |  (alpha['N']&dedt['N'])  |  (alpha['N']&dedt['ZR']) |  (alpha['ZR']&dedt['LN']) |  (alpha['ZR']&dedt['N']) |  (alpha['P']&dedt['LN']) ), consequent= Force_1['-1'], label = 'LOW' )
Rule_0 = ctrl.Rule(antecedent = ((alpha['LN']&dedt['VP']) |   (alpha['VP']&dedt['LN']) |  (alpha['N']&dedt['P'])  |  (alpha['P']&dedt['N']) |  (alpha['ZR']&dedt['ZR']) ), consequent= Force_1['0'], label= 'Zero' )
Rule_1 = ctrl.Rule(antecedent = ((alpha['VP']&dedt['N']) |   (alpha['N']&dedt['VP']) |  (alpha['VP']&dedt['ZR'])  |  (alpha['ZR']&dedt['VP']) |  (alpha['P']&dedt['ZR']) |  (alpha['ZR']&dedt['P']) |  (alpha['P']&dedt['P']) ), consequent= Force_1['1'], label= 'HIGH' )
Rule_2 = ctrl.Rule(antecedent = ((alpha['VP']&dedt['P']) |   (alpha['P']&dedt['VP']) |  (alpha['VP']&dedt['VP'])   ) , consequent= Force_1['2'], label= 'Very HIGH')


systems_1 = ctrl.ControlSystem([Rule_2_, Rule_1_, Rule_0, Rule_1, Rule_2])
Force_systems = ctrl.ControlSystemSimulation(systems_1, flush_after_run = 61*61+1) 


 # Tinh toan va gan bien mo phong
upsampled_1 = np.linspace((-math.pi/2),(math.pi/2),101)
upsampled_2 = np.linspace((-math.pi/4),(math.pi/4),101)
x,y = np.meshgrid(upsampled_1, upsampled_2)

z = np.zeros_like(x)

for i in range(101):
    for j in range(101):       
        Force_systems.input['alpha'] = x[i,j]
        Force_systems.input['dedt'] = y[i,j]
        Force_systems.compute()
        z[i,j] = Force_systems.output['Force_1']



fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
suf = ax.plot_surface(x,y,z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)

cset = ax.contourf(x, y, z, zdir='z', offset=9, cmap  = 'viridis', alpha = 0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=11, cmap  = 'viridis', alpha = 0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap  = 'viridis', alpha = 0.5)

plt.show()