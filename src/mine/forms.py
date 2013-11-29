from django import forms
from django.forms import ModelForm
from mine.models import UserSurvey
CHOICES_1=[('True','True'),
         ('False','False')]
CHOICES_2=[('1','your field'),
         ('2','everyone in your group\'s field'),
         ('3','the least completed field in your group')]
CHOICES_3=[('1','1'),
         ('2','2'),
         ('3','3'),
         ('10','10'),]
CHOICES_4=[('True','True'),
         ('False','False')]
CHOICES_5=[('True','True'),
         ('False','False')]    

class SurveyForm(ModelForm):
	class Meta:
		model = UserSurvey
		# fields = ['nationality','gender','agree','']
		exclude = ['user_profile']
		labels = ['','','']
		help_texts = {
            'nationality': ('Some useful help text.'),
        }

class InstructionForm(forms.Form):
	q1 = forms.ChoiceField(choices=CHOICES_1, widget=forms.RadioSelect(), label = '1. True or false: "Switching" incurs no cost or reduction in clicking completion level.')
	q2 = forms.ChoiceField(choices=CHOICES_2, widget=forms.RadioSelect(), label = '2. Which field determines payoffs?')
	q3 = forms.ChoiceField(choices=CHOICES_3, widget=forms.RadioSelect(), label = '3. Including you, how many members will be in your group?')
	q4 = forms.ChoiceField(choices=CHOICES_4, widget=forms.RadioSelect(), label = '4. True or False: The "switch back" button incurs no cost or reduction of clicking completion level.')
	q5 = forms.ChoiceField(choices=CHOICES_5, widget=forms.RadioSelect(), label = '5. True or false: A group will only contain members from the same country.')
