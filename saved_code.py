# print all submissions for a particular quiz
    submissions = quiz.get_submissions()
    all_interactions = []
    sub_list = []
    print("Got submissions: ")
    for submission in submissions:
        print(submission)
        new_submission = Submission(submission)
        # each submission has a userID -- use this to add to Student object
        # take each submission and make it into a list of interactions
        # assign each interaction to the student in the right group
        
        # all_interactions = recordSubmission(submission, all_interactions)