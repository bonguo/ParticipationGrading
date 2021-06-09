from canvasapi import Canvas
from InteractionClass import Interaction

# submissions lend to interactions
class Submission:
    def __init__(self, canvas_submission_object):

        self.submissionID = canvas_submission_object.submission_id
        self.quizID = canvas_submission_object.quiz_id
        self.userID = canvas_submission_object.user_id
    
    # set the group that the student is in
    def setStudentGroup(self, group_id):
        self.group = group_id
    
    # returns the student's name
    def getUserID(self):
        return self.name
    
    # returns the student's id
    def getID(self):
        return self.ID
    
    # returns the student's sis user id
    def getSIS(self):
        return self.SIS