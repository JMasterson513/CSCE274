#Copyright 2019 Joeseph Masterson, Cassidy Carter, Alfred Stephenson II

from State import State
import math
import time

perimeter = 2000.0 # perimeter of the polygon
velocity = 100.0 # set velocity of the robot
totalAngle = 360 # degrees in a circle
angularVelocity = 200.0 / 235.0
safe = 131 # opcode for safe mode
start = 128 # opcode for start mode
stop = 173 # opcode for stop mode
straightRadius = 0
turnRadius = 1

class part3Loop:
    def __init__(self): #default constructor
        self.State = State()
        self.State.state(start)
        self.State.state(safe)

    #calculates time to sleep on the sides
    def sleepStraight(self, N):
        sideLength = perimeter/N
        sideTime = sideLength / velocity
        return sideTime
    
    #Calculates the time to sleep on turn
    def sleepTurn(self, N):
        interiorAngle = (N - 2) * 180
        individualAngle = (interiorAngle/N)
        exteriorAngle = 180 + individualAngle 
        sleepTime = 2 * ( math.radians(abs(360 - exteriorAngle))/ (2*angularVelocity)) 
        return sleepTime

    #method to drive in the shape of a polygon
    def drivePolygon(self, N):
        straightSleep = self.sleepStraight(N)
        cornerSleep = self.sleepTurn(N)

        for i in range(N):
            self.State.drive(velocity, straightRadius)
            while time.sleep(straightSleep):
                print "sleeping"
                self.checkCleanButton()

            self.State.drive(velocity, turnRadius )
            while time.sleep(cornerSleep):
                self.checkCleanButton()

        self.State.drive(0,0)

    def checkCleanButton(self):
        print self.State.readState()
        return bool(self.State.readState())

roomba = part3Loop()
roomba.drivePolygon(6)
