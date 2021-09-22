from canvasapi import Canvas
from StudentClass import Student
import pandas as pd

class Group:
    # a group HAS a name
    # a group HAS an ID
    # a group HAS students
    # a group HAS interactions between students
    
    # initialize Group by passing in canvas group object
    def __init__(self, canvas_group_object):
        self.name = canvas_group_object.name
        self.group_id = canvas_group_object.id
        
        # set of student objects in this group
        self.students = set()
        self.interactions = None # for now
        self.participant_ids = self.setParticipantIDs(canvas_group_object)

    # get a list of Students in the group and save to self.students
    def addStudentToGroup(self, studentObject):
        self.students.add(studentObject)

    def setParticipantIDs(self, canvas_group_object):
        users = canvas_group_object.get_users()
        student_ids = []
        for user in users:
            student_ids.append(user.id)
        return student_ids

    # check that name, ID, and SIS match; student is in group
    # used to make sure the interactions are with people in the specific group
    # student should be a Student object
    def checkStudentInGroup(self, canvas_group_object, student):
        if student in canvas_group_object.getStudents():
            return True
        else:
            return False

    # get the group's name
    def getName(self):
        return self.name
        
    # get the group's ID
    def getGroupID(self):
        return self.group_id
    
    # get the group's students
    def getStudents(self):
        return self.students
    
    def getParticipantIDs(self):
        return self.participant_ids

    # get all interactions in a dataframe
    def getAllInteractions(self):
        allInteractions = []
        for student in self.students:
            for interaction in student.getInteractions():
                allInteractions.append(interaction)
        
        return pd.DataFrame([vars(interaction) for interaction in allInteractions])

    # def getInteractions(self):
    #     return self.interactions