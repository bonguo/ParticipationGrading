from canvasapi import Canvas
import pprint
import math
import pandas as pd
# from StudentClass import Student
from InteractionClass import Interaction
import re

# create a list of Interactions for each student
# TO DO: need a way to get students by ID instead of name
#        and add them as a Student object instead of just a string

# for each question:
    # ignore if full answer is [Select]
    # if interaction is half filled, important info is missing, email student to resubmit?
    # otherwise, create an Interaction object which notes:
        # activity type
        # duration (set to 0 if no duration was selected)
        # list of students involved, including the user who submitted (set to empty list if no selection)
        # Interaction ID, composed of user_id + submission_id + i (i=1,2,3,4)
    # append each valid Interaction to all_interactions
def createInteractions(inter_arr, user_name, user_id, quiz_id):
    acts = set(['Do introductions', 'Play a game', 'School-related topics', 'Non-school-related topics'])
    # duration is always the last element in each interaction list
    durs = set(['5', '10', '15', '20', '25', '30', '35', '40', '45+'])
    
    inter_list = []
    for interaction in inter_arr:
        # check for full empty submission, nan
        if interaction != interaction:
            continue

        # set activities
        activities = interaction.intersection(acts)

        duration = 0
        durations = interaction.intersection(durs)
        for duration in durations: # should only be one
            # strip non-numeric characters from the string, convert to int
            duration = int(re.sub('[^0-9]', '', duration))

        # set of people in interaction
        participants = set()
        for item in interaction:
            if item not in acts and item not in durs:
                participants.add(item)

        # If the user added themselves under participants, first remove
        if user_name in participants:
            participants.remove(user_name)

        # First check if activities, duration, or participants are empty
        if len(activities) > 0 and duration > 0 and len(participants) > 0:
            participants.add(user_name) # add the user who submitted the interaction

            # Interaction contains the activitites (set of strs), duration (int),
            # participants (set of strs), and the user_id of the Student the Interaction belongs to
            new_inter = Interaction(activities, duration, participants, user_id, quiz_id)
            inter_list.append(new_inter)
        else:
            pass
            # Invalid interaction -- missing essential information
            # Email student to resubmit?

    # list of Interactions for a single Student
    return inter_list

def fix_names(argList):
    list_out = []
    for i, arg in enumerate(argList):
        if arg[0] == ' ':
            full_name = arg[1:] + ' ' + argList[i-1][:-1]
            list_out.append(full_name)
        elif arg[-1] != '\\':
            list_out.append(arg)
    return list_out

