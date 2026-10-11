from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	class Role(models.TextChoices):
		EMPLOYEE = 'employee', 'Employee'
		MANAGER = 'manager', 'Manager'

	role = models.CharField(
		max_length=10,
		choices=Role.choices,
		default=Role.EMPLOYEE,
	)
	manager = models.ForeignKey(
		'self',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='team_members',
	)
	leave_balance = models.PositiveIntegerField(default=20)

	def __str__(self):
		return self.username


class LeaveRequest(models.Model):
	class LeaveType(models.TextChoices):
		ANNUAL = 'annual', 'Annual'
		SICK = 'sick', 'Sick'
		PERSONAL = 'personal', 'Personal'

	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		APPROVED = 'approved', 'Approved'
		REJECTED = 'rejected', 'Rejected'

	employee = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='leave_requests',
	)
	leave_type = models.CharField(max_length=10, choices=LeaveType.choices)
	start_date = models.DateField()
	end_date = models.DateField()
	reason = models.TextField()
	status = models.CharField(
		max_length=10,
		choices=Status.choices,
		default=Status.PENDING,
	)
	review_note = models.CharField(max_length=500, blank=True)
	reviewed_by = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='reviewed_leave_requests',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	@property
	def days_requested(self):
		return (self.end_date - self.start_date).days + 1

	def __str__(self):
		return f'{self.employee.username}: {self.start_date} to {self.end_date}'

	class Meta:
		ordering = ['-created_at']
