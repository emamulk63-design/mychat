from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message
from accounts.models import Profile


@login_required
def home(request):

    users = User.objects.exclude(id=request.user.id)

    chat_list = []

    for user in users:

        profile, created = Profile.objects.get_or_create(user=user)

        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by("-timestamp").first()

        unread = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()

        chat_list.append({
            "user": user,
            "profile": profile,
            "last_message": last_message,
            "unread": unread,
        })

    chat_list.sort(
        key=lambda x: x["last_message"].timestamp if x["last_message"] else 0,
        reverse=True
    )

    return render(
        request,
        "home.html",
        {
            "chat_list": chat_list
        }
    )


@login_required
def chat_view(request, username):

    receiver = get_object_or_404(User, username=username)

    Profile.objects.get_or_create(user=receiver)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by("timestamp")

    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    if request.method == "POST":

        text = request.POST.get("text")

        if text:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                text=text,
            )

        return redirect("chat", username=username)

    return render(
        request,
        "chat.html",
        {
            "receiver": receiver,
            "messages": messages,
        }
    )
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Message

@staff_member_required
def admin_dashboard(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    messages = Message.objects.all().order_by("-timestamp")

    return render(request, "admin_dashboard.html", {
        "users": users,
        "profiles": profiles,
        "messages": messages,
        "total_users": users.count(),
        "total_messages": messages.count(),
    })
