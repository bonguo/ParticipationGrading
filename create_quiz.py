from canvasapi import Canvas
from quiz_creator.participation_quiz import ParticipationQuiz
from datetime import datetime, timedelta
from quiz_test import *

if __name__ == "__main__":
    
    # get user input for the url
    # url = getAPIURL()
    # print("Got url: '",url,"'",sep='')
    url = 'https://canvas.ucdavis.edu'

    # get user input for the api key
    # key = getAPIKEY()
    # print("Got key: '",key,"'",sep='')
    key = '3438~S5MKJLaQYYFCVtVHFHQnxmSwi1hhoyMx7LfOl9Ih0ecClOUrQJTun5wZ0dzzFxqe'

    # now we have enough information to make our canvas object
    canvas = getCanvas(url, key)
    print("Got canvas: '",canvas,"'",sep='')

    # get user input for the course
    course = getCourse(canvas)
    print("Got course: '",course,"'",sep='')

    # Set the new assignment name and the number of interaction questions
    # assignment_name = input("Please name the assignment: ")
    assignment_name = "NEW Test Quiz"

    # num_activities = int(input("Please choose the number of interaction questions in the quiz: "))
    num_interactions = 4

    # Ask for the time range of the study group
    start = input("Please enter the start date of the study group in MM/DD/YYYY format: ")
    end = input("Please enter the end date of the study group in MM/DD/YYYY format: ")

    start = datetime.strptime(start, "%m/%d/%Y")
    end = datetime.strptime(end, "%m/%d/%Y")
    dates_list = [start + timedelta(days=x) for x in range((end-start).days + 1)]

    # Create the quiz
    quiz = ParticipationQuiz(course, assignment_name, num_interactions, dates_list)

    try:
        quiz.upload_to_canvas(course)
        print('Quiz uploaded to Canvas')
    except Exception as e:
        print('Quiz did not successfully upload to Canvas')
        print(e)