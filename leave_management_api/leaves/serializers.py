from rest_framework import serializers

from .models import LeaveRequest, User


class UserSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'manager', 'leave_balance']


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    days_requested = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'leave_type', 'start_date', 'end_date',
            'days_requested', 'reason', 'status', 'review_note',
            'reviewed_by', 'created_at',
        ]
        read_only_fields = ['status', 'review_note', 'reviewed_by', 'created_at']

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({'end_date': 'End date cannot be before start date.'})

        user = self.context['request'].user
        if start_date and end_date:
            days_requested = (end_date - start_date).days + 1
            pending_days = sum(
                request.days_requested
                for request in LeaveRequest.objects.filter(
                    employee=user,
                    status=LeaveRequest.Status.PENDING,
                )
            )
            if pending_days + days_requested > user.leave_balance:
                raise serializers.ValidationError({
                    'end_date': 'Requested days exceed your available leave balance.'
                })
        return attrs


class ReviewSerializer(serializers.Serializer):
    review_note = serializers.CharField(max_length=500, required=False, allow_blank=True)