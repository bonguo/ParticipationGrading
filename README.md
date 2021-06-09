# ParticipationGrading
Code for interacting with the Canvas API in order to automatically grade group participation

To run this code you will need:
* The most recent version of Python
* The Python canvasapi library, which you can get by doing $: pip install canvasapi
* Low expectations
* The Python pandas library, which you can get by doing $: pip install pandas
* Access to a Canvas page where you can get your account's API Key

TODO plan:
* Get the URL and KEY from the user
    * The KEY is unique to each user, but maybe we could have a dummy Canvas account linked to somone's alternative email (or a new email) which just has a key we use for everyone
    * All users could just use the same key, and the dummy account can be added as admin in whatever class needs to have the participation automatically graded
* Select the class
    * This can't be hardcoded in because there are multiple classes for which the participation grader will be used
* Select the assignment
    * Again, this can't be hardcoded because of all the different assignments
    * You might not need to select from a long assignment list though. Maybe it could just look for assignments that have "Participation", or maybe "Group", in the name
* Download the information for the submissions from each student, for the chosen quiz

Okay now's the part where I'm not sure the best approach
* Option 1: Storing students and interactions in a weighted-graph-like structure, where Students are the nodes and Interactions are the weighted edges
    * Interactions with the entire group could just be considered as individual interactions between each member of the group, but we would need to be careful about how we keep track of time in that case
    * Each time we go to add a new Interaction, we would check if that edge already exists. If it does exist, we would need to make sure the two people are in agreement about the interaction length and description
        * There would be a problem though, if a student reports a group interaction (we store it as X individual interactions) but then also reports an individual interaction with someone from that group. In that case, an edge would already exists. So we're either adding to that edge or making a second parallel edge, neither option I like
    * This option obviously has problems with keeping track of individual vs group interactions...
* Option 2: We have two classifications for interactions, group and individual, and we just keep a list (or maybe a dictionary, or something else) for each type
    * Individual interactions are just between 2 students and should be relatively simple to check because we only need to compare two people's times and descriptions
    * Group interactions can be created whenever someone says the interacted with more than one other person. Then we could check the other students and see if they reported the same group interaction
        * Figuring out which people to add to the group interaction might be difficult... I don't remember whether the student submission objects had the student's name anywhere (but hey, we could just add a "what's your name" question to the participation quiz)
    * I like the potential for this option, more than the graph

Things to look further into:
* Can we see the student groups from the API (the actual command is course.get_groups( ), so that's worth checking out)
    * Update: get_groups() works, and from each group you can get the students who are in the group
    * Currently the Group class deals with making the Student objects, although we'll need some way to check whether there are any students who *didn't* get put in groups somehow
* The Interaction class should be for keeping track of student interactions.
* When we're reading student quiz answers, the process might go something like this:
    * You (Zanthrop) say you interacted with Adam, Bob, and Carson for a certain duration
    * We check whether there's already an existing interaction between Zanthrop, Adam, Bob, and Carson
    * If there is, we make sure the durations are similar enough
        * What happens next?
    * If there's not, then we create the new Interaction instance
        * What happens next?
* Once all the users quizzes have been read in, we can go through each group and tally up the total interaction time each student has, and assign grades from there
