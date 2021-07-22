from canvasapi import Canvas
import re

groupmates = {'p1', 'p2', 'p3', 'p4'}
acts = {'Do introductions', 'Play a game', 'School-related topics', 'Non-school-related topics'}

class Interaction:
    # initialize Interaction object with quiz_id and question_id
    # possibly also add the Student it belongs to, to self.participants?
    def __init__(self, quiz_id, question_id):
        self.quiz_id = quiz_id
        self.question_id = question_id
        self.activities = set()
        self.participants = set()
        self.duration = None

    """def __init__(self, activities, duration, participants, user_id, quiz_id):
        self.activities = activities # set of activities in the Interaction
        self.duration = duration
        self.participants = participants # includes the user themselves
        self.user_id = user_id # the Student that this Interaction belongs to
        self.quiz_id = quiz_id # ID of the quiz this Interaction belongs to"""
    
    def addParticipant(self, student):
        # set datatype ensures that there are no duplicates
        self.participants.add(student)

    def addActivity(self, activity):
        # add a new activity type to the set
        self.activities.add(activity)
        
    def setDuration(self, duration):
        # strip non-numeric characters from the string, convert to int, set duration
        duration = int(re.sub('[^0-9]', '', duration))
        self.duration = duration

    # update the appropriate attributes of the Interaction object
    def updateInteraction(self, q_type, data):
        if q_type in groupmates:
            self.addParticipant(data) # this is just the name, get user_id somehow?
        elif q_type in acts:
            self.addActivity(data)
        elif q_type == 'duration':
            self.setDuration(data)
        else:
            print("Unexpected answer:", data)
    
    # Return the set of activities done by the Student in this Interaction
    def getActivity(self):
        return self.activities

    # Return the duration of this Interaction
    def getDuration(self):
        return self.duration
    
    # Return the set of participants in this Interaction
    def getParticipants(self):
        return self.participants

    # Return the ID of the quiz this Interaction belongs to
    def getQuizID(self):
        return self.quiz_id