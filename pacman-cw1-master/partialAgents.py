# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman"s interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class PartialAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        name = "Pacman"
        self.lastIndex = 0 #used to see which corner is being seeked 
        self.reachedCorners = [None] * 4 #used to track the reached corners (Initially it is empty as no corner has been reached)
        self.lastMove = Directions.STOP #initialise the last move as STOP as it has not moved yet
    
    # This is what gets run in between multiple games
    def final(self, state):
        self.lastIndex = 0 #used to see which corner is being seeked 
        self.reachedCorners = [None] * 4 #used to track the reached corners (Initially it is empty as no corner has been reached)
        self.lastMove = Directions.STOP #initialise the last move as STOP as it has not moved yet
      
     #Method checks if the pacman can go right or if there is a ghost within two spots to the right 
    def checkIfCanGoRight(self, state, ghostsNearby, currentLocationOfPacman): #ghostsNearby are all the ghosts the pacman can see
        maxLen = len(ghostsNearby) #number of ghosts nearby
        for i in range(maxLen): #for each ghost
                distanceInX = ghostsNearby[i][0]-currentLocationOfPacman[0] #how far away on the x-axis the pacman is from the chosen ghost. 
                #Positive means the ghost is on the right
                #Negative means the ghost is to the left of the pacman
                if (distanceInX>0) and (distanceInX<3): #if the ghost was on the right and is within 2 spots 
			  distanceInY = ghostsNearby[i][1]-currentLocationOfPacman[1] #how far away on the y-axis the pacman is from the chosen ghost. 
			  if ((distanceInY<0) and (distanceInY>-3)) or ((distanceInY>0) and (distanceInY<3)): #if it is also nearby in the y-direction
			  	  return False #there is a ghost too close on the right to go right so return false
        return True #there is no ghost too close on the right to go right so return true
    
    #Method checks if the pacman can go left or if there is a ghost within two spots to the left 
    def checkIfCanGoLeft(self, state, ghostsNearby, currentLocationOfPacman): #ghostsNearby are all the ghosts the pacman can see
        maxLen = len(ghostsNearby) #number of ghosts nearby
        for i in range(maxLen): #for each ghost

            distanceInX = ghostsNearby[i][0]-currentLocationOfPacman[0] #how far away on the x-axis the pacman is from the chosen ghost. 
            #Positive means the ghost is on the right
            #Negative means the ghost is to the left of the pacman
	
            if (distanceInX<0) and (distanceInX>-3): #if the ghost was on the left and is within 2 spots 
	      	distanceInY = ghostsNearby[i][1]-currentLocationOfPacman[1] #how far away on the y-axis the pacman is from the chosen ghost. 
		if ((distanceInY<0) and (distanceInY>-3)) or ((distanceInY>0) and (distanceInY<3)): #if it is also nearby in the y-direction
			  return False #there is a ghost too close on the left to go left so return false
        return True #there is no ghost too close on the left to go left so return true
    
    #Method checks if the pacman can go down or if there is a ghost within two spots below it 
    def checkIfCanGoDown(self, state, ghostsNearby, currentLocationOfPacman): #ghostsNearby are all the ghosts the pacman can see
      
      maxLen = len(ghostsNearby) #number of ghosts nearby
      for i in range(maxLen): #for each ghosts
	
	distanceInY = ghostsNearby[i][0]-currentLocationOfPacman[0] #how far away on the y-axis the pacman is from the chosen ghost. 
	#Positive means the ghost is above the pacman
	#Negative means the ghost is below the pacman
	
	if (distanceInY<0) and (distanceInY>-3):#if the ghost was below and is within 2 spots 
	  distanceInX = ghostsNearby[i][0]-currentLocationOfPacman[0] #how far away on the x-axis the pacman is from the chosen ghost. 
	  if ((distanceInX<0) and (distanceInX>-3)) or ((distanceInX>0) and (distanceInX<3)): #if it is also nearby in the x-direction
	    return False #there is a ghost too close below to go down so return false
      return True #there is no ghost too close below to go down so return true
    
        #Method checks if the pacman can go up or if there is a ghost within two spots above it 
    def checkIfCanGoUp(self, state, ghostsNearby, currentLocationOfPacman): #ghostsNearby are all the ghosts the pacman can see
      maxLen = len(ghostsNearby) #number of ghosts nearby
      for i in range(maxLen): #for each ghost

	distanceInY = ghostsNearby[i][1]-currentLocationOfPacman[1] #how far away on the y-axis the pacman is from the chosen ghost. 
	#Positive means the ghost is above the pacman
	#Negative means the ghost is below the pacman

	if (distanceInY>0) and (distanceInY<3): #if the ghost was above and is within 2 spots 
	  distanceInX = ghostsNearby[i][0]-currentLocationOfPacman[0]#how far away on the x-axis the pacman is from the chosen ghost. 
	  if ((distanceInX<0) and (distanceInX>-3)) or ((distanceInX>0) and (distanceInX<3)): #if it is also nearby in the x-direction
	    return False #there is a ghost too close above to go up so return false
      return True #there is no ghost too close above to go up so return true
    
    #Method makes the ghost try and escape the ghosts nearby .
    def escapeGhosts(self, state, ghostsNearby, legal, currentLocationOfPacman): #ghostsNearby are all the ghosts the pacman can see

      if (len(ghostsNearby)>0): #if there is at least one ghost nearby the pacman
	
	firstGhostToAvoid = ghostsNearby[0] #the first ghost in the list of nearby ghosts
	xOfFirstGhost = firstGhostToAvoid[0] #the x coordinate of the first ghost
	yOfFirstGhost = firstGhostToAvoid[1] #the y coordinate of the first ghost

      if (len(ghostsNearby) == 1): #if there is exactly one nearby ghost

	  if (xOfFirstGhost>currentLocationOfPacman[0]): #if the ghost is to the right of the pacman
	    
	     if Directions.WEST in legal: #the ghost is east of the pacman so try and flee west but it cannot be done if it is not a legal move
	       self.lastMove = Directions.WEST #update the last move made to be west as that will be where the pacman moves
	       return api.makeMove(Directions.WEST, legal) #go west!
	     
	     elif Directions.EAST in legal: #otherwise, if west was NOT legal but east was, do not go east! 
	       #The ghost is to the east and the pacman should avoid it at all costs
	       legal.remove(Directions.EAST)
	 
	  if (xOfFirstGhost<currentLocationOfPacman[0]): #if the ghost is to the left of the pacman
	    
	     if Directions.EAST in legal: #the ghost is west of the pacman so try and flee east but it cannot be done if it is not a legal move
	       self.lastMove = Directions.EAST #update the last move made to be east as that will be where the pacman moves
	       return api.makeMove(Directions.EAST, legal) #go east!
	     
	     elif Directions.WEST in legal:  #otherwise, if east was NOT legal but west was, do not go west! 
	       #The ghost is to the west and the pacman should avoid it at all costs
	       legal.remove(Directions.WEST)
	     
	  if (yOfFirstGhost<currentLocationOfPacman[1]): #if the ghost is below the pacman
	    
	     if Directions.NORTH in legal: #try and go north if you can to avoid the ghost to the south
	       self.lastMove = Directions.NORTH
	       return api.makeMove(Directions.NORTH, legal)
	     
	     elif Directions.SOUTH in legal: #if you cant go north, go anywhere but south
	       legal.remove(Directions.SOUTH)
	     
          if (yOfFirstGhost>currentLocationOfPacman[1]): #if the ghost is above the pacman
	    
	     if Directions.SOUTH in legal:#try and go south if you can to avoid the ghost to the north
	       self.lastMove = Directions.SOUTH
	       return api.makeMove(Directions.SOUTH, legal)
	     
	     elif Directions.NORTH in legal: #if you cant go south, go anywhere but north
	       legal.remove(Directions.NORTH)       
      elif (len(ghostsNearby)>1): #otherwise, if there are multiple ghosts 

	  if (xOfFirstGhost>currentLocationOfPacman[0]): #if the first ghost is to the east
	     if (Directions.WEST in legal): #check you can legally go west
	       
	       canGoLeft = self.checkIfCanGoLeft(state, ghostsNearby, currentLocationOfPacman) #check if you can go left without dying (losing the game)
	       
	       if canGoLeft == True: #if the pacman will not die when it goes west then go west
	         self.lastMove = Directions.WEST
	         return api.makeMove(Directions.WEST, legal)
	       else:
		 legal.remove(Directions.WEST) #do not go west if it is likely to kill you
	       
	       if Directions.EAST in legal: #if you cannot go west, then make sure you do not go east
		 legal.remove(Directions.EAST)
	 
	  if (xOfFirstGhost<currentLocationOfPacman[0]): #if the first ghost is to the west
	     if Directions.EAST in legal: #check you can legally go east
	       
	       canGoRight = self.checkIfCanGoRight(state, ghostsNearby, currentLocationOfPacman) #check if you can go right without dying (losing the game)
	       
	       if canGoRight == True: #if the pacman will not die when it goes east then go east
	         self.lastMove = Directions.EAST 
	         return api.makeMove(Directions.EAST, legal)
	       else:
		 legal.remove(Directions.EAST) #do not go east if it is likely to kill you
	       
	       if Directions.WEST in legal: #if you cannot go east then at the very least, do not go west!
	        legal.remove(Directions.WEST)
	     
	  if (yOfFirstGhost<currentLocationOfPacman[1]): #if the first ghost is to the south
	     if Directions.NORTH in legal: #check you can legally go north
	       
	       canGoUp = self.checkIfCanGoUp(state, ghostsNearby, currentLocationOfPacman) #check if you can go up without dying (losing the game)
	       
	       if canGoUp == True: #if the pacman will not die when it goes north then go north
	         self.lastMove = Directions.NORTH
	         return api.makeMove(Directions.NORTH, legal)
	       else:
		 legal.remove(Directions.NORTH) #do not go north if it is likely to kill you
	       
	       if Directions.SOUTH in legal: #if you cannot go north then at the very least, do not go south!
	         legal.remove(Directions.SOUTH)
	     
          if (yOfFirstGhost>currentLocationOfPacman[1]): #if the first ghost is to the north
	    
	     if Directions.SOUTH in legal:#check you can legally go south
	       
	       canGoDown = self.checkIfCanGoUp(state, ghostsNearby, currentLocationOfPacman) #check if you can go down without dying (losing the game)
	       
	       if canGoDown==True: #if the pacman will not die when it goes south then go south
	         self.lastMove = Directions.SOUTH
	         return api.makeMove(Directions.SOUTH, legal)
	       else:
		 legal.remove(Directions.SOUTH) #do not go south if it is likely to kill you
	       if Directions.NORTH in legal: #if you cannot go south then at the very least, do not go north!
	         legal.remove(Directions.NORTH)

    #Method used to choose what move the pacman will make
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them. (this is code from Professor Simon Parsons)
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
       
       #(code from Professor Simon Parsons ends)
       
        currentLocationOfPacman = api.whereAmI(state) #get the current position of pacman (used later when deciding which way to go regardless of whether you are running away from ghosts or searching for food or corners)
	
        corners = api.corners(state) #gets the corners
	ghostsNearby = api.ghosts(state) #gets the nearby ghosts
      
      	if (len(ghostsNearby)>0): #if there is at least one ghost nearby
	  self.escapeGhosts(state, ghostsNearby, legal, currentLocationOfPacman) #escape the ghosts!
	  
        foodNotCorner = False #Initially assume it seeks the corners, not food
        
        index = self.lastIndex #will be used to choose a corner to search for
        
        if (self.reachedCorners[3] == None): #if the last corner has not been reached yet
	   goalChosen = corners[index] #choose the corner the pacman will head to and make it the goal
	   
	else: #All corners have been reached so the priority is now the food
	  
	  foodNearby = api.food(state) # get all the food locations that the pacman knows of
	  
	  if (len(foodNearby)>0): #if there is at least one food nearby

	    if(len(foodNearby[0])>0): #if the first food location in the list is not empty
	      goalChosen = foodNearby[0] #make the goal the first food in the list
	      foodNotCorner = True #Now it is seeking food and not corners

	    else: #search for a corner again if there was an error with the food locator
	      foodNotCorner = False #now seeking a corner again
	      if index<len(corners): #if the index corresponds to a real slot in corners make the corner the new goal
		goalChosen = corners[index]
	      else: #otherwise reset the index to 0 and make the goal the corresponding corner
	       self.lastIndex = 0
	       goalChosen = corners[0]

	  else: #if there was no food nearby
	     
	     foodNotCorner = False #now seeking a corner again
	     if index<len(corners): #if the index corresponds to a real slot in corners make the corner the new goal
	       goalChosen = corners[index]

	     else: #otherwise reset the index to 0 and 
	       self.lastIndex = 0
	       goalChosen = corners[0]

	#if pacman was looking for a corner and you reached it (+/-1 from pacman location)
        if foodNotCorner == False and (currentLocationOfPacman == goalChosen or ((currentLocationOfPacman[0] == (goalChosen[0]+1)) and (currentLocationOfPacman[1] == (goalChosen[1]+1))) or ((currentLocationOfPacman[0] == (goalChosen[0]-1)) and (currentLocationOfPacman[1] == (goalChosen[1]-1))) or ((currentLocationOfPacman[0] == (goalChosen[0]+1)) and (currentLocationOfPacman[1]==(goalChosen[1]-1))) or ((currentLocationOfPacman[0]==(goalChosen[0]-1)) and (currentLocationOfPacman[1] == (goalChosen[1]+1)))):

            self.lastIndex = index+1 #increase the index

            if self.lastIndex<len(corners): #if index is still valid update reachedCorners and goalChosen
	      self.reachedCorners[index-1] = goalChosen
	      goalChosen = corners[self.lastIndex]

	    else:
	      #all corners have been reached so the first nearby food is made the goal if possible
	      foodNearby = api.food(state)
	      
	      if (len(foodNearby)>0):
		if(len(foodNearby[0])>0): #if the first food in the list is valid then make that the goal and update that you are searching for food and not a corner
		  goalChosen = foodNearby[0]
		  foodNotCorner = True
		else: #reset index to 0 and make the first corner the goal
		  self.lastIndex = 0
		  foodNotCorner = False #looking for a corner again
		  goalChosen = corners[0]
		  
        if (goalChosen[0]<currentLocationOfPacman[0]): #x of goal is less than pacman's current x
            if (self.lastMove!=Directions.EAST): #this line is here to stop the pacman getting into a loop of west-east-west-east etc.
                if Directions.WEST in legal: #only move west if it is legal
                    self.lastMove = Directions.WEST
                    return api.makeMove(Directions.WEST, legal)
            elif Directions.WEST in legal: #if previous move was east do not go west
                legal.remove(Directions.WEST)

        if (goalChosen[0]>currentLocationOfPacman[0]):#x of goal is more than pacman's current x
            if (self.lastMove!=Directions.WEST): #this line is here to stop the pacman getting into a loop of west-east-west-east etc.
                if Directions.EAST in legal: #only move east if it is legal
                    self.lastMove = Directions.EAST
                    return api.makeMove(Directions.EAST, legal)
            elif Directions.EAST in legal: #if previous move was west do not go east
                legal.remove(Directions.EAST)

        if (goalChosen[1]<currentLocationOfPacman[1]):  #y of goal is less than pacman's currentY
            if (self.lastMove!=Directions.NORTH): #this line is here to stop the pacman getting into a loop of north-south-north-south etc.
                if Directions.SOUTH in legal:#only move south if it is legal
                    self.lastMove = Directions.SOUTH
                    return api.makeMove(Directions.SOUTH, legal)
            elif Directions.SOUTH in legal: #if previous move was north do not go south
                    legal.remove(Directions.SOUTH)
                
        if (goalChosen[1]>currentLocationOfPacman[1]): #y of goal is more than pacman's currentY
            if (self.lastMove!=Directions.SOUTH): #this line is here to stop the pacman getting into a loop of north-south-north-south etc.
                if Directions.NORTH in legal:#only move north if it is legal
                    self.lastMove = Directions.NORTH
                    return api.makeMove(Directions.NORTH, legal)
            elif Directions.NORTH in legal: #if previous move was south do not go north
                    legal.remove(Directions.NORTH)


	if (len(legal) == 0): #if there are no legal methods left re-add the stop move to legal
	  legal.append(Directions.STOP)
	
	randomchoice = random.choice(legal)  #if all else (everything above) fails just make a random move
        self.lastMove = randomchoice

        return api.makeMove(randomchoice, legal)
        
   