def parse(studentData:pd, CLASS_ID: int, quiz_id: int):
    # Fill the dictionary and the student lists
    dictSt = {}
    
    """
    #Set default to ECS 154A, but it could also be 36A
    #This will need to be changed each time the quiz is changed
    if CLASS_ID == 516271:
        activity1 = 'some other id'
        activity2 = 'some other id'   
    """

    # The list of question ids of questions 
    questionList = []

    # The numerical index location of the question
    questionsLoc = []

    # all columns in the student data csv. Need for full question string
    fullQuestionList = studentData.columns.values.tolist()
    #print(fullQuestionList)

    # Parse fullQuestionList for the question locations and IDs,
    # which are 7-digit numbers at the beginning of the string
    for i, item in enumerate(fullQuestionList):
        if len(item) > 7 and item[0:7].isdigit():
            questionList.append(item[0:7])
            questionsLoc.append(i)

    print(questionList)
    print(questionsLoc)

    # for item in questionList:
      #  questionsFull.append([word for word in fullQuestionList if item in word])
    #for item in questionsFull:
    #    questionLoc.append(studentData.columns.get_loc(item))
    questionsDict = dict(zip(questionList, questionsLoc)) 
    questionsDict['id'] = studentData.columns.get_loc('id')
    questionsDict['name'] = studentData.columns.get_loc('name')

    # print(questionsDict)
    # {'1360923': 7, '1360924': 9, '1360925': 11, '1360926': 13, '1360927': 15, 'id': 1, 'name': 0}
    # exit()

    # parse each student submission
    # compile a master dictionary of submissions and return that
    # Key: submitting user's ID
    # Value: list of Interactions
    sub_dict = {}
    for row in studentData.itertuples(index=False, name=None):
        # get user name
        name = row[questionsDict['name']]
        print("Name:", name)

        # get user id
        user_id = row[questionsDict['id']]
        print("User ID:", user_id)

        # list of lists to hold all activities
        all_interactions = []

        # get user answers for each activity
        for i, activity in enumerate(questionList):
            if i != len(questionList) - 1:
                try:
                    # Won't work when names are separated by commas
                    # Do some name pre-processing before turning it into a set
                    argList = fix_names(row[questionsDict[activity]].split(','))
                    tempArr = set(argList)
                    all_interactions.append(tempArr)
                except:
                    tempArr = "empty submission"
                print("Interaction ", i+1, ": ", tempArr, sep='')
            else: # the last question, free response, could be blank
                print("Free response:", row[questionsDict[activity]])
                # Add this to the Group Student's info somehow?
        
        # creates list of Interaction objects for this specific submission
        # can map it to the specific student for grading purposes?
        # list of Interactions for a single Student
        inter_list = createInteractions(all_interactions, name, user_id, quiz_id)

        # create dictionary entry
        sub_dict[user_id] = inter_list

    return sub_dict

    """
    for row in studentData.itertuples(index=False, name=None):

        #name and id
        tempStudent = Student(row[questionsDict['id']], row[questionsDict['name']])

        #pronouns that the student prefers
        tempArr = row[questionsDict[pronounsQ]]
        
        freeResponse = row[questionsDict[pronounsFree]]
        if len(tempArr) != 0:
            if tempArr == "Not Included":
                tempStudent.pronouns = freeResponse
            else:
                tempStudent.pronouns  = tempArr

        #preferSame is True if the student would like to share their group with someone of the same gender
        tempArr = row[questionsDict[genderMatchQ]]
        if type(tempArr) is str:
            if tempArr == "I would prefer another person who as the same pronouns as I do.":
                tempStudent.preferSame = 2
            elif tempArr == "I would prefer another person who does not have the same pronouns as I do.":
                tempStudent.preferSame = 0
            elif tempArr == "No preference":
                tempStudent.preferSame = 1


        #meeting times - Sun - Sat, Midnight-4, 4-8, 8-noon, etc  [0][0] is sunday at midnight to 4 time slot
        tempArr = row[questionsDict[timeQ]]
        if type(tempArr) is str:
            meetingTimes = tempArr.split(",")
            daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri","Sat"]
            for i in range(7):
                for j in range(1, 7):
                    if daysOfWeek[i] + str(j) in meetingTimes:
                        tempStudent.meetingTimes[i][(j - 1)] = True
        

        #asynch (2), synch (1), no pref (0)- how the student would like to meet
        studentSync = row[questionsDict[syncQ]]
        if type(studentSync) is str:
            if studentSync == "Synchronously":
                tempStudent.preferAsy = 1
            elif studentSync == "Asynchronously":
                tempStudent.preferAsy = 2
            else:
                tempStudent.preferAsy = 0

        #contact pref - Discord, Phone, Email, Canvas - 2 = yes, 1 = no preference, 0 = not comfortable
        tempArr = (row[questionsDict[commPreferenceQ]])
        if type(tempArr) is str:
            contactPreference = tempArr.split(",")
            # Parse which contact method student wants from a list
            if "Discord" in contactPreference:
                (tempStudent.contactPreference)[0] = True
            if "Text/Phone Number" in contactPreference:
                (tempStudent.contactPreference)[1] = True
            if "Email" in contactPreference:
                (tempStudent.contactPreference)[2] = True 
            if "Canvas Groups" in contactPreference: 
                (tempStudent.contactPreference)[3] = True

        #contact info - [DiscordHandle, PhoneNumber, personal@email.com]
        tempArr = (row[questionsDict[commValuesQ]])
        if type(tempArr) is str:
            contactInfo = tempArr.split(",")
            for i in range(3):
                tempStudent.contactInformation[i] = contactInfo[i]

        #prefer leader- True if they prefer to be the leader, false otherwise
        studentLeader = row[questionsDict[leaderQ]]
        if type(studentLeader) is str:
            if studentLeader == "I like to lead.":
                tempStudent.preferLeader = True
            else:
                tempStudent.preferLeader = False

        #country - Country of Origin
        '''
        tempArr = (row[studentData.columns.str.contains(countryQ)].tolist())
        freeResponse = row[studentData.columns.str.contains(countryFree)].tolist()
        
        if type(tempArr[0]) is str:
            countryResult = tempArr[0].split(",")
            if len(countryResult) == 2:
                if countryResult[0] == "Not Included":
                    tempStudent.countryOfOrigin = freeResponse[0]
                else:
                    tempStudent.countryOfOrigin = tempArr[0]
            elif len(countryResult) == 1:
                if countryResult[0] == "Yes" or tempArr[0] == "No":
                    #preferCountry - True if they would like to have a groupmate from the same country
                    if tempArr[0] == "No":
                        tempStudent.preferCountry = False
                    else: 
                        tempStudent.preferCountry = True 
                else:
                    if tempArr[1] == "No":
                        tempStudent.preferCountry = False
                    else: 
                        tempStudent.preferCountry = True
                    
        tempArr.clear()
        freeResponse.clear()
        '''

        #international student preference
        tempArr = row[questionsDict[internationalQ]]
        if type(tempArr) is str:
            if tempArr == "I would like to be placed with another international student.":
                tempStudent.international = 2
            elif tempArr == "No preference":
                tempStudent.international = 1
            elif tempArr == "I am not an international student.":
                tempStudent.international = 0

        #languages - Preferred language
        languageSelect = row[questionsDict[languageQ]]
        notIncluedeLanguage = row[questionsDict[languageFree]]
        if type(languageSelect) is str:
            if languageSelect == "Not Included":
                tempStudent.language = notIncluedeLanguage
            else:
                tempStudent.language = languageSelect
            

        #Preferred stuff to do - the drop downs and free response
        tempArr = (row[questionsDict[groupWantsQ]])
        # Take the array of one item and check if its the right type,
        # then assign to the variable
        if type(tempArr) is str:
            tempStudent.option1 = tempArr
        tempResponse = row[questionsDict[groupWantsFree]]
        if type(tempResponse) is str:
            tempStudent.freeResponse = tempResponse
        
        #Priority of what they want
        freeResponse = row[questionsDict[priorityQ]]
        if type(freeResponse) is str:
            priority = freeResponse.split(",")
            while len(priority) < 5:
                priority.append("default")
            tempStudent.priorityList = priority

        # how the student feels in the class
        tempArr = row[questionsDict[studentPerfQ]]
        if type(tempArr) is str: 
            if tempArr == "I'm confident.":
                tempStudent.confidence = 2
            elif tempArr == "I have some questions.":
                tempStudent.confidence = 1
            elif tempArr == "I could really use some help.":
                tempStudent.confidence = 0

        #Add the student to the dictionary of all students
        dictSt[row[questionsDict['id']]] = tempStudent

    return dictSt

def parseEmails(dictSt:dict, canvasClass:Canvas):
    missingSt = {}

    # update student dictionary to include people who did not take, as well as list composed of students who did not take the test
    # the class and add default emails to all students
    for user in canvasClass.get_users(enrollment_type=['student']):
        if user.id not in dictSt:
            name = user.sortable_name.split(",")
            temp = Student(user.id, user.name, user.email, name[1], name[0])
            missingSt[user.id] = temp
        else:
            name = user.sortable_name.split(",")
            tempStudent = dictSt[user.id]
            tempStudent.schoolEmail = user.email
            tempStudent.firstName = name[1]
            tempStudent.lastName = name[0]
            dictSt[user.id] = tempStudent

    return missingSt"""