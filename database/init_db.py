import sqlite3
import os

if not os.path.exists('database'):
    os.makedirs('database')

DB_PATH = 'database/job_fair.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Companies')
cursor.execute('DROP TABLE IF EXISTS Jobs')
cursor.execute('DROP TABLE IF EXISTS Candidate')
cursor.execute('DROP TABLE IF EXISTS Application')

cursor.execute('''
CREATE TABLE Companies (
    company_id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    location TEXT,
    CONSTRAINT check_company_id CHECK (
        LENGTH(company_id) = 8 AND SUBSTR(company_id, 1, 1) != '0'
    )
)''')

cursor.execute('''
CREATE TABLE Jobs (
    job_id TEXT PRIMARY KEY,
    job_title TEXT NOT NULL,
    job_description TEXT,
    company_id TEXT,
    deadline TEXT,
    status TEXT NOT NULL,
    job_type TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies (company_id),
    CONSTRAINT check_job_id CHECK (
        LENGTH(job_id) = 8 AND SUBSTR(job_id, 1, 1) != '0'
    ),
    CONSTRAINT check_job_status CHECK (status IN ('เปิด', 'ปิด')),
    CONSTRAINT check_job_type CHECK (job_type IN ('งานปกติ', 'สหกิจศึกษา'))
)''')

cursor.execute('''
CREATE TABLE Candidate (
    candidate_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    CONSTRAINT check_candidate_id CHECK (
        LENGTH(candidate_id) = 8 AND SUBSTR(candidate_id, 1, 1) != '0'
    ),
    CONSTRAINT check_candidate_status CHECK (status IN ('กำลังศึกษา', 'จบแล้ว'))
)''')

cursor.execute('''
CREATE TABLE Application (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    application_date TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES Jobs (job_id),
    FOREIGN KEY (candidate_id) REFERENCES Candidate (candidate_id)
)''')

companies_data = [
    ('11110001', 'Innovatech Solutions', 'hr@innovatech.com', 'Bangkok'),
    ('22220002', 'Cyberdyne Systems', 'careers@cyberdyne.com', 'Pathum Thani')
]
cursor.executemany('INSERT INTO Companies VALUES (?, ?, ?, ?)', companies_data)

jobs_data = [
    ('10000001', 'Junior Python Developer', 'Develop web apps.', '11110001', '2025-10-31', 'เปิด', 'งานปกติ'),
    ('10000002', 'Data Science Intern', 'Analyze datasets.', '11110001', '2025-10-15', 'เปิด', 'สหกิจศึกษา'),
    ('10000003', 'Frontend Developer', 'Create UI/UX.', '11110001', '2025-11-10', 'เปิด', 'งานปกติ'),
    ('10000004', 'Cloud Engineer', 'Manage AWS/Azure.', '11110001', '2025-11-20', 'ปิด', 'งานปกติ'),
    ('10000005', 'QA Tester Intern', 'Test new software.', '11110001', '2025-09-30', 'เปิด', 'สหกิจศึกษา'),
    ('20000001', 'AI Research Scientist', 'Build AI models.', '22220002', '2025-12-01', 'เปิด', 'งานปกติ'),
    ('20000002', 'Robotics Engineer', 'Design and build robots.', '22220002', '2025-11-30', 'เปิด', 'งานปกติ'),
    ('20000003', 'Backend Developer (Go)', 'Develop microservices.', '22220002', '2025-10-25', 'ปิด', 'งานปกติ'),
    ('20000004', 'Machine Learning Intern', 'Train ML models.', '22220002', '2025-10-05', 'เปิด', 'สหกิจศึกษา'),
    ('20000005', 'Cybersecurity Analyst', 'Monitor network security.', '22220002', '2025-11-15', 'เปิด', 'งานปกติ')
]
cursor.executemany('INSERT INTO Jobs VALUES (?, ?, ?, ?, ?, ?, ?)', jobs_data)

candidates_data = [
    ('66010001', 'Somchai', 'Jaidee', 'somchai.j@example.com', 'จบแล้ว'),
    ('66010002', 'Somsri', 'Rakdee', 'somsri.r@example.com', 'จบแล้ว'),
    ('67010001', 'Apiwat', 'Boonma', 'apiwat.b@example.com', 'กำลังศึกษา'),
    ('67010002', 'Naree', 'Yindee', 'naree.y@example.com', 'กำลังศึกษา'),
    ('65010003', 'Peter', 'Parker', 'peter.p@example.com', 'จบแล้ว'),
    ('68010004', 'Wanda', 'Maximoff', 'wanda.m@example.com', 'กำลังศึกษา'),
    ('66010005', 'Tony', 'Stark', 'tony.s@example.com', 'จบแล้ว'),
    ('67010006', 'Bruce', 'Banner', 'bruce.b@example.com', 'จบแล้ว'),
    ('68010007', 'Natasha', 'Romanoff', 'natasha.r@example.com', 'กำลังศึกษา'),
    ('67010008', 'Steve', 'Rogers', 'steve.r@example.com', 'จบแล้ว')
]
cursor.executemany('INSERT INTO Candidate VALUES (?, ?, ?, ?, ?)', candidates_data)

conn.commit()
conn.close()