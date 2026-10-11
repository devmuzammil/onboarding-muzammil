from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LeaveRequest, User


@admin.register(User)
class LeaveUserAdmin(UserAdmin):
	add_fieldsets = UserAdmin.add_fieldsets + (
		('Leave management', {'fields': ('role', 'manager', 'leave_balance')}),
	)
	fieldsets = UserAdmin.fieldsets + (
		('Leave management', {'fields': ('role', 'manager', 'leave_balance')}),
	)
	list_display = ['username', 'email', 'role', 'manager', 'leave_balance']
	list_filter = ['role']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
	list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status']
	list_filter = ['status', 'leave_type', 'start_date']
	search_fields = ['employee__username', 'reason']
	readonly_fields = ['created_at']
