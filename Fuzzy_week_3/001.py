import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl 
from mpl_toolkits.mplot3d import Axes3D

universe = np.linspace(0,10,61)  # Chia ra tu 0->10 co 61 do phan giai 
universe_1 = np.linspace(10,30,61)

food = ctrl.Antecedent(universe, 'food')
service = ctrl.Antecedent(universe, 'service')
tip = ctrl.Consequent(universe_1, 'tip')

names_1 = ['VP', 'P', 'AV', 'G', 'VG']
names_2 = ['VL', 'L', 'H', 'VH']
food.automf(names = names_1)               # Ham chi tao ra membership function la mot so le
service.automf(names = names_1)
tip.automf(names  = names_2)

rule_VL = ctrl.Rule(antecedent=((food['VP'] & service['VP']) |  (food['VP'] & service['P']) | (food['P'] & service['VP'])), consequent=tip['VL'], label= 'Rule VL')
rule_L = ctrl.Rule(antecedent=((food['VP'] & service['AV']) |  (food['VP'] & service['G']) | (food['P'] & service['P'])  | (food['P'] & service['AV'])  | (food['AV'] & service['P'])  | (food['AV'] & service['VP'])  | (food['G'] & service['VP'])), consequent=tip['L'], label= 'Rule L')
rule_H = ctrl.Rule(antecedent=((food['VG'] & service['VG']) |  (food['VG'] & service['G']) | (food['G'] & service['VG'])  | (food['G'] & service['G'])  | (food['VG'] & service['AV'])  | (food['G'] & service['AV'])  | (food['AV'] & service['G'])  | (food['AV'] & service['VG'])), consequent=tip['VH'], label= 'Rule VH')
rule_VH = ctrl.Rule(antecedent=((food['VG'] & service['VP']) |  (food['VP'] & service['VG']) | (food['P'] & service['VG'])  | (food['P'] & service['G'])  | (food['VG'] & service['P'])  | (food['G'] & service['P'])  | (food['AV'] & service['AV'])  ), consequent=tip['H'], label= 'Rule H')


systems_1 = ctrl.ControlSystem([rule_L, rule_VL, rule_VH, rule_H])
tipping_systems = ctrl.ControlSystemSimulation(systems_1, flush_after_run=61*61+1) 

 # Tinh toan va gan bien mo phong
upsampled = np.linspace(0,10,101)
x,y = np.meshgrid(upsampled, upsampled)

z = np.zeros_like(x)

for i in range(61):
    for j in range(61):       
        tipping_systems.input['food'] = x[i,j]
        tipping_systems.input['service'] = y[i,j]
        tipping_systems.compute()
        z[i,j] = tipping_systems.output['tip']



fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
suf = ax.plot_surface(x,y,z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)

cset = ax.contourf(x, y, z, zdir='z', offset=9, cmap  = 'viridis', alpha = 0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=11, cmap  = 'viridis', alpha = 0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap  = 'viridis', alpha = 0.5)






ax.view_init(30,200)

food.view()
service.view()
tip.view()

rule_VL.view()

plt.show()
