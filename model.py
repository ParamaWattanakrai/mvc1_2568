import sqlite3
import re
from datetime import datetime

DB_PATH = 'database/job_fair.db'

def get_open_jobs():
    '''Fetches all jobs with 'เปิด' status, joining with company info.'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT j.job_id, j.job_title, c.company_name, j.job_type, j.deadline
        FROM Jobs j
        JOIN Companies c ON j.company_id = c.company_id
        WHERE j.status = 'เปิด'
    ''')
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_candidate_by_email(email):
    '''Retrieves candidate data for login.'''
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Candidate WHERE email = ?', (email,))
    candidate = cursor.fetchone()
    conn.close()
    return candidate

def get_job_by_id(job_id):
    '''Retrieves a single job's data.'''
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Jobs WHERE job_id = ?', (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job

def validate_email(email):
    '''Simple email format validation.'''
    if re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return True
    return False

def is_candidate_eligible(candidate_status, job_type):
    '''
    Checks if a candidate is eligible for a job based on their status.
    - Co-op jobs are only for 'กำลังศึกษา' candidates.
    - Regular jobs are only for 'จบแล้ว' candidates.
    '''
    if job_type == 'สหกิจศึกษา' and candidate_status == 'กำลังศึกษา':
        return True
    if job_type == 'งานปกติ' and candidate_status == 'จบแล้ว':
        return True
    return False

def create_application(job_id, candidate_id):
    '''Saves a new application record to the database with the current timestamp.'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(
        'INSERT INTO Application (job_id, candidate_id, application_date) VALUES (?, ?, ?)',
        (job_id, candidate_id, current_time)
    )
    conn.commit()
    conn.close()