import sqlite3
import tkinter as tk
from tkinter import messagebox

class JobPortalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Listings Portal")
        self.root.geometry("600x400")
        self.root.attributes('-fullscreen', True) 

        self.styles = {
            "bg_color": "#f0f0f0",
            "primary_color": "#007bff",
            "text_color": "#333333",
            "font_title": ("Arial", 20),
            "font_label": ("Arial", 12),
            "font_button": ("Arial", 10, "bold")
        }
        
        self.root.configure(bg=self.styles["bg_color"])        
        self.create_tables()
        self.create_admin_user() 
        
        tk.Button(self.root, text="Logout", font=self.styles["font_button"], bg="red", fg="white", command=self.logout).pack(pady=10)
        
        self.login_page()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not getattr(self, 'fullscreen', False)  # Toggle fullscreen state
        self.root.attributes('-fullscreen', self.fullscreen)


    def create_tables(self):
        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user' 
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            company TEXT NOT NULL,
            salary REAL NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    def login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Login Page")

        tk.Label(self.root, text="Login", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        tk.Label(self.root, text="Username:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        self.root.attributes('-fullscreen', True)

        tk.Button(self.root, text="Login", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.register_page).pack()

        tk.Button(self.root, text="Exit App", command=self.exit_app, font=("Arial", 14), fg="red").pack(pady=10)


    def register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Register Page")

        tk.Label(self.root, text="Register", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        tk.Label(self.root, text="Username:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.reg_username_entry = tk.Entry(self.root)
        self.reg_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.register_user).pack(pady=10)
        tk.Button(self.root, text="Back to Login", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.login_page).pack()

        tk.Button(self.root, text="Exit App", command=self.exit_app, font=("Arial", 14), fg="red").pack(pady=10)



    def dashboard_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Dashboard")
        self.root.attributes('-fullscreen', True)  # Make the window full screen

        tk.Label(self.root, text="Job Listings", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        tk.Button(self.root, text="Add Job", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.add_job_page).pack(pady=10)
        tk.Button(self.root, text="View Jobs", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.view_jobs_page).pack(pady=10)
    
    
        tk.Button(self.root, text="User Job Listings", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.user_job_listing_page).pack(pady=10)
    
        tk.Button(self.root, text="Logout", font=self.styles["font_button"], bg="red", fg="white", command=self.logout).pack(pady=10)


    def create_admin_user(self):
        username = "admin"
        password = "admin123"  
        role = "admin"

        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Admin user already exists.")
        finally:
            conn.close()

 
    def user_job_listing_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("User Job Listings")
        tk.Label(self.root, text="Available Job Listings", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        table_frame = tk.Frame(self.root, bg=self.styles["bg_color"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        headers = ["Title", "Description", "Company", "Salary", "Apply"]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=self.styles["font_label"], bg=self.styles["primary_color"], fg="white", width=20).grid(row=0, column=col, padx=5, pady=5)

        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        c.execute("SELECT id, title, description, company, salary FROM jobs")
        jobs = c.fetchall()
        conn.close()

        for row_num, job in enumerate(jobs, start=1):
            job_id, title, description, company, salary = job

            tk.Label(table_frame, text=title, font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=0, padx=5, pady=5)
            tk.Label(table_frame, text=description, font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=1, padx=5, pady=5)
            tk.Label(table_frame, text=company, font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=2, padx=5, pady=5)
            tk.Label(table_frame, text=f"₹{salary:,.2f}", font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=3, padx=5, pady=5)  # Displaying formatted salary

            tk.Button(table_frame, text="Apply", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white",
                  command=lambda title=title: self.apply_job_page(title)).grid(row=row_num, column=4, padx=5, pady=5)

        tk.Button(self.root, text="Back to Dashboard", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.dashboard_page).pack(pady=10)

 
    def apply_for_job(self, job_id):
        messagebox.showinfo("Job Application", f"You have applied for job ID: {job_id}.")

 
    def apply_job_page(self, job_title):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Apply for Job")

        tk.Label(self.root, text="Apply for Job", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        tk.Label(self.root, text="Job Title: " + job_title, font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)

        tk.Label(self.root, text="Full Name:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.full_name_entry = tk.Entry(self.root)
        self.full_name_entry.pack(pady=5)

        tk.Label(self.root, text="Mobile Number:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.mobile_number_entry = tk.Entry(self.root)
        self.mobile_number_entry.pack(pady=5)

        tk.Label(self.root, text="Email ID:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Address:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.pack(pady=5)

        tk.Button(self.root, text="Submit Application", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.submit_application).pack(pady=10)
        tk.Button(self.root, text="Back to Job Listings", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.user_job_listing_page).pack()

 
    def submit_application(self):
        full_name = self.full_name_entry.get()
        mobile_number = self.mobile_number_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if full_name and mobile_number and email and address:
            messagebox.showinfo("Application Submitted", "Your application has been submitted successfully!")
            self.user_job_listing_page()  
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")




    def logout(self):
        messagebox.showinfo("Logout", "You have been logged out.")
        self.login_page()  
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            role = user[0]  
            if role == "admin":
                messagebox.showinfo("Login Success", "Welcome to the Admin Dashboard!")
                self.view_jobs_page()  
            else:
                messagebox.showinfo("Login Success", "Welcome to the User Job Listings!")
                self.user_job_listing_page()  
        else:
            messagebox.showerror("Login Error", "Invalid credentials. Please try again.")

 
    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if username and password:
            conn = sqlite3.connect('job_portal.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')", (username, password))
                conn.commit()
                messagebox.showinfo("Registration Success", "User registered successfully!")
                self.login_page()
            except sqlite3.IntegrityError:
                messagebox.showerror("Registration Error", "Username already exists.")
            finally:
                conn.close()
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")

 
    def add_job_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Add Job")

        tk.Label(self.root, text="Add New Job", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        tk.Label(self.root, text="Job Title:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.job_title_entry = tk.Entry(self.root)
        self.job_title_entry.pack(pady=5)

        tk.Label(self.root, text="Description:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.job_description_entry = tk.Entry(self.root)
        self.job_description_entry.pack(pady=5)

        tk.Label(self.root, text="Company:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.job_company_entry = tk.Entry(self.root)
        self.job_company_entry.pack(pady=5)

        tk.Label(self.root, text="Salary:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
        self.job_salary_entry = tk.Entry(self.root)
        self.job_salary_entry.pack(pady=5)

        tk.Button(self.root, text="Add Job", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.add_job).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.dashboard_page).pack()

 
 
    def add_job(self):
        title = self.job_title_entry.get()
        description = self.job_description_entry.get()
        company = self.job_company_entry.get()
        salary = self.job_salary_entry.get()

        if title and description and company and salary:
            try:
                salary = float(salary) 
                conn = sqlite3.connect('job_portal.db')
                c = conn.cursor()
                c.execute("INSERT INTO jobs (title, description, company, salary) VALUES (?, ?, ?, ?)", (title, description, company, salary))
                conn.commit()
                messagebox.showinfo("Job Added", "Job has been added successfully!")
                self.dashboard_page()
            except ValueError:
                messagebox.showerror("Input Error", "Salary must be a number.")
            finally:
                conn.close()
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")

 
    def view_jobs_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("View Jobs")

        tk.Label(self.root, text="Job Listings", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

        table_frame = tk.Frame(self.root, bg=self.styles["bg_color"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        headers = ["Title", "Description", "Company", "Salary", "Actions"]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=self.styles["font_label"], bg=self.styles["primary_color"], fg="white", width=20).grid(row=0, column=col, padx=5, pady=5)

        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        c.execute("SELECT id, title, description, company, salary FROM jobs")
        jobs = c.fetchall()
        conn.close()

        for row_num, job in enumerate(jobs, start=1):
            job_id, title, description, company, salary = job
        
            tk.Label(table_frame, text=title, font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=0, padx=5, pady=5)
            tk.Label(table_frame, text=description, font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=1, padx=5, pady=5)
            tk.Label(table_frame, text=company, font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=2, padx=5, pady=5)
            tk.Label(table_frame, text=f"₹ {salary:,.2f}", font=self.styles["font_label"], bg=self.styles["bg_color"], width=20, anchor="w").grid(row=row_num, column=3, padx=5, pady=5)  # Displaying formatted salary
        
            tk.Button(table_frame, text="Update", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=lambda job_id=job_id: self.update_job_page(job_id)).grid(row=row_num, column=4, padx=5, pady=5)
            tk.Button(table_frame, text="Delete", font=self.styles["font_button"], bg="red", fg="white", command=lambda job_id=job_id: self.delete_job(job_id)).grid(row=row_num, column=5, padx=5, pady=5)

        tk.Button(self.root, text="Back to Dashboard", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.dashboard_page).pack(pady=10)

 
    def update_job_page(self, job_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Update Job")

        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        c.execute("SELECT title, description, company, salary FROM jobs WHERE id=?", (job_id,))
        job = c.fetchone()
        conn.close()

        if job:
            title, description, company, salary = job

            tk.Label(self.root, text="Update Job", font=self.styles["font_title"], fg=self.styles["primary_color"], bg=self.styles["bg_color"]).pack(pady=10)

            tk.Label(self.root, text="Job Title:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
            self.update_job_title_entry = tk.Entry(self.root)
            self.update_job_title_entry.insert(0, title)  # Pre-fill with current title
            self.update_job_title_entry.pack(pady=5)

            tk.Label(self.root, text="Description:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
            self.update_job_description_entry = tk.Entry(self.root)
            self.update_job_description_entry.insert(0, description)  # Pre-fill with current description
            self.update_job_description_entry.pack(pady=5)

            tk.Label(self.root, text="Company:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
            self.update_job_company_entry = tk.Entry(self.root)
            self.update_job_company_entry.insert(0, company)  # Pre-fill with current company
            self.update_job_company_entry.pack(pady=5)

            tk.Label(self.root, text="Salary:", font=self.styles["font_label"], bg=self.styles["bg_color"]).pack(pady=5)
            self.update_job_salary_entry = tk.Entry(self.root)
            self.update_job_salary_entry.insert(0, salary)  # Pre-fill with current salary
            self.update_job_salary_entry.pack(pady=5)

            tk.Button(self.root, text="Update Job", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=lambda: self.update_job(job_id)).pack(pady=10)
            tk.Button(self.root, text="Back to View Jobs", font=self.styles["font_button"], bg=self.styles["primary_color"], fg="white", command=self.view_jobs_page).pack()
        else:
            messagebox.showerror("Error", "Job not found.")

    def update_job(self, job_id):
        title = self.update_job_title_entry.get()
        description = self.update_job_description_entry.get()
        company = self.update_job_company_entry.get()
        salary = self.update_job_salary_entry.get()

        if title and description and company and salary:
            try:
                salary = float(salary)  # Convert salary to float
                conn = sqlite3.connect('job_portal.db')
                c = conn.cursor()
                c.execute("UPDATE jobs SET title=?, description=?, company=?, salary=? WHERE id=?", (title, description, company, salary, job_id))
                conn.commit()
                messagebox.showinfo("Job Updated", "Job details updated successfully!")
                self.view_jobs_page()  # Refresh job listings
            except ValueError:
                messagebox.showerror("Input Error", "Salary must be a number.")
            finally:
                conn.close()
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")



    def delete_job(self, job_id):
        conn = sqlite3.connect('job_portal.db')
        c = conn.cursor()
        c.execute("DELETE FROM jobs WHERE id=?", (job_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Delete Job", "Job deleted successfully!")
        self.view_jobs_page()  

    def exit_app(self):
        self.root.quit()  
        
if __name__ == "__main__":
    root = tk.Tk()
    app = JobPortalApp(root)
    root.mainloop()
