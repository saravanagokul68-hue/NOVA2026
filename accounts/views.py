from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

import qrcode
import base64

from io import BytesIO

from .models import (
    UserProfile,
    Event,
    Booking,
    Notification
)


# =========================================================
# HOME
# =========================================================

def home(request):

    return render(
        request,
        "accounts/home.html"
    )


# =========================================================
# LOGIN
# =========================================================

def student_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                "student_dashboard"
            )

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def student_dashboard(request):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        "event"
    ).order_by(
        "-id"
    )

    total_tickets = sum(
        booking.tickets
        for booking in bookings
    )

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "profile": profile,
            "bookings": bookings,
            "total_tickets": total_tickets,
            "unread_notifications": unread_notifications,
            "total_bookings": bookings.count(),
            "total_tickets": total_tickets,
        }
    )


# =========================================================
# EVENTS
# =========================================================

@login_required
def events(request):

    events = Event.objects.all().order_by(
        "event_date",
        "event_time"
    )

    return render(
        request,
        "accounts/events.html",
        {
            "events": events
        }
    )


# =========================================================
# BOOK EVENT
# =========================================================

@login_required
def book_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    if request.method == "POST":

        tickets = request.POST.get(
            "tickets",
            "1"
        )

        try:
            tickets = int(tickets)
        except (ValueError, TypeError):
            tickets = 1

        if tickets < 1:
            tickets = 1

        booking = Booking.objects.create(
            user=request.user,
            event=event,
            tickets=tickets,
            status="Confirmed"
        )

        Notification.objects.create(
            user=request.user,
            title="Booking Confirmed 🎟️",
            message=(
                f"Your booking for {event.title} "
                f"has been confirmed. "
                f"You booked {tickets} ticket(s)."
            )
        )

        return redirect(
            "booking_success"
        )

    return render(
        request,
        "accounts/book_event.html",
        {
            "event": event
        }
    )


# =========================================================
# BOOKING SUCCESS
# =========================================================

@login_required
def booking_success(request):

    booking = Booking.objects.filter(
        user=request.user
    ).select_related(
        "event"
    ).order_by(
        "-id"
    ).first()

    return render(
        request,
        "accounts/booking_success.html",
        {
            "booking": booking
        }
    )


# =========================================================
# MY TICKETS
# =========================================================

@login_required
def my_tickets(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        "event"
    ).order_by(
        "-id"
    )

    return render(
        request,
        "accounts/my_tickets.html",
        {
            "bookings": bookings
        }
    )


# =========================================================
# DIGITAL TICKET
# =========================================================

