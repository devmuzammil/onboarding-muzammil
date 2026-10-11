from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from .models import LeaveRequest, User


class LeaveRequestAPITests(APITestCase):
	def setUp(self):
		self.manager = User.objects.create_user(
			username='manager',
			password='test-password',
			role=User.Role.MANAGER,
		)
		self.employee = User.objects.create_user(
			username='employee',
			password='test-password',
			manager=self.manager,
			leave_balance=5,
		)
		self.request_data = {
			'leave_type': 'annual',
			'start_date': '2026-11-02',
			'end_date': '2026-11-03',
			'reason': 'Family event',
		}

	def test_employee_applies_for_leave(self):
		self.client.force_authenticate(self.employee)

		response = self.client.post('/api/leave-requests/', self.request_data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['days_requested'], 2)
		self.assertEqual(self.employee.leave_balance, 5)

	def test_employee_cannot_apply_over_balance(self):
		self.client.force_authenticate(self.employee)
		self.request_data['end_date'] = '2026-11-08'

		response = self.client.post('/api/leave-requests/', self.request_data)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(LeaveRequest.objects.count(), 0)

	def test_pending_requests_cannot_exceed_balance(self):
		LeaveRequest.objects.create(
			employee=self.employee,
			leave_type='annual',
			start_date=date(2026, 11, 2),
			end_date=date(2026, 11, 5),
			reason='Existing request',
		)
		self.client.force_authenticate(self.employee)

		response = self.client.post('/api/leave-requests/', self.request_data)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(LeaveRequest.objects.count(), 1)

	def test_manager_approval_deducts_balance_once(self):
		leave_request = LeaveRequest.objects.create(
			employee=self.employee,
			leave_type='annual',
			start_date=date(2026, 11, 2),
			end_date=date(2026, 11, 3),
			reason='Family event',
		)
		self.client.force_authenticate(self.manager)

		response = self.client.post(f'/api/leave-requests/{leave_request.id}/approve/')
		repeated_response = self.client.post(f'/api/leave-requests/{leave_request.id}/approve/')

		self.employee.refresh_from_db()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(repeated_response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(self.employee.leave_balance, 3)

	def test_rejection_does_not_deduct_balance(self):
		leave_request = LeaveRequest.objects.create(
			employee=self.employee,
			leave_type='sick',
			start_date=date(2026, 11, 2),
			end_date=date(2026, 11, 3),
			reason='Not feeling well',
		)
		self.client.force_authenticate(self.manager)

		response = self.client.post(f'/api/leave-requests/{leave_request.id}/reject/')

		self.employee.refresh_from_db()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(self.employee.leave_balance, 5)

	def test_employee_cannot_review_leave(self):
		leave_request = LeaveRequest.objects.create(
			employee=self.employee,
			leave_type='annual',
			start_date=date(2026, 11, 2),
			end_date=date(2026, 11, 3),
			reason='Family event',
		)
		self.client.force_authenticate(self.employee)

		response = self.client.post(f'/api/leave-requests/{leave_request.id}/approve/')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_manager_cannot_review_another_managers_request(self):
		other_manager = User.objects.create_user(
			username='other-manager',
			password='test-password',
			role=User.Role.MANAGER,
		)
		other_employee = User.objects.create_user(
			username='other-employee',
			password='test-password',
			role=User.Role.EMPLOYEE,
			manager=other_manager,
		)
		leave_request = LeaveRequest.objects.create(
			employee=other_employee,
			leave_type='annual',
			start_date=date(2026, 11, 2),
			end_date=date(2026, 11, 3),
			reason='Family event',
		)
		self.client.force_authenticate(self.manager)

		response = self.client.post(f'/api/leave-requests/{leave_request.id}/approve/')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_employee_can_get_jwt_tokens(self):
		response = self.client.post('/api/token/', {
			'username': 'employee',
			'password': 'test-password',
		})

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)

	def test_status_and_date_filters(self):
		LeaveRequest.objects.create(
			employee=self.employee,
			leave_type='annual',
			start_date=date(2026, 11, 2),
			end_date=date(2026, 11, 3),
			reason='Family event',
		)
		self.client.force_authenticate(self.manager)

		response = self.client.get(
			'/api/leave-requests/?status=pending&from_date=2026-11-03&to_date=2026-11-04'
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
