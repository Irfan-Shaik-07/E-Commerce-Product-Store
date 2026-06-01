from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notification

def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def notifications_list(request):
    session_id = get_session_id(request)
    if request.user.is_authenticated:
        # Merge guest notifications if any
        guest_notifs = Notification.objects.filter(session_id=session_id)
        for notif in guest_notifs:
            notif.user = request.user
            notif.save()
        notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    else:
        notifs = Notification.objects.filter(session_id=session_id).order_by('-created_at')
        
    context = {
        'notifications': notifs,
    }
    return render(request, 'notifications_test.html', context)

def mark_read(request, notification_id):
    session_id = get_session_id(request)
    if request.user.is_authenticated:
        notif = get_object_or_404(Notification, id=notification_id, user=request.user)
    else:
        notif = get_object_or_404(Notification, id=notification_id, session_id=session_id)
        
    notif.is_read = True
    notif.save()
    messages.success(request, "Notification marked as read.")
    return redirect('notifications_list')
