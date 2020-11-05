from django.test import TestCase

from quizzes.forms import QuestionForm


class QuestionFormTests(TestCase):
    def setUp(self):
        self.choices = [(i, f'answer_{i}') for i in range(4)]

    def test_renders_checkboxes_when_multiple_choice(self):
        """ When multi is True answers are rendered as multiple choice checkboxes. """
        form = QuestionForm(choices=self.choices, multi=True)
        self.assertIn('checkbox', str(form))

    def test_renders_radio_buttons_when_not_multiple_choice(self):
        form = QuestionForm(choices=self.choices, multi=False)
        self.assertIn('radio', str(form))

    def test_cleaned_answers_is_always_list(self):
        data = {"answers": [choice[0] for choice in self.choices]}

        form = QuestionForm(data=data, choices=self.choices, multi=True)
        form.full_clean()
        answers = form.cleaned_data['answers']
        self.assertIsInstance(answers, list)

        data = {"answers": self.choices[0][0]}
        form = QuestionForm(data=data, choices=self.choices, multi=False)
        form.full_clean()
        answers = form.cleaned_data['answers']
        self.assertIsInstance(answers, list)