@login_required
def digital_ticket(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    qr_data = (
        f"NOVA2026|"
        f"Booking:{booking.id}|"
        f"User:{request.user.username}|"
        f"Event:{booking.event.title}|"
        f"Tickets:{booking.tickets}"
    )

    qr = qrcode.make(
        qr_data
    )

    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return render(
        request,
        "accounts/digital_ticket.html",
        {
            "booking": booking,
            "qr_code": qr_code
        }
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def student_logout(request):

    logout(request)

    return redirect(
        "student_login"
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def student_profile(request):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile
        }
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.phone = request.POST.get(
            "phone",
            ""
        )

        profile.roll_number = request.POST.get(
            "roll_number",
            ""
        )

        profile.register_number = request.POST.get(
            "register_number",
            ""
        )

        profile.course = request.POST.get(
            "course",
            ""
        )

        semester = request.POST.get(
            "semester",
            ""
        )

        if semester:

            try:
                profile.semester = int(
                    semester
                )
            except (ValueError, TypeError):
                profile.semester = 0

        profile.save()

        return redirect(
            "student_profile"
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "profile": profile
        }
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required
def notifications(request):

    notification_list = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        "accounts/notifications.html",
        {
            "notifications": notification_list
        }
    )


# =========================================================
# VERIFY TICKET
# =========================================================

@login_required
def verify_ticket(request):

    booking = None
    error = ""

    if request.method == "POST":

        booking_id = request.POST.get(
            "booking_id",
            ""
        ).strip()

        if not booking_id:

            error = "❌ Please enter a booking ID."

        else:

            try:

                booking = Booking.objects.select_related(
                    "event",
                    "user"
                ).get(
                    id=int(booking_id)
                )

            except (
                Booking.DoesNotExist,
                ValueError,
                TypeError
            ):

                error = "❌ Invalid ticket. Booking not found."

    return render(
        request,
        "accounts/verify_ticket.html",
        {
            "booking": booking,
            "error": error
        }
    )


# =========================================================
# NOVA AI
# =========================================================

@login_required
def nova_ai(request):

    answer = ""

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        "event"
    ).order_by(
        "-id"
    )

    chat_history = request.session.get(
        "nova_chat_history",
        []
    )

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if request.GET.get("clear") == "1":

        request.session[
            "nova_chat_history"
        ] = []

        request.session.modified = True

        return redirect(
            "nova_ai"
        )

    # =====================================================
    # ASK NOVA
    # =====================================================

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        ).strip()

        question_lower = question.lower()

        # HELLO
        if question_lower in [
            "hello",
            "hi",
            "hey"
        ]:

            answer = (
                "👋 Hello! I'm NOVA AI. "
                "I'm ready to help you with "
                "your NOVA2026 journey."
            )

        # EVENT DATE / TIME
        elif (
            "when is my event" in question_lower
            or "my event date" in question_lower
            or "my event time" in question_lower
        ):

            if bookings.exists():

                booking = bookings.first()

                answer = (
                    "🚀 Your booked event is:\n\n"
                    f"🎟️ {booking.event.title}\n"
                    f"📅 Date: "
                    f"{booking.event.event_date.strftime('%d %b %Y')}\n"
                    f"⏰ Time: "
                    f"{booking.event.event_time.strftime('%I:%M %p')}"
                )

            else:

                answer = (
                    "📋 You don't have a booked event yet. "
                    "Visit the Events section to book one."
                )

        # BOOKINGS
        elif (
            "booking" in question_lower
            or "bookings" in question_lower
        ):

            if bookings.exists():

                booking = bookings.first()

                total_amount = (
                    booking.tickets *
                    booking.event.price
                )

                answer = (
                    "📋 Your Latest Booking\n\n"
                    f"🎟️ Event: {booking.event.title}\n"
                    f"📅 Date: "
                    f"{booking.event.event_date.strftime('%d %b %Y')}\n"
                    f"⏰ Time: "
                    f"{booking.event.event_time.strftime('%I:%M %p')}\n"
                    f"🎫 Tickets: {booking.tickets}\n"
                    f"💰 Total: ₹{total_amount:.2f}\n"
                    f"✅ Status: {booking.status}"
                )

            else:

                answer = (
                    "📋 You don't have any bookings yet."
                )

        # TICKETS
        elif "ticket" in question_lower:

            total_tickets = sum(
                booking.tickets
                for booking in bookings
            )

            answer = (
                f"🎫 You currently have "
                f"{total_tickets} ticket(s) "
                f"across {bookings.count()} booking(s).\n\n"
                "You can view your digital tickets "
                "from the My Tickets section."
            )

        # EVENTS
        elif (
            "event" in question_lower
            or "events" in question_lower
            or "fest" in question_lower
        ):

            event_list = Event.objects.all().order_by(
                "event_date",
                "event_time"
            )[:5]

            if event_list.exists():

                event_details = []

                for event in event_list:

                    event_details.append(
                        f"🚀 {event.title}\n"
                        f"📍 {event.location}\n"
                        f"📅 "
                        f"{event.event_date.strftime('%d %b %Y')}\n"
                        f"⏰ "
                        f"{event.event_time.strftime('%I:%M %p')}\n"
                        f"💰 ₹{event.price}"
                    )

                answer = (
                    "🚀 Here are the available NOVA events:\n\n"
                    +
                    "\n\n".join(
                        event_details
                    )
                )

            else:

                answer = (
                    "🚀 There are currently no events available."
                )

        # PROFILE
        elif "profile" in question_lower:

            answer = (
                "👤 You can view and edit your "
                "student profile from the Profile section."
            )

        # NAME
        elif (
            "my name" in question_lower
            or "who am i" in question_lower
        ):

            name = (
                request.user.get_full_name()
                or request.user.username
            )

            answer = (
                f"👋 Your name is {name}."
            )

        # COURSE
        elif "course" in question_lower:

            if profile:

                answer = (
                    f"📚 Your course is "
                    f"{profile.course}."
                )

            else:

                answer = (
                    "📚 Your course information "
                    "has not been added yet."
                )

        # SEMESTER
        elif "semester" in question_lower:

            if profile:

                answer = (
                    f"🎓 You are currently in "
                    f"semester {profile.semester}."
                )

            else:

                answer = (
                    "🎓 Your semester information "
                    "has not been added yet."
                )

        # REGISTER NUMBER
        elif (
            "register number" in question_lower
            or "registration number" in question_lower
            or "register no" in question_lower
        ):

            if profile:

                answer = (
                    f"🪪 Your register number is "
                    f"{profile.register_number}."
                )

            else:

                answer = (
                    "🪪 Your register number "
                    "has not been added yet."
                )

        # ROLL NUMBER
        elif (
            "roll number" in question_lower
            or "roll no" in question_lower
        ):

            if profile:

                answer = (
                    f"🔢 Your roll number is "
                    f"{profile.roll_number}."
                )

            else:

                answer = (
                    "🔢 Your roll number "
                    "has not been added yet."
                )

        # HELP
        elif "help" in question_lower:

            answer = (
                "🤖 I can help you with:\n\n"
                "🎫 Tickets\n"
                "📋 Bookings\n"
                "🚀 Events\n"
                "👤 Profile\n"
                "📚 Course\n"
                "🎓 Semester\n"
                "🪪 Register number\n"
                "🔢 Roll number"
            )

        # UNKNOWN
        else:

            answer = (
                "🤖 I'm still learning!\n\n"
                "Try asking me about your "
                "tickets, bookings, events, "
                "profile, course or semester."
            )

        # SAVE CHAT
        if question:

            chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        chat_history = chat_history[-20:]

        request.session[
            "nova_chat_history"
        ] = chat_history

        request.session.modified = True

    return render(
        request,
        "accounts/nova_ai.html",
        {
            "answer": answer,
            "chat_history": chat_history
        }
    )