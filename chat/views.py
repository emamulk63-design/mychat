from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def home(request):
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'home.html', {'users': all_users})

@login_required
def chat_view(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ) | Message.objects.filter(
        sender=receiver, receiver=request.user
    )
    messages = messages.order_by('timestamp')
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                text=text
            )
        return redirect('chat', username=username)
    
    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages
    })
