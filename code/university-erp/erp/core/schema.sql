-- ERP core schema. Modules add their own tables in erp/modules/<name>/schema.sql, prefixed with the module name.
CREATE TABLE IF NOT EXISTS faculties (code TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS departments (code TEXT PRIMARY KEY, name TEXT NOT NULL,
  faculty_code TEXT NOT NULL REFERENCES faculties(code));
CREATE TABLE IF NOT EXISTS programmes (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE,
  department_code TEXT NOT NULL REFERENCES departments(code));
CREATE TABLE IF NOT EXISTS courses (code TEXT PRIMARY KEY, title TEXT NOT NULL, units INTEGER NOT NULL CHECK (units BETWEEN 1 AND 6),
  level INTEGER NOT NULL, semester TEXT NOT NULL, department_code TEXT NOT NULL REFERENCES departments(code));
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, full_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS user_roles (user_id INTEGER NOT NULL REFERENCES users(id), role TEXT NOT NULL,
  scope TEXT NOT NULL DEFAULT '*', PRIMARY KEY (user_id, role, scope));
CREATE TABLE IF NOT EXISTS students (matric_no TEXT PRIMARY KEY, user_id INTEGER UNIQUE REFERENCES users(id),
  programme_id INTEGER NOT NULL REFERENCES programmes(id), level INTEGER NOT NULL, entry_session TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active');
CREATE TABLE IF NOT EXISTS staff (staff_no TEXT PRIMARY KEY, user_id INTEGER UNIQUE REFERENCES users(id),
  department_code TEXT REFERENCES departments(code), category TEXT NOT NULL CHECK (category IN ('academic','non-academic')),
  rank TEXT NOT NULL);
-- Append-only, hash-chained: each row's hash covers the previous row's hash, so editing history is detectable.
CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY, at TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL,
  entity TEXT NOT NULL, details TEXT NOT NULL, prev_hash TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit_log BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit_log BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
