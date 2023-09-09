from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Subscriber, Campaign
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib import messages 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import SubscriberForm, CampaignForm
from django.urls import reverse


def add_subscriber(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        subscriber, created = Subscriber.objects.get_or_create(email=email, defaults={'first_name': first_name})
        if created:
            # Subscriber added successfully
            return redirect(reverse('subscribers_list'))

    return render(request, 'add_subscriber.html')
def subscribers_list(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'subscribers_list.html', {'subscribers': subscribers})


def unsubscribe(request, email):
    try:
        subscriber = Subscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.save()
        message = "You have been unsubscribed successfully."
    except Subscriber.DoesNotExist:
        message = "Subscriber not found."
    
    return render(request, 'unsubscribe.html', {'message': message})



def send_campaigns(request):
    today = timezone.now().date()
    campaigns = Campaign.objects.filter(published_date=today)

    for campaign in campaigns:
        subject = campaign.subject
        message = campaign.html_content  # Use this if campaign content is HTML
        sender_email = 'myemail@email.com'

        recipient_list = []
        active_subscribers = Subscriber.objects.filter(is_active=True)
        for subscriber in active_subscribers:
            recipient_list.append(subscriber.email)

        try:
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
        except Exception as e:
            return HttpResponse(f'Error sending email: {str(e)}')

    
    return render(request, 'campaigns_sent.html')

def render_campaign_email(request, campaign_id):
    try:
        # Retrieve the campaign object from the database using the campaign_id
        campaign = Campaign.objects.get(pk=campaign_id)
        
        # Load the email template
        email_template = loader.get_template('campaign_email_template.html')
        
        # Context data to be passed to the template
        context = {
            'campaign': campaign,
        }
        
        # Render the email content using the template and context
        email_content = email_template.render(context)
        
        # Here, you can send the email with the email_content
        # You can use your email sending function here
        
        # For demonstration purposes, let's just return the email content as an HTTP response
        return HttpResponse(email_content)
    
    except Campaign.DoesNotExist:
        # Handle the case where the campaign with the given ID does not exist
        return HttpResponse('Campaign not found', status=404)
def test_email(request):
    subject = 'Test Email'
    message = 'This is a test email sent via Mailgun SMTP.'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient@example.com']

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent successfully')
    except Exception as e:
        return HttpResponse('Email could not be sent: {}'.format(str(e)))
