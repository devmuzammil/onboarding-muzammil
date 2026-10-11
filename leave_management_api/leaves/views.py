from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .models import LeaveRequest, User
from .serializers import LeaveRequestSerializer, ReviewSerializer, UserSerializer


class LeaveRequestFilter(filters.FilterSet):
	from_date = filters.DateFilter(field_name='end_date', lookup_expr='gte')
	to_date = filters.DateFilter(field_name='start_date', lookup_expr='lte')

	class Meta:
		model = LeaveRequest
		fields = ['status']


class CurrentUserView(generics.RetrieveAPIView):
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class LeaveRequestViewSet(viewsets.ModelViewSet):
	serializer_class = LeaveRequestSerializer
	filterset_class = LeaveRequestFilter
	http_method_names = ['get', 'post', 'head', 'options']

	def get_queryset(self):
		user = self.request.user
		requests = LeaveRequest.objects.select_related('employee', 'reviewed_by')
		if user.role == User.Role.MANAGER:
			return requests.filter(employee__manager=user)
		return requests.filter(employee=user)

	def perform_create(self, serializer):
		if self.request.user.role != User.Role.EMPLOYEE:
			raise PermissionDenied('Only employees can apply for leave.')
		serializer.save(employee=self.request.user)

	def _review(self, request, pk, new_status):
		if request.user.role != User.Role.MANAGER:
			raise PermissionDenied('Only managers can review leave requests.')

		review_serializer = ReviewSerializer(data=request.data)
		review_serializer.is_valid(raise_exception=True)

		with transaction.atomic():
			leave_request = get_object_or_404(
				self.get_queryset().select_for_update(),
				pk=pk,
			)
			if leave_request.status != LeaveRequest.Status.PENDING:
				raise ValidationError('This leave request has already been reviewed.')

			if new_status == LeaveRequest.Status.APPROVED:
				employee = User.objects.select_for_update().get(pk=leave_request.employee_id)
				if leave_request.days_requested > employee.leave_balance:
					raise ValidationError('The employee no longer has enough leave balance.')
				employee.leave_balance -= leave_request.days_requested
				employee.save(update_fields=['leave_balance'])

			leave_request.status = new_status
			leave_request.reviewed_by = request.user
			leave_request.review_note = review_serializer.validated_data.get('review_note', '')
			leave_request.save(update_fields=['status', 'reviewed_by', 'review_note'])

		return Response(self.get_serializer(leave_request).data, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'])
	def approve(self, request, pk=None):
		return self._review(request, pk, LeaveRequest.Status.APPROVED)

	@action(detail=True, methods=['post'])
	def reject(self, request, pk=None):
		return self._review(request, pk, LeaveRequest.Status.REJECTED)
