import model
from view import App, LoginPage, JobsPage, ApplicationPage
from tkinter import messagebox

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_user = None

    def start(self):
        self.view.show_frame(LoginPage)

    def login(self, email):
        if not self.model.validate_email(email):
            messagebox.showerror('Invalid Email', 'Please enter a valid email format.')
            return

        candidate = self.model.get_candidate_by_email(email)
        if candidate:
            self.current_user = dict(candidate)
            self.view.show_frame(JobsPage)
        else:
            messagebox.showerror('Login Failed', 'No candidate found with that email.')

    def logout(self):
        self.current_user = None
        self.view.show_frame(LoginPage)
    
    def get_open_jobs_data(self):
        return self.model.get_open_jobs()

    def get_current_user_name(self):
        if self.current_user:
            return f"{self.current_user['first_name']} {self.current_user['last_name']}"
        return 'Guest'

    def show_jobs_page(self):
        self.view.show_frame(JobsPage)

    def show_application_page(self, job_id):
        job_data = self.model.get_job_by_id(job_id)
        if job_data:
            full_job_data = dict(job_data)
            
            conn = model.sqlite3.connect(model.DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT company_name FROM Companies WHERE company_id = ?', (full_job_data['company_id'],))
            company = cursor.fetchone()
            conn.close()
            full_job_data['company_name'] = company[0] if company else 'N/A'

            self.view.frames[ApplicationPage].display_job_details(full_job_data)
            self.view.show_frame(ApplicationPage)

    def confirm_application(self, job_id):
        job = self.model.get_job_by_id(job_id)
        if not job:
            messagebox.showerror('Error', 'Job not found.')
            self.view.show_frame(JobsPage)
            return
            
        candidate_status = self.current_user['status']
        job_type = job['job_type']

        if self.model.is_candidate_eligible(candidate_status, job_type):
            try:
                self.model.create_application(job['job_id'], self.current_user['candidate_id'])
                messagebox.showinfo('Success', f"You have successfully applied for {job['job_title']}!")
            except Exception as e:
                messagebox.showerror('Database Error', f'Could not save application: {e}')
        else:
            if job_type == 'สหกิจศึกษา':
                reason = 'This is a co-op position for current students only.'
            else:
                reason = 'This is a full-time position for graduates only.'
            messagebox.showerror('Application Failed', f'You are not eligible for this position.\nReason: {reason}')
        
        self.view.show_frame(JobsPage)