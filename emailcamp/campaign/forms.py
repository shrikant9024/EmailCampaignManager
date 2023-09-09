from django import forms
from .models import Subscriber, Campaign

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email','first_name']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['subject', 'html_content', 'published_date']