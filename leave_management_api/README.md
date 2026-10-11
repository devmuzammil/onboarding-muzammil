# Leave Management API

A small Django REST Framework API for employee leave requests and manager decisions. PostgreSQL is the configured database. Leave duration is counted in inclusive calendar days, including weekends.

## Setup

From this folder in PowerShell:

```powershell
Copy-Item env.example .env
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Edit `.env` with your PostgreSQL username and password, then create the database named in `DB_NAME`:

```powershell
createdb -U postgres leave_management
..\.venv\Scripts\python.exe manage.py makemigrations leaves
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py test leaves
..\.venv\Scripts\python.exe manage.py createsuperuser
..\.venv\Scripts\python.exe manage.py runserver
```

In Django admin, create manager accounts with the `manager` role, then create employee accounts and select their manager. New employees start with 20 leave days; the admin can change this balance.

## Endpoints

All API endpoints require a JWT access token except the token endpoints.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/token/` | Get access and refresh tokens with username and password |
| `POST` | `/api/token/refresh/` | Get a new access token |
| `GET` | `/api/me/` | View the signed-in user's role, manager, and balance |
| `GET` | `/api/leave-requests/` | Employees see their requests; managers see their team's requests |
| `POST` | `/api/leave-requests/` | Employee applies for leave |
| `POST` | `/api/leave-requests/{id}/approve/` | Manager approves a pending team request |
| `POST` | `/api/leave-requests/{id}/reject/` | Manager rejects a pending team request |

Filter the request list with `?status=pending`, `?from_date=2026-11-01`, and `?to_date=2026-11-30`. Date filters include requests that overlap the selected range.

An application body looks like:

```json
{
  "leave_type": "annual",
  "start_date": "2026-11-02",
  "end_date": "2026-11-03",
  "reason": "Family event"
}
```

The approval endpoint deducts the requested days inside a database transaction. Requests are checked against the employee's balance both when submitted and when approved.

## Suggested Team Issues

Create these as separate GitHub issues and assign one to each teammate:

1. Add employee and manager roles, team relationships, leave balance, and Django admin setup.
2. Build the employee leave application endpoint and validate dates and available balance.
3. Build manager team-request listing and approve/reject actions with transactional balance updates.
4. Configure JWT authentication and status/date filters.
5. Add API tests and verify the complete workflow against PostgreSQL.

Use one branch and pull request per issue; review and merge each pull request before the team considers the issue done.