from canvasapi import Canvas
from InteractionClass import Interaction

class Student:
    # a student HAS a name
    # a student HAS some identification
    # a student HAS Interactions

    # initialize Student object with name and id
    def __init__(self, canvas_user_object):
        self.name = canvas_user_object.name
        self.ID = canvas_user_object.id
        self.SIS = canvas_user_object.sis_user_id # might not need
        self.group_id = None
        self.interactions = {} # maps question ID to interaction
        self.quiz_grades = {} # maps quiz ID to grade
    
    # set the group that the student is in
    def setStudentGroup(self, group_id):
        self.group_id = group_id
    
    # set the student's Interactions
    def setInteractions(self, stud_inters):
        self.interactions = stud_inters

    # Create a new Interaction object in the self.interactions dictionary
    def addInteraction(self, question_id, quiz_id):
        self.interactions[question_id] = Interaction(quiz_id, question_id)

    def updateInteractions(self, question_id, q_type, data):
        self.interactions[question_id].updateInteraction(q_type, data)

    # returns the student's name
    def getName(self):
        return self.name
    
    # returns the student's id
    def getID(self):
        return self.ID
    
    # returns the student's sis user id
    def getSIS(self):
        return self.SIS

    # returns the student's group ID
    def getName(self):
        return self.group_id
    
    # returns the student's dictionary of question ID : Interaction objects
    def getInteractions(self):
        return self.interactions