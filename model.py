import sqlite3
import re
from datetime import datetime

DB_PATH = 'database/job_fair.db'

def get_open_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT j.job_id, j.job_title, c.company_name, j.job_type, j.deadline
        FROM Jobs j
        JOIN Companies c ON j.company_id = c.company_id
        WHERE j.status = 'เปิด'
        ORDER BY j.job_title ASC
    ''')
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_candidate_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Candidate WHERE email = ?', (email,))
    candidate = cursor.fetchone()
    conn.close()
    return candidate

def get_job_by_id(job_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Jobs WHERE job_id = ?', (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job

def validate_email(email):
    if re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return True
    return False

def _create_application_record(job_id, candidate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        'INSERT INTO Application (job_id, candidate_id, application_date) VALUES (?, ?, ?)',
        (job_id, candidate_id, current_time)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_application_details(app_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.application_date, j.job_title, c.company_name
        FROM Application a
        JOIN Jobs j ON a.job_id = j.job_id
        JOIN Companies c ON j.company_id = c.company_id
        WHERE a.application_id = ?
    ''', (app_id,))
    details = cursor.fetchone()
    conn.close()
    return details

def apply_for_coop_job(job_id, candidate):
    if candidate['status'] == 'กำลังศึกษา':
        new_app_id = _create_application_record(job_id, candidate['candidate_id'])
        return True, 'Application successful.', new_app_id
    else:
        return False, 'This is a co-op position for current students only.', None

def apply_for_regular_job(job_id, candidate):
    if candidate['status'] == 'จบแล้ว':
        new_app_id = _create_application_record(job_id, candidate['candidate_id'])
        return True, 'Application successful.', new_app_id
    else:
        return False, 'This is a full-time position for graduates only.', None