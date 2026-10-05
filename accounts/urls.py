from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # LOGIN
    # =====================================================

    path(
        "login/",
        views.student_login,
        name="student_login"
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),


    # =====================================================
    # EVENTS
    # =====================================================

    path(
        "events/",
        views.events,
        name="events"
    ),


    # =====================================================
    # BOOK EVENT
    # =====================================================

    path(
        "book/<int:event_id>/",
        views.book_event,
        name="book_event"
    ),


    # =====================================================
    # BOOKING SUCCESS
    # =====================================================

    path(
        "booking-success/",
        views.booking_success,
        name="booking_success"
    ),


    # =====================================================
    # MY TICKETS
    # =====================================================

    path(
        "my-tickets/",
        views.my_tickets,
        name="my_tickets"
    ),


    # =====================================================
    # DIGITAL TICKET
    # =====================================================

    path(
        "ticket/<int:booking_id>/",
        views.digital_ticket,
        name="digital_ticket"
    ),


    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "logout/",
        views.student_logout,
        name="student_logout"
    ),


    # =====================================================
    # PROFILE
    # =====================================================

    path(
        "profile/",
        views.student_profile,
        name="student_profile"
    ),


    # =====================================================
    # EDIT PROFILE
    # =====================================================

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),


    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),


    # =====================================================
    # VERIFY TICKET
    # =====================================================

    path(
        "verify-ticket/",
        views.verify_ticket,
        name="verify_ticket"
    ),


    # =====================================================
    # NOVA AI
    # =====================================================

    path(
        "nova-ai/",
        views.nova_ai,
        name="nova_ai"
    ),

]