#!/home/bob/anaconda2/bin/python

from random import randrange
import os

def nextNote(notePosition,arraySize): 
    newPosition = -1
    while (newPosition < 0) or (newPosition >= arraySize):
        interval = randrange(10) - 5   # between -5 and +5
        newPosition = notePosition + interval
    return newPosition

os.system('cat fakeBebopHeader.ttl')

# A bar is 1920 ticks. Ride cymbal starts at the beginning. 
# bassTicksStart = 3840 means that bass starts after 2 bars.

ticksToPlay = 32280 
bassTicksStart = 3840
trumpetTicksStart = 7680

############# create bass notes ###########

# Potential notes to play are stored in arrays like this. Here it's
# just all the notes (i.e. chromatic scale) but the use of an array
# means that other scales could easily be used.
bassNotes = []
for midiNoteVal in range(28,53):   # bass note values: 28 - 52
    bassNotes.append(midiNoteVal)

bassNotePosition = len(bassNotes)/2 # first bass note

# bass event list: start with setup events defined in header file
bassEventList = """
mid:bassTrack a mid:Track ;
    mid:hasEvent bt:event0000,
        bt:event0001,
        bt:event0002,
        bt:event0003,
        bt:event0004,
        bt:event0005,
        bt:event0006,
        bt:event0007,
        bt:event0008,
        bt:event0009,
        bt:event0010,
        bt:event0011,
        bt:event0012,
        bt:event0013,
        bt:event0014,
        bt:event0015,
        bt:event0016,
        bt:event0017,
        bt:event0018,
        bt:event0019,
        bt:event0020,
        bt:event0021
"""

eventNum = 21    # most recent one

bassNoteEventPair = """
bt:EVENT-ON-NAME a mid:NoteOnEvent ;
    mid:channel 2 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 1 ;
    mid:velocity 112 .

bt:EVENT-OFF-NAME a mid:NoteOnEvent ;
    mid:channel 2 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 479 ;
    mid:velocity 0 .
"""

bassTicks = bassTicksStart
firstOneFixed = False
while (bassTicks < ticksToPlay):
    # Output the information about each as we calculate it and
    # append each event's URI to the bassEventList, which will be
    # output at the end.
    
    # Select the note
    bassNotePosition = nextNote(bassNotePosition,len(bassNotes))
    note = bassNotes[bassNotePosition]
    # make a copy of the note event pair template and replace note and both event numbers
    noteEventPair = bassNoteEventPair
    noteEventPair = noteEventPair.replace("PITCHNUMBER",str(note))
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-ON-NAME",eventLocalName)
    bassEventList = bassEventList + ",\nbt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-OFF-NAME",eventLocalName)
    bassEventList = bassEventList + ",\nbt:" + eventLocalName
    if firstOneFixed == False:
        # The very first note should start after 4 bars.
        noteEventPair = noteEventPair.replace("mid:tick 1","mid:tick " + str(bassTicksStart))
        firstOneFixed = True
    print noteEventPair
    bassTicks += 480
    
eventNum += 1
eventLocalName = "event" + str(eventNum).zfill(4)
print "bt:" + eventLocalName + " a mid:EndOfTrackEvent ;\n    mid:data \"[]\" ;\n    mid:tick 1 ."
bassEventList = bassEventList + ",\nbt:" + eventLocalName
bassTicks += 1
print bassEventList + " ."
    

####### create trumpet notes ########

trumpetNotes = []
for midiNoteVal in range(58,84):   # trumpet note values
    trumpetNotes.append(midiNoteVal)

trumpetNotePosition = len(trumpetNotes)/2 # first trumpet note
# trumpet event list: start with setup events defined in header file
trumpetEventList = """
mid:trumpetTrack a mid:Track ;
    mid:hasEvent tt:event0000,
        tt:event0001,
        tt:event0002,
        tt:event0003,
        tt:event0004,
        tt:event0005,
        tt:event0006,
        tt:event0007,
        tt:event0008,
        tt:event0009,
        tt:event0010,
        tt:event0011,
        tt:event0012,
        tt:event0013,
        tt:event0014,
        tt:event0015,
        tt:event0016
"""

eventNum = 16    # most recent one

# output two of these with the second tick value being 287 then 191.
trumpetNoteEventPair = """
tt:EVENT-ON-NAME a mid:NoteOnEvent ;
    mid:channel 0 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 1 ;
    mid:velocity 112 .

tt:EVENT-OFF-NAME a mid:NoteOnEvent ;
    mid:channel 0 ;
    mid:pitch PITCHNUMBER ;
    mid:tick TICKNUMBER ;
    mid:velocity 0 .
"""

