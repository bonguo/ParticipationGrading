from canvasapi import Canvas
from StudentClass import Student

# each interaction comes from a submission
class Interaction:
    # an interaction HAS students involved
    # an interaction HAS a duration
    
    # initialize interaction without any arguments?
    def __init__(self, activity, duration, participants, user_id, quiz_id):
        self.activity = activity
        self.duration = duration
        self.participants = participants
        self.user_id = user_id # the Student that this Interaction belongs to
        self.quiz_id = quiz_id # ID of the quiz this Interaction belongs to
    
    def addStudent(self, student):
        # maybe do input validation here, check whether student is duplicate, etc
        self.students.append(student)
        
    def setDuration(self, duration):
        # check how the duration compares with other reported durations for this interaction?
        self.duration = duration
    
    def getActivity(self):
        return self.activity

    def getDuration(self):
        return self.duration
    
    def getParticipants(self):
        return self.participants

    def getQuizID(self):
        return self.quiz_id