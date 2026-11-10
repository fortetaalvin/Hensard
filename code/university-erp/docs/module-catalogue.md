# Module catalogue

The ERP is built module by module. **Course Registration** is the class module, built together in the weekly labs.
Each team chooses **one** other module in week 3 as its capstone and owns its folder under `erp/modules/`.
Two teams may not take the same module.

| Module (folder) | Owner office | Stakeholder you interview | What it does | Publishes | Consumes |
| --- | --- | --- | --- | --- | --- |
| Course Registration (`registration`) · **class** | Registry / Academic Affairs | Deputy Registrar (Academic) | Students register courses within credit-load limits; adviser and HOD approve | `registration.approved` | `fees.cleared` |
| Admissions (`admissions`) | Admissions Office | Admissions Officer | Applicants, screening scores, offers, acceptance, matric number allocation | `student.admitted` | — |
| Fees and Bursary (`fees`) | Bursary | Bursar | Fee schedules by programme and level, invoices, payments, receipts, clearance | `fees.cleared`, `payment.received` | `student.admitted`, `registration.approved` |
| Examinations and Results (`results`) | Exams and Records | Exams Officer | Score entry, moderation, Senate approval, GPA and CGPA, result release | `result.approved` | `registration.approved` |
| Records and Transcripts (`records`) | Registry | Head of Records | Transcript, certificate and letter requests; replaces the legacy Registry app | `transcript.issued` | `result.approved`, `fees.cleared` |
| Hostels and Accommodation (`hostels`) | Student Affairs | Hall Warden | Bed spaces, allocation rules, check-in and check-out, maintenance requests | `bedspace.allocated` | `fees.cleared` |
| Staff Records and HR (`hr`) | Establishment / HR | Head of Establishment | Staff records, appointments, leave, appraisal, promotion cases | `staff.appointed`, `staff.promoted` | — |
| Payroll (`payroll`) | Bursary (Salaries) | Head of Salaries | Salary structure, monthly payroll, deductions, payslips | `payroll.run` | `staff.appointed`, `staff.promoted` |
| Library (`library`) | University Library | University Librarian | Catalogue, loans, returns, fines, library clearance | `library.cleared` | `student.admitted`, `registration.approved` |
| Timetabling and Venues (`timetable`) | Academic Planning | Timetable Officer | Lecture and exam timetables, venue capacity, clash detection | `timetable.published` | `registration.approved` |

## Rules for every module

1. Build only inside your folder: `erp/modules/<name>/`. CODEOWNERS makes your team the required reviewer for it.
2. Use `erp/core/contracts.py` for students, staff, roles, sessions and the audit log. Never query core tables directly.
3. Never import another module. Integrate through the events in `docs/integration-contracts.md`.
4. Prefix your tables with the module name in your `schema.sql`.
5. Record every consequential action (approval, payment, grade change, allocation) with `contracts.record_event`.
6. Synthetic data only. No real student or staff record ever enters the repository, a prompt or a transcript.
