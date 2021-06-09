from canvasapi import Canvas
from quiz_creator.participation_quiz import ParticipationQuiz
from quiz_test import *

if __name__ == "__main__":
    
    # get user input for the url
    url = getAPIURL()
    print("Got url: '",url,"'",sep='')

    # get user input for the api key
    key = getAPIKEY()
    print("Got key: '",key,"'",sep='')

    # now we have enough information to make our canvas object
    canvas = getCanvas(url, key)
    print("Got canvas: '",canvas,"'",sep='')

    # OHH OKAY IT LOOKS LIKE THIS ONE MIGHT NOT EVEN BE NEEDED! WHOOPS
    # get user input for the canvas's user
    user = getUser(canvas)
    print("Got user: '",user,"'",sep='')
    
    # get user input for the course
    course = getCourse(canvas)
    print("Got course: '",course,"'",sep='')

    assignment_name = "Test Quiz"
    number_of_activities = 4

    quiz = ParticipationQuiz(course, assignment_name, number_of_activities)

    quiz.upload_to_canvas(course)