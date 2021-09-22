from canvasapi import Canvas
from datetime import datetime
import re

groupmates = {'p1', 'p2', 'p3', 'p4'}
acts = {'Do introductions', 'Play a game', 'School-related topics', 'Non-school-related topics'}

class Interaction:
    # initialize Interaction object with quiz_id and question_id
    # possibly also add the Student it belongs to, to self.participants?
    def __init__(self, user_id, inter_owner_obj):
        # self.quiz_id = quiz_id
        self.interaction_owner = user_id
        self.activities = set()
        self.participants = {inter_owner_obj} # set of Student objects
        self.duration = None
        self.validated = False
    
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

    def setDate(self, date):
        dt_obj = datetime.strptime(date, "%m/%d/%Y")
        self.date = dt_obj

    # update the appropriate attributes of the Interaction object
    def updateInteraction(self, q_type, data, name_to_student):
        if q_type in groupmates:
            # get Student object from name
            self.addParticipant(name_to_student[data])
        elif q_type in acts:
            self.addActivity(data)
        elif q_type == 'duration':
            self.setDuration(data)
        elif q_type == 'date':
            self.setDate(data)
        else:
            print("Unexpected answer:", data)
    
    # Return the set of activities done by the Student in this Interaction
    def getActivities(self):
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

    # Return the date that this Interaction occured
    def getDate(self):
        return self.date