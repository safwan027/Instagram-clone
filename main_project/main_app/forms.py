from django.forms import ModelForm
from . models import story

class StoryForm(ModelForm):
    class Meta:
        model = story
        fields = ['image','fk_user'] 