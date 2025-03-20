# views.py
from django.shortcuts import render


def template_preview(request):
    """
    Dev View function to preview the email templates
    """
    # Add your context data and change the HTML template to see the preview
    context = {
        'name': "Test"
    }
    return render(request, 'emails/account/delete_account_confirmation.html', context)
