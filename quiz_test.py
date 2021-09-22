
from canvasapi import Canvas
import urllib.request
import pandas as pd
import pprint
from StudentClass import Student
from GroupClass import Group
# from InteractionClass import Interaction
# from SubmissionClass import Submission
from func_utils import *
    
###############################
######## Main Function ########
###############################

if __name__ == "__main__":
    
    # get user input for the url
    # url = getAPIURL()
    url = 'https://canvas.ucdavis.edu'
    print("Got url: '",url,"'",sep='')

    # get user input for the api key
    # key = getAPIKEY()
    key = '3438~S5MKJLaQYYFCVtVHFHQnxmSwi1hhoyMx7LfOl9Ih0ecClOUrQJTun5wZ0dzzFxqe'
    print("Got key: '",key,"'",sep='')

    # now we have enough information to make our canvas object
    canvas = getCanvas(url, key)
    print("Got canvas: '",canvas,"'",sep='')
    
    # get user input for the course
    course = getCourse(canvas)
    print("Got course: '",course,"'",sep='')

    # Make a few dictionaries
    # id_to_student maps student IDs (ints) to Student objects
    # name_to_student maps student names to Student objects (possibility of repeat)
    id_to_student = {}
    name_to_student = {}
    users = course.get_users(enrollment_type=['student'])
    for user in users:
        stu = Student(user)
        id_to_student[user.id] = stu
        name_to_student[user.sortable_name] = stu

    # get the user input for the quiz
    quiz = getQuiz(course)
    print("Got quiz: '",quiz,"'",sep='')

    quiz_stats = list(quiz.get_statistics())[0].question_statistics

    # iterate through the main questions in the quiz
    for question in quiz_stats:
        # get the question id
        question_id = question['id']
        if question['question_type'] == 'multiple_dropdowns_question':
            # Go through the answer sets
            # each dropdown is a sub-question for each question
            # initialize an empty set of students that have responded to this question here
            responded = set()
            for dropdown in question['answer_sets']:
                # the question type -- p1, p2, etc.
                q_type = dropdown['text']
                # each answer is a possible answer in the dropdown
                for answer in dropdown['answers']:
                    # the actual text answer from the dropdown
                    selection = answer['text']
                    # each user is someone who chose this particular answer
                    # for this particular dropdown
                    # for this particular question
                    for user_id in answer['user_ids']:
                        # if the answer has not been left blank, handle it
                        if selection != 'No Answer':
                            # if student ID is not in that responded set, then this Interaction does not exist yet
                            # create the interaction and add their ID to the set
                            if user_id not in responded:
                                id_to_student[user_id].addInteraction(user_id, id_to_student[user_id])
                                responded.add(user_id)

                            # update the last interaction in their interactions list                            
                            # add data to the appropriate section of that Interaction
                            id_to_student[user_id].updateInteractions(q_type, selection, name_to_student)

    # By the end of this for loop, we should have:
    # a dictionary mapping student IDs to Student objects
    # each Student object has a dictionary mapping question IDs to Interaction objects
    # each Interaction object has the participants, activities, and duration set,
        # if that particular Student selected those options for that question in the quiz

    # Now let's put those students into their Groups
    
    # get the groups of a particular course
    groups = getGroups(course)

    # convert each group to a Group object
    # then put them into a master group_list
    group_list = []
    for group in groups:
        # initialize group with group name, ID, and participant student IDs
        g = Group(group)

        # Add the appropriate Student objects to the group students list
        for id in g.getParticipantIDs():
            g.addStudentToGroup(id_to_student[id])
        group_list.append(g)

    # DONE: change participants from strings to Student objects
    # TODO: handle students with identical names

    # Now we have:
        # a list of Groups
        # each Group has a list of Students
        # each Student has a list of Interactions
        # each Interaction is composed of Student participants

    # time to grade the Interactions!
    for group in group_list:
        gradeSubmissions(group)

    exit()

# General outline to implement:
    # Just ask:
        # is the name selected in the group?
        # How would I compare Interactions by hand?

    # For each group
        # For each member in that group
            # For each interaction that they reported
                # Verify that interaction against the report of the student's that they said they interacted with

# group all interactions that are similar
    # place each interaction into its own InteractionGroup
    # shouldn't have an interaction group that contains multiple interactions reported by the same person
        # infinite distances between interaction groups with interactions reported by the same person
    # repeat the following until convergence:
        # 1. find the pairwise distances from the center of EACH interaction group
        # to the center of the other interaction groups
        # 2. if the minimum of all those distances is beneath some cutoff, merge the two groups together
        # otherwise, stop the algorithm
        # 3. the center of an interaction group:
            # participants:
                # imagine an array of numbers, one for each person in the group
                # holding the percentage of times each person occured in the "same" interactions
                # sum up the differences in percentages for each person's appearance between interaction groups
            # date:
                # average date via datetime.timestamp()
            # duration:
                # average duration reported
            # activities:
                # similar to participants
        # 4. Algorithm to say where "similarity" cuts off 
            # each difference is an increasing penalty -- exponential growth function
                # weight * field_base ** diff
                    # scale * diff * field_base ** diff to make the distance 0 when diff is 0
                    # or make it a piecewise function -- if diff is 0, it's 0; otherwise...
                # weight (between 0 and 1) specifies how important this field is in our overall calculation
                # field_base is a constant for each field
                # diff must be on the same scale for all fields
            # scales need to be the same for each field (participants, date, etc.)
                # for duration, divide by 5 (step size)
                # for participants and activities, max difference is group size / number of activities
                # make everything out of 5?
                # the scale of the difference affects how much each individual discrepency is penalized
            # sum up the distances for each field to get the total difference between the centers of InteractionGroups

    # Machine learning:
        # optimize the grouping by optimizing the distance function

# for those interactions, award credit for:
    # minimum duration
    # average duration
    # most common duration
# who to give the credit to:
    # percentage of appearance within the interaction
    # so how many of the similar interactions that they appear in
    # potential hard limit: you need to appear in x% of the interactions to get full credit
        # will have to manually ask the students who didn't report the student in the interaction
        # can maybe automate an email
    # other possibility: you get awarded the amount of credit (in minutes) multiplied by the percentage of appearance

# For people who don't submit, but are involved in interactions
    # award full credit to the person who did turn in the assignment
    # award no credit to the person who didn't turn it in

# When actually scoring assignments, double check that they're still in the class
    # because people drop

# Other option:
    # Do you have an interaction with me that took about the same time at around the same time?

    # TODO: how many differences do you want to allow?