# Integration contracts

Modules integrate through events on the core bus (`erp/core/events.py`), never by importing each other.
This file is the contract. Adding or changing an event needs a PR reviewed by every team that publishes or consumes it.

| Event | Published by | Payload (all keys required) | Consumed by |
| --- | --- | --- | --- |
| `student.admitted` | admissions | `matric_no`, `programme`, `level`, `session` | fees, library |
| `registration.approved` | registration | `matric_no`, `session`, `semester`, `courses` (list of codes), `total_units` | fees, results, library, timetable |
| `fees.cleared` | fees | `matric_no`, `session`, `cleared_at` | registration, records, hostels |
| `payment.received` | fees | `matric_no`, `amount_kobo`, `reference`, `channel` | — |
| `result.approved` | results | `session`, `semester`, `programme`, `approved_by`, `senate_date` | records |
| `transcript.issued` | records | `matric_no`, `request_ref` | — |
| `bedspace.allocated` | hostels | `matric_no`, `hall`, `room`, `session` | — |
| `staff.appointed` | hr | `staff_no`, `rank`, `department_code`, `effective` | payroll |
| `staff.promoted` | hr | `staff_no`, `from_rank`, `to_rank`, `effective` | payroll |
| `payroll.run` | payroll | `period`, `staff_count`, `total_kobo` | — |
| `library.cleared` | library | `matric_no`, `cleared_at` | records |
| `timetable.published` | timetable | `session`, `semester`, `kind` (`lecture` or `exam`) | — |

## Conventions

- Money is an integer number of **kobo**. Never a float.
- Times are ISO 8601 strings in UTC. Display in the institution's time zone.
- A handler must be idempotent: the same event may arrive twice.
- A handler that fails logs and returns; it must not raise into the publisher.
- Every handler that changes data also records an audit event.
