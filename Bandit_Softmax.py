import math
import random
import time 
import numpy
from dataclasses import dataclass


#~~ Data structure to store important data ~~# 
@dataclass
class Bandit:
    arms      : list
    visited   : list
    arm_sum   : int 

@dataclass
class Agent:
    rewards   : list 
    machine   : int 
    arm       : int 
    tokens    : int 

#Setting the bandit enviroment as dataclasses(structures) inside a list 
def set_Bandits( Machines , Levers ):
    
    #List containing the probability of each arm to be pulled
    arms     = []
    visited  = []
    #List that holds that structures of the bandits 
    nBandits = []
    
    
    for i in range( Machines ):
 
        for j in range( Levers ):
            #loop to store the probabilities of the levers 
            arms.append(  round( random.random(  ) , 2 ) )
            visited.append(0)
        #loop to store the levers of the machines 
        nBandit = Bandit( arms  , visited, Levers     ) 
        nBandits.append ( nBandit )
        print( nBandits[i].arms , nBandits[i].visited )
        
        #clearing the list of the levers
        arms     = []
        visited  = []
        
    return nBandits

def prob_Explore( nBandits , agent , tau ):
    for rewards in agent.rewards:
          #For each machine 
          #Using softmax formula to calculate the probabilities to pick an machine 
          sigma = sum( [ math.exp( value / tau )  for value in rewards ] )
          p_Explore =      [ math.exp( value / tau ) / sigma  for value in rewards ]
     
    return p_Explore

def index_Draw( p_Explore ):
    
    rand = random.random()
    draw_prob = 0.0
    
    for i in range( len( p_Explore ) ):
        prob = p_Explore[i]
        draw_prob += prob
        
        if draw_prob > rand:
            return i
    
    return len( p_Explore ) - 1

def pull_Arm( nBandits , agent , draw_Index):
    pull      = round ( random.random() , 2)
    arm_Index = random.randint( 0, 3 )
    
    if nBandits [ draw_Index ].arms   [ arm_Index ] <= pull:
        #if we get a good reward from the arm 
        nBandits         [ draw_Index ].visited[ arm_Index ] += 1
        sigma  = nBandits[ draw_Index ].visited[ arm_Index ]
        
        reward = agent.rewards[ draw_Index ][arm_Index] + 1 / sigma
        agent.rewards         [ draw_Index ][ arm_Index ] = round( reward , 2 )
    else:
        nBandits        [ draw_Index ].visited[ arm_Index ] += 1
        sigma = nBandits[ draw_Index ].visited[ arm_Index ]
        
        reward = agent.rewards[ draw_Index ][ arm_Index ] - 1 / sigma
        agent.rewards         [ draw_Index ][ arm_Index ] = round( reward , 2 )

def Softmax( nBandits , agent , tau ):
    
    #For the set games 
    while agent.tokens != 0:
        
        #functions that return an array of calculated probabilities
        #Based on the softmax formula-> e^(r_i / tau) / sum( e^[r_k / tau] )
        #for the first itterations the Machines aare equaprobable
        p_Explore  = prob_Explore( nBandits , agent , tau )
        
        #the draw index returns the machine with the beast probablity 
        draw_Index = index_Draw( p_Explore )
        
        #lastly we pull a random arm from the machine 
        pull_Arm( nBandits , agent , draw_Index)
        
        agent.tokens = agent.tokens - 1
    print( p_Explore )
    return 0
Machines = int( input("Enter number of Machines: ") )
Levers   = int( input("Enter number of Levers:   ") )

#Setting the bandits by initializing 
#the Probabilities of each Lever 
nBandits = set_Bandits( Machines , Levers )


#Initilizing the agent 
visited  = []
rewards  = []
temp     = []
machine  = -1
arm      = -1
tokens   = int( input("~ Type number of Tokens to spend: ") )
for i in range( Machines ):
    
    for j in range( Levers ):
        temp.append(0)
    rewards.append( temp )
    temp = []
print( "Machine Reward Lists: ", rewards )
agent    = Agent(rewards , machine , arm, tokens )
#print( agent )

#Calling softmax function
#with temperature to adjust explore/exploit 
tau = 0.43
Softmax ( nBandits , agent , tau  )
