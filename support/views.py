from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SupportTicket
from .forms import SupportTicketForm

def support_page(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.status = 'Open'
            ticket.save()

            # Create Notification
            from notifications.models import Notification
            Notification.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.session_key,
                title="Support Ticket Submitted",
                message=f"Your support ticket regarding '{ticket.subject}' has been submitted. Status: Open."
            )

            messages.success(request, "Support ticket submitted successfully! We will contact you soon.")
            return redirect('support_page')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        # Prepopulate name and email if user is authenticated
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': request.user.username,
                'email': request.user.email,
            }
        form = SupportTicketForm(initial=initial)

    return render(request, 'support_test.html', {'form': form})

