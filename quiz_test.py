
from quiz_creator.participation_quiz import ParticipationQuiz
from canvasapi import Canvas
import urllib.request
import pandas as pd
import pprint
from parseStudent import parse
from StudentClass import Student
from GroupClass import Group
from InteractionClass import Interaction
from SubmissionClass import Submission
from func_utils import *

# big ideas:

# User inputs the url
# User inputs their api_key
# User inputs (or chooses) the user
# User inputs (or chooses) the course id
# User inputs (or chooses) the quiz id
# All user submissions get downloaded
# more stuff happens


# potentially useful API functions:
# course .get_quizzes() returns a list of quizzes
# course .get_recent_students() returns a list of students in order
                            # of how recently they've logged on
# course .get_user(userID) returns the User
# course .get_users() returns all users!
# quiz .get_submissions() returns all submissions
# quiz .get_statistics() returns all statistics (rebeca said this was good?)
# quizSubmission .get_submission_questions() returns quizSubmissionQuestion's
# quizSubmission .update_score_and_comments() somehow send the "fudge points"??

    
##############################
######## Main Function #######
##############################

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

    # OHH OKAY IT LOOKS LIKE THIS ONE MIGHT NOT EVEN BE NEEDED! WHOOPS
    # get user input for the canvas's user
    # user = getUser(canvas)
    # print("Got user: '",user,"'",sep='')
    
    # get user input for the course
    course = getCourse(canvas)
    print("Got course: '",course,"'",sep='')

    # Make a dictionary mapping student IDs (ints) to Student objects
    student_dict = {}
    users = course.get_users()
    for user in users:
        student_dict[user.id] = Student(user)

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
                        # if this Interaction does not exist in the Student's interactions, create it
                        if selection != 'No Answer':
                            if question_id not in student_dict[user_id].getInteractions():
                                # in Student.interactions, maps question_id to Interaction
                                student_dict[user_id].addInteraction(question_id, quiz.id)
                            # now add data to the appropriate section of that Interaction
                            student_dict[user_id].updateInteractions(question_id, q_type, selection)

    # By the end of this for loop, we should have:
    # a dictionary mapping student IDs to Student objects
    # each Student object has a dictionary mapping question IDs to Interaction objects
    # each Interaction object has the participants, activities, and duration set,
        # if that particular Student selected those options for that question in the quiz

    # Now let's put those students into their Groups
    
    exit()
    # Get the right quiz
    studentReport = quiz.create_report("student_analysis")
    reportProgress = None

    # URL of canvas progress object from studentReport
    reportProgressURL = studentReport.progress_url

    # parse so only the process id remains
    prefix = 'https://canvas.ucdavis.edu/api/v1/progress/'
    if reportProgressURL.startswith(prefix):
        reportProgressID = reportProgressURL[len(prefix):]
    else: 
        reportProgressID = reportProgressURL

    # wait for student report to finish generating while the process has not completed or failed 
    while reportProgress != 'completed' and reportProgress != 'failed':
        reportProgressObj = canvas.get_progress(reportProgressID)
        reportProgress = reportProgressObj.workflow_state

    studentReportN = quiz.create_report("student_analysis")
    url = studentReportN.file["url"]
    studentData = pd.read_csv(url)

    """ To help get question IDs:
    for key in studentData.keys():
        print("-------------------------")
        print("Key:",key, sep='\n')
        print("-----------")
        print("Value:",studentData[key],sep='\n')
    """

    # have this return a dictionary 
    # key: userID
    # value: list of Interactions
    # then when we build the group we can insert the Interactions for each student
    sub_dict = parse(studentData, course.id, quiz.id)

    print(sub_dict)

    # get the groups of a particular course
    groups = getGroups(course)

    # for group in groups:
    #     print("\n\nPrinting group '",group.name,"'",sep='')
    #     print(group.__dict__)
    #     print("------------------\nMembers:")
        
    #     users = group.get_users()
        
    #     print("------------------")
    #     for user in users:
    #         print("Printing users '",user.name,"'",sep='')
    #         print(user.__dict__)
    #         print("------------------")

    # convert each group to a Group object
    # then put them into a master group_list
    group_list = []
    for group in groups:
        # initialize group with group name, group ID, and group Students
        g = Group(group)

        # for each group, add the Interactions to each Student!
        g.addInteractions(sub_dict)

        group_list.append(g)

    # create a dictionary mapping each group_id to their list of Student objects
    # remember that each student has an attribute identifying their group as well
    group_dict = {}
    for g in group_list:
        group_dict[g.getID()] = g.getStudents()
        
        # print(g.getName())
        # print(g.getID())
        # print(g.getStudents())

    # print(group_dict)
    # exit()

    # Now we have:
        # a list of Groups
        # each Group has a list of Students
        # each Student has a list of Interactions

    # time to grade the Interactions!
    for group in group_list:
        gradeSubmissions(quiz.id, group)

    # get user input for the assignment
    #assignment = getAssignment(course)
    #print("Got assignment: '",assignment,"'",sep='')

    #getQuizSubmissions(quiz)
    #getSubmissions(quiz)


    # Bonnie interacts with Scott
    # Scott interacts with Bonnie and Matthew
    # Matthew interacts with Bonnie and Scott


    # Questions:
    # How to import list of student names into quiz? Automatically generate quiz?
    # How should we be checking groups?
        # Right now I'm looking at all submissions. From each submission, I can get the submitting user ID and their answers,
        # but their answers will be the *names* of their group members -- I can't match them to ID
        # I also have access to a dictionary mapping each group_id to a list of Student objects
            # Student objects have name, id, group ID, and a list of Interactions
        # Compile submissions by Group?
            # get the user_ids of each Student in each Group
            # using the user ids, search through the master submission list, since you can check by user_id
            # get the list of Interactions for each student in the group
            # check them against each other somehow? this is the part I'm having trouble with
                # For each participant in each Interaction, check that they have a matching interaction
                # For each Interaction, add a 'validated' attribute?
            # tally up valid durations
            # add a grade attribute to each Student in the Group?
    # Separately: should there be Interaction IDs? Composed of user_id + quiz_id + question_id?
        # Used to make sure students don't match their own interactions? Or will that not be a problem?
        # Maybe it's only a problem if I compile a master list of Interactions and check for identical ones?

# General outline to implement:
    # We have a list of all submissions
        # From the submission, we can get user ID
    # We have a dictionary mapping each group_id to their list of Student objects
        # Each Student object has name and ID

    
    # Form Groups of Students
    # Each Student in the Group has a list of Interactions
    # Each Interaction contains: activity, duration, Students involved

    # Make a master list of Interactions within each group
    # For each Interaction in the Group, check within that master list for a matching ones, per participant


    # Make a dictionary that maps each student in the class to their ID and use that?
        # Issue with repeat names

    # Autogenerate Canvas quiz question dropdown with student names and IDs?
        # Did Rebecca do this last quarter? Or you, for the Kudo points?

    # Just ask:
        # is the name selected in the group?
        # How would I compare Interactions by hand?

    # For each group
        # For each member in that group
            # For each interaction that they reported
                # Verify that interaction against the report of the student's that they said they interacted with