from datetime import datetime
from InteractionClass import Interaction
from StudentClass import Student
from dataclasses import dataclass

@dataclass
class InteractionCenter:
    participants: "dict[Student, float]"
    avgDate: int
    avgDuration: int
    activities: "dict[str, float]"

class InteractionGroup:
    # add type-hinting
    def __init__(self, group, interaction: Interaction):
        self.interactions = [interaction]
        self.group = group
        self.participants = group.getStudents() # set of student objects
        self.activities = {'Do introductions', 'Play a game', 'School-related topics', 'Non-school-related topics'}
        self.center = self.calculateCenter()

    # return combined interaction groups
    # add an argument: cutoff point for similarity
    # add an argument: function that computes the differences
    def combineGroups(self, interactionGroup):
        for group in interactionGroup.getInteractions():
            self.interactions.append(group)

        self.center = self.calculateCenter()

        return self

    # TODO: save time by not recalculating everything upon merge?
    # TODO: break sections down into separate functions
    def calculateCenter(self):
        # calculate the total number of interactions in this InteractionGroup
        numInteractions = len(self.interactions)

        # participants:
            # imagine an array of numbers, one for each person in the group
            # holding the percentage of times each person occured in the "same" interactions
            # sum up the differences in percentages for each person's appearance between interaction groups

        # map student object to percentage they occur; start at 0
        participants = {student : 0 for student in self.participants}

        # for every interaction in this InteractionGroup
        for interaction in self.interactions:
            # for every student in each interaction
            for student in interaction.getParticipants():
                # if the student belongs in the Group that we're grading
                if student in self.participants:
                    # add the appropriate percentage of their occurance to the dictionary
                    participants[student] += (1/numInteractions)

        # date:
            # average date via datetime.timestamp() to get POSIX timestamp
        
        totalTime = 0
        # for every interaction in this InteractionGroup
        for interaction in self.interactions:
            # get the date of the interaction as a datetime object
            dt_obj = interaction.getDate()

            # convert the datetime object to POSIX timestamp and add
            totalTime += datetime.timestamp(dt_obj)

        avgDate = totalTime / numInteractions
        
        # duration:
            # average duration reported

        totalDuration = 0
        # for every interaction in this InteractionGroup
        for interaction in self.interactions:
            # get the duration of the interaction and add
            totalDuration += interaction.getDuration()

        avgDuration = totalDuration / numInteractions
        # divide by units of time aka distance between options (5min)

        # activities:
            # similar to participants

        # map activities to percentage they occur; start at 0
        activities = {activity : 0 for activity in self.activities}

        # for every interaction in this InteractionGroup
        for interaction in self.interactions:
            # for every student in each interaction
            for act in interaction.getActivities():
                # add the appropriate percentage of its occurance to the dictionary
                activities[act] += (1/numInteractions)

        # use python dataclass
        return InteractionCenter(participants, avgDate, avgDuration, activities)

    def getInteractions(self):
        return self.interactions

    # TODO: use participants, avgDate, avgDuration, and activities to compare between InteractionGroups
    def getCenter(self):
        return self.center

# https://www.desmos.com/calculator/awm8v3ygrj for distance function