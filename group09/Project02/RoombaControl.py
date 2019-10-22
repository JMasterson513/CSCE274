# Copyright 2019 Joe Masterson, Cassidy Carter, and Alfred Stephenson II

from Interface import Interface
import struct

# Element of the packet where clean is returned
clean = 0

# Opocde for the drive method
drive = 137

# queries for the package
query = 142 

# Opcode for the full mode
full = 132

# Packet which tells state of the buttons
button_packet = 18

# Packet which tells state of drop sensor
drop_packet = 7

# Packet for the left cliff sensor
cliff_left = 9

# Packet for the front left cliff sensor
cliff_front_left = 10

# Packet for the front right cliff sensor
cliff_front_right = 11

# Packet for right cliff sensor
cliff_right = 12

# Packet for the virtual wall sensor
virtual_wall = 13

# Packet for the distance 
distance_packet = 19

# Packet for the angle
angle_packet = 20

# Opcode for Drive Direct
drive_direct = 145

# Opcode for the song
song = 140

# Constant to divide by when getting the anlge
angle_divisor = 0.324056
class RoombaControl:

    # Default Constructor - connects to the romba
    def __init__(self):
        self.Interface = Interface()
        self.FullMode()
    
    # Sets the set of the robot
    def state(self, state):
        #self.Interface.send(chr(state))
        self.Interface.send(struct.pack('B', state))

    # Gets a string of the buttons hit 
    def readButton(self):
        sent_string = struct.pack('BB', query, button_packet) # ask for the button state
        self.Interface.send(sent_string) 
        received_string = self.Interface.read(1) # read in the state

        button_push = struct.unpack('B', received_string) # Interpert the state
        return button_push[clean]

    # Sends the drive command to the robot
    def drive(self, velocity, radius):
        packed = struct.pack('>B2h', drive, velocity, radius)
        self.Interface.send(packed)
    
    # Sets the robot to full mode
    def FullMode(self):
        self.state(full)

    def PacketQuery(self, packet, packet_size):
        sent_string = struct.pack('BB', query, packet)
        self.Interface.send(sent_string)
        recieved_string = self.Interface.read(packet_size)
        return struct.unpack('B', recieved_string)

    def PacketSignedQuery( self, packet, packet_size):
        sent_string = struct.pack('bb' , query, packet)
        self.Interface.send(sent_string)
        recieved_string = self.Interface.read(packet_size)
        return struct.unpack('b' , recieved_string)

    def readDrop(self):
        drop_push = str(self.PacketQuery(drop_packet, 1))

        return drop_push[0], drop_push[1], drop_push[2], drop_push[3]

    def readCliff(self):
        # Left 
        left_cliff = str(self.PacketQuery(cliff_left, 1))

        # Left Front
        left_front = str(self.PacketQuery(cliff_front_left, 1))

        # Right
        right_cliff = str(self.PacketQuery(cliff_right, 1))

        # Right Front
        right_front = str(self.PacketQuery(cliff_front_right, 1))

        # Virtual Wall
        virtual_wall_state = str(self.PacketQuery(virtual_wall, 1))

        return left_cliff, left_front, right_cliff, right_front, virtual_wall_state

        #TODO deal with signed ints
        def DistanceRead(self):
            distance_read = self.PacketSignedQuery(distance_packet, 2)
            return distance_read

        #TODO deal with signed ints and converting to radians - do we need to divide?
        def AngleRead(self):
            angle_read = self.PacketSignedQuery(angle_read, 2)
            return angle_read / angle_divisor

        def DriveDirect(self, rightVelocity, leftVelocity):
            direct_pack = struct.pack('>B2h', drive_direct, rightVelocity, leftVelocity)
            self.Interface.send(direct_pack)

        def Song(self, song_length, note_length):
            count = song_length / note_length
            notes = []
            while count > 0:
                print("Enter note frequency: ")
                notes.append(raw_input)
                notes.append(note_length)
            song = struct.pack('BBBB', song, 1, song_length, notes)
            self.Interface.send(song)

                
roomba = RoombaControl()

while True:
    print(roomba.readDrop())