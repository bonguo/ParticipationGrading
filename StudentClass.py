from canvasapi import Canvas
from InteractionClass import Interaction

class Student:
    # initialize Student object with name and id
    def __init__(self, canvas_user_object):
        self.name = canvas_user_object.name
        self.ID = canvas_user_object.id
        self.SIS = canvas_user_object.sis_user_id # might not need
        self.group_id = None
        self.interactions = []
        self.quiz_grades = {} # maps quiz ID to grade

    # when you print(Student) it'll print the name
    def __str__(self) -> str:
        return self.name
    
    # set the group that the student is in
    def setStudentGroup(self, group_id):
        self.group_id = group_id

    # Create a new Interaction object in the self.interactions dictionary
    def addInteraction(self, user_id, inter_owner_obj):
        self.interactions.append(Interaction(user_id, inter_owner_obj))

    def updateInteractions(self, q_type, data, name_to_student):
        self.interactions[-1].updateInteraction(q_type, data, name_to_student)

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