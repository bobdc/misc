#!/home/bob/anaconda2/bin/python

from random import randrange
import os

def nextNote(notePosition,arraySize): 
    newPosition = -1
    while (newPosition < 0) or (newPosition >= arraySize):
        interval = randrange(10) - 5   # between -5 and +5
        newPosition = notePosition + interval
    return newPosition

os.system('cat wholeTonePianoQuarterNotesHeader.ttl')

# A bar is 1920 ticks.

ticksToPlay =24000
maxTick = 76

############# create bass notes ###########

# Potential notes to play are stored in arrays like this. Here it's
# just all the notes (i.e. chromatic scale) but the use of an array
# means that other scales could easily be used.
trebleClefNotes = []
for midiNoteVal in range(28,43): 
    trebleClefNotes.append(midiNoteVal * 2)  # to make a whole tone scale

trebleNotePosition = len(trebleClefNotes)/2 # first bass note

# bass event list: start with setup events defined in header file
trebleClefEventList = """
mid:pianoHeadertrack00 a mid:Track ;
    mid:hasEvent p1:event0000,
        p1:event0001,
        p1:event0002,
        p1:event0003,
        p1:event0004,
        p1:event0005,
        p1:event0006,
        p1:event0007,
        p1:event0008,
        p1:event0009
"""

eventNum = 9    # most recent one

trebleNoteEventPair = """
p1:EVENT-ON-NAME a mid:NoteOnEvent ;
    mid:channel 0 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 1 ;
    mid:velocity 80 .

p1:EVENT-OFF-NAME a mid:NoteOnEvent ;
    mid:channel 0 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 479 ;
    mid:velocity 0 .
"""

trebleClefTicks = 0
while (trebleClefTicks < ticksToPlay):
    # Output the information about each as we calculate it and
    # append each event's URI to the trebleClefEventList, which will be
    # output at the end.
    
    # Select the note
    trebleNotePosition = nextNote(trebleNotePosition,len(trebleClefNotes))
    note = trebleClefNotes[trebleNotePosition]
    # make a copy of the note event pair template and replace note and both event numbers
    noteEventPair = trebleNoteEventPair
    noteEventPair = noteEventPair.replace("PITCHNUMBER",str(note))
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-ON-NAME",eventLocalName)
    eventOnTickValue = 100 + randrange(maxTick)*10 # multiple of 10 to encourage intervals
    noteEventPair = noteEventPair.replace("EVENT-ON-TICK",str(eventOnTickValue))
    trebleClefEventList = trebleClefEventList + ",\np1:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-OFF-NAME",eventLocalName)
    eventOffTickValue = 100 + randrange(maxTick)*10
    noteEventPair = noteEventPair.replace("EVENT-OFF-TICK",str(eventOffTickValue))
    # Change random 1/2 of notes to be a rest instead
    if (randrange(2) == 0):
           noteEventPair = noteEventPair.replace("velocity 80","velocity 0")
    trebleClefEventList = trebleClefEventList + ",\np1:" + eventLocalName
    print noteEventPair
    trebleClefTicks += 480
    
eventNum += 1
eventLocalName = "event" + str(eventNum).zfill(4)
print "p1:" + eventLocalName + " a mid:EndOfTrackEvent ;\n    mid:data \"[]\" ;\n    mid:tick 1 ."
trebleClefEventList = trebleClefEventList + ",\np1:" + eventLocalName
trebleClefTicks += 1
print trebleClefEventList + " ."
    

####### create bassClef notes ########

bassClefNotes = []
for midiNoteVal in range(19,35): 
    bassClefNotes.append(midiNoteVal*2)  # to make a whole note scale

bassClefNotePosition = len(bassClefNotes)/2 # first bassClef note
# bassClef event list: start with setup events defined in header file
bassClefEventList = """
mid:pianoHeadertrack01 a mid:Track ;
    mid:hasEvent p2:event0000,
        p2:event0001
"""

eventNum = 1    # most recent one

bassClefNoteEventPair = """
p2:EVENT-ON-NAME a mid:NoteOnEvent ;
    mid:channel 0 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 1; 
    mid:velocity 80 .

p2:EVENT-OFF-NAME a mid:NoteOnEvent ;
    mid:channel 0 ;
    mid:pitch PITCHNUMBER ;
    mid:tick 479;
    mid:velocity 0 .
"""

# Create bassClef notes.
bassClefTicks = 0
while (bassClefTicks < ticksToPlay):
    # Output the first of two notes
    bassClefNotePosition = nextNote(bassClefNotePosition,len(bassClefNotes))
    note = bassClefNotes[bassClefNotePosition]
    # make a copy of the note event pair template and replace note and both event numbers
    noteEventPair = bassClefNoteEventPair
    noteEventPair = noteEventPair.replace("PITCHNUMBER",str(note))
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-ON-NAME",eventLocalName)
    bassClefEventList = bassClefEventList + ",\np2:" + eventLocalName
    eventNum += 1
    eventLocalName = "event" + str(eventNum).zfill(4)
    noteEventPair = noteEventPair.replace("EVENT-OFF-NAME",eventLocalName)
    # Change random 1/2 of notes to be a rest instead
    if (randrange(2) == 0):
           noteEventPair = noteEventPair.replace("velocity 80","velocity 0")
    bassClefEventList = bassClefEventList + ",\np2:" + eventLocalName
    print noteEventPair

    bassClefTicks += 480

eventNum += 1
eventLocalName = "event" + str(eventNum).zfill(4)
print "p2:" + eventLocalName + " a mid:EndOfTrackEvent ;\n    mid:data \"[]\" ;\n    mid:tick 1 ."
bassClefEventList = bassClefEventList + ",\np2:" + eventLocalName
bassClefTicks += 1

print bassClefEventList + " ."
