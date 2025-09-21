import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    '''Main application window that manages frames.'''
    def __init__(self):
        super().__init__()
        self.title('Job Fair Application System')
        self.geometry('800x600')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.controller = None
        self.frames = {}

        for F in (LoginPage, JobsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def set_controller(self, controller):
        self.controller = controller
        for frame in self.frames.values():
            frame.set_controller(controller)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if cont == JobsPage:
            frame.refresh_data()

class LoginPage(tk.Frame):
    def __init__(self, parent, app_instance):
        super().__init__(parent)
        self.app = app_instance
        self.controller = None

        tk.Label(self, text='Login with your Email', font=('Helvetica', 16)).pack(pady=20)
        
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.pack(pady=10)
        
        login_button = tk.Button(self, text='Login', command=self.login)
        login_button.pack(pady=10)

    def set_controller(self, controller):
        self.controller = controller

    def login(self):
        email = self.email_entry.get()
        if self.controller:
            self.controller.login(email)

class JobsPage(tk.Frame):
    def __init__(self, parent, app_instance):
        super().__init__(parent)
        self.app = app_instance
        self.controller = None

        top_frame = tk.Frame(self)
        top_frame.pack(fill='x', pady=5)
        self.welcome_label = tk.Label(top_frame, text='', font=('Helvetica', 12))
        self.welcome_label.pack(side='left', padx=10)
        logout_button = tk.Button(top_frame, text='Logout', command=self.logout)
        logout_button.pack(side='right', padx=10)

        columns = ('job_id', 'title', 'company', 'type', 'deadline')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        self.tree.heading('job_id', text='ID')
        self.tree.heading('title', text='Job Title')
        self.tree.heading('company', text='Company')
        self.tree.heading('type', text='Type')
        self.tree.heading('deadline', text='Deadline')

        self.tree.column('job_id', width=80)
        self.tree.column('title', width=200)
        self.tree.column('company', width=150)
        self.tree.column('type', width=100)
        self.tree.column('deadline', width=100)

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        apply_button = tk.Button(self, text='Apply for Selected Job', command=self.apply_for_job)
        apply_button.pack(pady=10)

    def set_controller(self, controller):
        self.controller = controller

    def refresh_data(self):
        '''Called by controller to update the jobs list and welcome message.'''
        if not self.controller: return

        user_name = self.controller.get_current_user_name()
        self.welcome_label.config(text=f'Welcome, {user_name}!')
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        jobs = self.controller.get_open_jobs_data()
        for job in jobs:
            self.tree.insert('', 'end', values=job)

    def apply_for_job(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning('No Selection', 'Please select a job from the list to apply.')
            return
            
        job_id = self.tree.item(selected_item)['values'][0]
        if self.controller:
            self.controller.apply_for_job(job_id)

    def logout(self):
        if self.controller:
            self.controller.logout()