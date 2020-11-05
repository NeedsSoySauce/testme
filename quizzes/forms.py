from django import forms


class QuestionForm(forms.Form):
    """ Renders it's answers as radio buttons or checkboxes based on the 'multi' flag. """
    # answer = forms.ChoiceField(widget=forms.RadioSelect, label=False)
    answers = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', tuple())
        multi = kwargs.pop('multi', False)
        super().__init__(*args, **kwargs)

        if multi:
            self.fields['answers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

        answers = self.fields['answers']
        answers.choices = choices
        answers.label = False

    def clean_answers(self):
        data = self.cleaned_data['answers']
        # Always return answers as a list
        if not isinstance(data, list):
            return [data]
        return data
