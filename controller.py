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
            
        success = False
        message = 'An unexpected error occurred.'
        new_app_id = None

        try:
            if job['job_type'] == 'สหกิจศึกษา':
                success, message, new_app_id = self.model.apply_for_coop_job(job['job_id'], self.current_user)
            elif job['job_type'] == 'งานปกติ':
                success, message, new_app_id = self.model.apply_for_regular_job(job['job_id'], self.current_user)
            
            if success and new_app_id is not None:
                details = self.model.get_application_details(new_app_id)
                success_message = (
                    'Application Submitted!\n\n'
                    f"Job Title: {details['job_title']}\n"
                    f"Company: {details['company_name']}\n"
                    f"Date Submitted: {details['application_date']}"
                )
                messagebox.showinfo('Success', success_message)
            else:
                messagebox.showerror('Application Failed', f'You are not eligible for this position.\nReason: {message}')

        except Exception as e:
            messagebox.showerror('Database Error', f'Could not save application: {e}')
        
        self.view.show_frame(JobsPage)