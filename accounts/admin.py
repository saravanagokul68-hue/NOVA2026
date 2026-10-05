from django.contrib import admin

from .models import (
    Event,
    Booking,
    UserProfile,
    Notification
)


# =====================================================
# EVENT ADMIN
# =====================================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "location",
        "event_date",
        "event_time",
        "price",
        "created_at",
    )

    list_filter = (
        "category",
        "event_date",
    )

    search_fields = (
        "title",
        "category",
        "location",
    )

    ordering = (
        "event_date",
        "event_time",
    )


# =====================================================
# BOOKING ADMIN
# =====================================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "event",
        "tickets",
        "status",
        "booking_date",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "user__username",
        "event__title",
    )


# =====================================================
# USER PROFILE ADMIN
# =====================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "phone",
        "roll_number",
        "register_number",
        "course",
        "semester",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "register_number",
        "roll_number",
    )


# =====================================================
# NOTIFICATION ADMIN
# =====================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "title",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "user__username",
        "title",
        "message",
    )

    ordering = (
        "-created_at",
    )