# Create trumpet notes.
trumpetTicks = trumpetTicksStart
firstOneFixed = False
while (trumpetTicks < ticksToPlay):
    # Output the first of two notes
    trumpetNotePosition = nextNote(trumpetNotePosition,len(trumpetNotes))
    note = trumpetNotes[trumpetNotePosition]
    # make a copy of the note event pair template and replace note and both event numbers
    noteEventPair = trumpetNoteEventPair
    noteEventPair = noteEventPair.replace("PITCHNUMBER",str(note))
    noteEventPair = noteEventPair.replace("TICKNUMBER","287")
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-ON-NAME",eventLocalName)
    trumpetEventList = trumpetEventList + ",\ntt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-OFF-NAME",eventLocalName)
    trumpetEventList = trumpetEventList + ",\ntt:" + eventLocalName
    # Change 1/5 of notes to be a rest instead
    if (randrange(5) == 0):
           noteEventPair = noteEventPair.replace("velocity 112","velocity 0")

    if firstOneFixed == False:
        # The very first note should start after 8 bars.
        noteEventPair = noteEventPair.replace("mid:tick 1","mid:tick " + str(trumpetTicksStart))
        firstOneFixed = True
    print noteEventPair

    # Output the second of two notes. Very redundant code.
    trumpetNotePosition = nextNote(trumpetNotePosition,len(trumpetNotes))
    note = trumpetNotes[trumpetNotePosition]
    # make a copy of the note event pair template and replace note and both event numbers
    noteEventPair = trumpetNoteEventPair
    noteEventPair = noteEventPair.replace("PITCHNUMBER",str(note))
    noteEventPair = noteEventPair.replace("TICKNUMBER","191")
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-ON-NAME",eventLocalName)
    trumpetEventList = trumpetEventList + ",\ntt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-OFF-NAME",eventLocalName)
    trumpetEventList = trumpetEventList + ",\ntt:" + eventLocalName
    if (randrange(5) == 0):
           noteEventPair = noteEventPair.replace("velocity 112","velocity 0")
    print noteEventPair

    trumpetTicks += 480

eventNum += 1
eventLocalName = "event" + str(eventNum).zfill(4)
print "tt:" + eventLocalName + " a mid:EndOfTrackEvent ;\n    mid:data \"[]\" ;\n    mid:tick 1 ."
trumpetEventList = trumpetEventList + ",\ntt:" + eventLocalName
trumpetTicks += 1

print trumpetEventList + " ."
    
########### drums ##########    

drumEventList = """
mid:drumsTrack a mid:Track ;
    mid:hasEvent dt:event0000,
        dt:event0001,
        dt:event0002,
        dt:event0003,
        dt:event0004,
        dt:event0005,
        dt:event0006,
        dt:event0007,
        dt:event0008
"""

eventNum = 8   # most recent one

hihatEventsTemplate = """
dt:EVENT1NAME a mid:NoteOnEvent ;
    mid:channel 9 ;
    mid:pitch 57 ;
    mid:tick 479 ;
    mid:velocity 0 .

dt:EVENT2NAME a mid:NoteOnEvent ;
    mid:channel 9 ;
    mid:pitch 57 ;
    mid:tick 1 ;
    mid:velocity 80 .

dt:EVENT3NAME a mid:NoteOnEvent ;
    mid:channel 9 ;
    mid:pitch 57 ;
    mid:tick 319 ;
    mid:velocity 0 .

dt:EVENT4NAME a mid:NoteOnEvent ;
    mid:channel 9 ;
    mid:pitch 57 ;
    mid:tick 1 ;
    mid:velocity 80 .

dt:EVENT5NAME a mid:NoteOnEvent ;
    mid:channel 9 ;
    mid:pitch 57 ;
    mid:tick 159 ;
    mid:velocity 0 .

dt:EVENT6NAME a mid:NoteOnEvent ;
    mid:channel 9 ;
    mid:pitch 57 ;
    mid:tick 1 ;
    mid:velocity 80 .
"""

drumTicks = 0
while (drumTicks < ticksToPlay):
    hihatEventSet = hihatEventsTemplate;
    # More very repetitive code!
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    hihatEventSet = hihatEventSet.replace("EVENT1NAME",str(eventLocalName))
    drumEventList = drumEventList + ",\ndt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    hihatEventSet = hihatEventSet.replace("EVENT2NAME",str(eventLocalName))
    drumEventList = drumEventList + ",\ndt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    hihatEventSet = hihatEventSet.replace("EVENT3NAME",str(eventLocalName))
    drumEventList = drumEventList + ",\ndt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    hihatEventSet = hihatEventSet.replace("EVENT4NAME",str(eventLocalName))
    drumEventList = drumEventList + ",\ndt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    hihatEventSet = hihatEventSet.replace("EVENT5NAME",str(eventLocalName))
    drumEventList = drumEventList + ",\ndt:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    hihatEventSet = hihatEventSet.replace("EVENT6NAME",str(eventLocalName))
    drumEventList = drumEventList + ",\ndt:" + eventLocalName

    drumTicks += 960
    print hihatEventSet

eventNum += 1
eventLocalName = "event" + str(eventNum).zfill(4)
print "dt:" + eventLocalName + " a mid:EndOfTrackEvent ;\n    mid:data \"[]\" ;\n    mid:tick 1 ."
drumEventList = drumEventList + ",\ndt:" + eventLocalName
drumTicks += 1

print drumEventList + " ."

