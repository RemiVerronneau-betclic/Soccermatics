"""
Markov chains
====================

Here we look at how to formulate expected threat in terms of a Markov chain.
First watch the video


..  youtube:: 5ESij-MDKl4
   :width: 640
   :height: 349
"""


import numpy as np


########################
# Setting up the matrix
# ---------------------
# We first set up the pass matrix *A* and the goal vector *g*.

#Pass matrix
A = np.matrix([[0.25, 0.20, 0.1], [0.1, 0.25, 0.2],[0.1, 0.1, 0.25]])
#Goal vector
g = np.transpose(np.matrix([0.05, 0.15, 0.05]))



########################
# Linear algebra method
# ------------------------
#
# Here we solve *(I-A)xT = g*

xT1 = np.linalg.solve(np.identity(3) - A,g)

print('Expected Threat')
print('Central, Box, Wing')
print(np.transpose(xT1))



########################
# Iterative method
# ------------------------
#
# Here we iterate xT' = A xT + g
# to update through each move of the ball


xT2=np.zeros((3,1))
for _ in range(10):
   #print(np.matmul(A,xT2) + g)
   xT2 = np.matmul(A,xT2) + g

print('Expected Threat')
print('Central, Box, Wing')
print(np.transpose(xT2))


########################
# Simulation method
# ---------------------------
#
# Here we simulate *num_sim* possessions, starting from each of the three areas.

num_sims=10
xT3=np.zeros(3) 

description = {0: 'Central', 1: 'Wing', 2: 'Box' }

for i in range(3):
   num_goals = 0

   print('---------------')
   print(f'Start from {description[i]}')
   print('---------------')

   for _ in range(num_sims):
      ballinplay=True
      #Initial state is i
      s = i
      describe_possession=''

      while ballinplay:
         r=np.random.rand()

            # Make commentary text
         describe_possession = f'{describe_possession} - {description[s]}'
                     

         #Cumulative sum of in play probabilities
         c_sum=np.cumsum(A[s,:])
         new_s = np.sum(r>c_sum)
         if new_s>2:
            #Ball is either goal or out of play
            ballinplay=False
            if r < g[s] + c_sum[0,2]:
               #Its a goal!
               num_goals = num_goals + 1
               describe_possession = f'{describe_possession} - Goal!'
            else:
               describe_possession = f'{describe_possession} - Out of play'
         s = new_s  

      print(describe_possession)  

   xT3[i] = num_goals/num_sims


print('\n\n---------------')
print('Expected Threat')
print('Central, Box, Wing')
print(xT3)      
              
                    
############################################################
#Here I work through the derivation of equations for *xT*
#
#.. image:: ../../../source/images/lesson4/DeriveMarkov1.png
#
#Here I outline how we write this in matrix form:
#
#.. image:: ../../../source/images/lesson4/DeriveMarkov2.png
