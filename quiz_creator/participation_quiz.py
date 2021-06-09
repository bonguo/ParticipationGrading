import canvasapi
import datetime
from typing import List, Callable, Optional

class ParticipationQuiz:
    def __init__(self, course: canvasapi.course.Course,
                 assignment_name: str,
                 # assignment_group: canvasapi.assignment.AssignmentGroup,
                 number_of_activities,
                 due_date: Optional[datetime.datetime] = None,
                 unlock_date: Optional[datetime.datetime] = None,
                 lock_date: Optional[datetime.datetime] = None):
        """
        :param course:
        :param assignment_name:
        :param assignment_group:
        :param number_of_activities:
        :param due_date:
        :param unlock_date:
        :param lock_date:
        """
        self.user = course
        self.assignment_name = assignment_name
        #self.assignment_group = assignment_group
        self.unlock_date = unlock_date
        self.due_date = due_date
        self.lock_date = lock_date
        self.number_of_activities = number_of_activities

        students = course.get_users(sort='username', enrollment_type=['student'])
        self.students = {}
        for student in students:
            if student.sortable_name not in self.students:
                self.students[student.sortable_name] = []
            self.students[student.sortable_name].append(student)

        self.quiz_info = self._create_quiz_info()
        self.assignment_info = self._create_assignment_info()
        self.quiz_questions = self._create_quiz_questions()

    def _create_quiz_info(self) -> dict:
        prompt = """<p>Please fill out your study group participation. You can <strong>NOT </strong>count time with people not in your group.</p>
                <p>&nbsp;</p>
                <p><span style="font-family: inherit; font-size: 1rem;">After responding, please ignore Canvas's notification that your answer are incorrect. Your response has been recorded correctly, Canvas just does not know how to deal with multiple-choice questions where every answer is "correct."</span></p>"""
        return {
            'title': self.assignment_name,
            'description': prompt,
            'quiz_type': 'assignment',
            #'assignment_group_id': self.assignment_group.id,
            'allowed_attempts': 10,
            'scoring_policy': 'keep_latest',
            'published': False,
            'show_correct_answers': False,
            'due_at': self.due_date,
            'lock_at': self.lock_date,
            'unlock_at': self.unlock_date
        }

    def _create_assignment_info(self) -> dict:
        return {
            # setting grading_type to not_graded breaks the association between Quiz and Assignment
            # not sure if this is a bug on Canvas's end or what so leaving it out for now.
            # 'grading_type': 'not_graded',
            'omit_from_final_grade': True,
            'published': True
        }

    # create all the activity questions here
    def _create_quiz_questions(self) -> List[dict]:
        answers = self._create_answers()

        # four activity questions
        questions = [
            {
                'question_name': f'Interaction {act_num}',
                'question_text': """<p>What of these activities did you do? Choose 'Yes' for 'None' if you didn't do this activity.<br>
                                    <b>Warning:</b> If you select 'Yes' for 'None', the rest of your answer will not be analyzed.<br></p>
                                    <p>None: [a1]<br>Do introductions: [a2]<br>Play a game: [a3]<br>Talk about school-related topics: [a4]<br>Talk about non-school-related topics: [a5]</p><br>
                                    <p>How long did you spend on this interaction? [duration] minutes</p><br>
                                    <p>Who did you do this activity with? Choose 'None' for the remaining options if you interacted 
                                    with less than four people in your group for this activity.<br>
                                    Groupmate 1: [p1]<br>Groupmate 2: [p2]<br>Groupmate 3: [p3]<br>Groupmate 4: [p4]</p>""",
                'question_type': 'multiple_dropdowns_question',
                'answers': dict(enumerate(answers)),
                'points_possible': 1
            } for act_num in range(1, self.number_of_activities+1)
        ]

        # if they didn't interact, explain here
        questions.append({
            'question_name': f"If you couldn't meet with your group",
            'question_text': "If you did not get to interact with anyone in your group this week, please explain what happened here.",
            'question_type': 'essay_question',
            'points_possible': 1
        })

        return questions

    # create activity answers
    def _create_answers(self) -> List[dict]:
        activities = ['a1', 'a2', 'a3', 'a4', 'a5']
        durations = ['5', '10', '15', '20', '25', '30', '35', '40', '45+']
        groupmates = ['p1', 'p2', 'p3', 'p4']

        answers = []

        # participants questions
        for groupmate in groupmates:
            for student_name, student in self.students.items():
                answers.append({
                    'answer_html': ','.join([str(s.id) for s in student]),
                    'answer_text': student_name,
                    'blank_id': groupmate,
                    'answer_weight': 1
                })

            # add 'None' choice
            answers.append({
                'answer_html': ','.join([str(s.id) for s in student]),
                'answer_text': 'None',
                'blank_id': groupmate,
                'answer_weight': 1
            })

        # activity question
        for activity in activities:
            answers.append({
                'answer_text': 'Yes',
                'blank_id': activity,
                'answer_weight': 1
            })
            answers.append({
                'answer_text': 'No',
                'blank_id': activity,
                'answer_weight': 1
            })
    

        # duration question
        for duration in durations:
            answers.append({
                'answer_text': duration,
                'blank_id': 'duration',
                'answer_weight': 1
            })

        return answers

    def upload_to_canvas(self, course: canvasapi.course.Course) -> None:
        canvas_quiz = course.create_quiz(self.quiz_info)
        for question in self.quiz_questions:
            canvas_quiz.create_question(question=question)
        canvas_assignment = course.get_assignment(canvas_quiz.assignment_id)
        edited_canvas_assignment = canvas_assignment.edit(assignment=self.assignment_info)
        # edited_quiz = canvas_quiz.edit(quiz={'published': True})
        # second_assignment = course.get_assignment(canvas_quiz.assignment_id)
        pass