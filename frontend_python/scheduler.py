# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# import requests
# import json

# class OrderSchedulerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Order Scheduler")
#         self.root.geometry("800x600")
#         self.root.resizable(False, False)
        
#         # API Base URL
#         self.base_url = "http://localhost:3000"
#         self.token = None
#         self.user_email = None
        
#         # Configure styles
#         self.setup_styles()
        
#         # Main container
#         self.main_container = tk.Frame(root, bg="#f0f0f0")
#         self.main_container.pack(fill=tk.BOTH, expand=True)
        
#         # Show login page initially
#         self.show_login_page()
    
#     def setup_styles(self):
#         style = ttk.Style()
#         style.theme_use('clam')
        
#         # Configure button style
#         style.configure('TButton', padding=6, relief="flat", background="#4CAF50", foreground="white")
#         style.map('TButton', background=[('active', '#45a049')])
        
#         # Configure entry style
#         style.configure('TEntry', padding=5, relief="solid")
        
#     def clear_container(self):
#         """Clear all widgets from main container"""
#         for widget in self.main_container.winfo_children():
#             widget.destroy()
    
#     def show_login_page(self):
#         """Display login/signup page"""
#         self.clear_container()
        
#         # Center frame
#         frame = tk.Frame(self.main_container, bg="#f0f0f0")
#         frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
#         # Title
#         title = tk.Label(frame, text="Order Scheduler", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
#         title.grid(row=0, column=0, columnspan=2, pady=20)
        
#         # Email
#         tk.Label(frame, text="Email:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
#         self.email_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
#         self.email_entry.grid(row=1, column=1, pady=5, padx=10)
        
#         # Password
#         tk.Label(frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
#         self.password_entry = ttk.Entry(frame, width=30, show="*", font=("Arial", 11))
#         self.password_entry.grid(row=2, column=1, pady=5, padx=10)
        
#         # Buttons frame
#         btn_frame = tk.Frame(frame, bg="#f0f0f0")
#         btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
#         login_btn = tk.Button(btn_frame, text="Login", command=self.login, 
#                              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
#                              padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
#         login_btn.pack(side=tk.LEFT, padx=5)
        
#         signup_btn = tk.Button(btn_frame, text="Sign Up", command=self.signup,
#                               bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
#                               padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
#         signup_btn.pack(side=tk.LEFT, padx=5)
    
#     def login(self):
#         """Handle user login"""
#         email = self.email_entry.get().strip()
#         password = self.password_entry.get().strip()
        
#         if not email or not password:
#             messagebox.showerror("Error", "Please enter both email and password")
#             return
        
#         try:
#             response = requests.post(f"{self.base_url}/auth/login", 
#                                     json={"email": email, "password": password})
            
#             if response.status_code == 200:
#                 data = response.json()
#                 self.token = data.get("token")
#                 self.user_email = email
#                 messagebox.showinfo("Success", "Login successful!")
#                 self.show_orders_page()
#             else:
#                 messagebox.showerror("Error", f"Login failed: {response.text}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Connection error: {str(e)}")
    
#     def signup(self):
#         """Handle user signup"""
#         email = self.email_entry.get().strip()
#         password = self.password_entry.get().strip()
        
#         if not email or not password:
#             messagebox.showerror("Error", "Please enter both email and password")
#             return
        
#         try:
#             response = requests.post(f"{self.base_url}/auth/signup",
#                                     json={"email": email, "password": password})
            
#             if response.status_code == 200 or response.status_code == 201:
#                 data = response.json()
#                 self.token = data.get("token")
#                 self.user_email = email
#                 messagebox.showinfo("Success", "Signup successful! You are now logged in.")
#                 self.show_orders_page()
#             else:
#                 messagebox.showerror("Error", f"Signup failed: {response.text}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Connection error: {str(e)}")
    
#     def show_orders_page(self):
#         """Display orders management page"""
#         self.clear_container()
        
#         # Header
#         header = tk.Frame(self.main_container, bg="#4CAF50", height=60)
#         header.pack(fill=tk.X)
        
#         tk.Label(header, text=f"Welcome, {self.user_email}", font=("Arial", 14, "bold"),
#                 bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        
#         logout_btn = tk.Button(header, text="Logout", command=self.logout,
#                               bg="#f44336", fg="white", font=("Arial", 10, "bold"),
#                               padx=15, pady=5, relief=tk.FLAT, cursor="hand2")
#         logout_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
#         # Content frame
#         content = tk.Frame(self.main_container, bg="#f0f0f0")
#         content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Left panel - Create Order
#         left_panel = tk.LabelFrame(content, text="Create New Order", font=("Arial", 12, "bold"),
#                                    bg="white", padx=15, pady=15)
#         left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
#         # Schedule Time
#         tk.Label(left_panel, text="Schedule Time:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
#         tk.Label(left_panel, text="(YYYY-MM-DD HH:MM:SS)", font=("Arial", 8), bg="white", fg="gray").grid(row=0, column=1, sticky=tk.W)
#         self.schedule_time_entry = ttk.Entry(left_panel, width=25)
#         self.schedule_time_entry.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W)
#         self.schedule_time_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
#         # Is Recurring
#         self.is_recurring_var = tk.BooleanVar()
#         recurring_check = tk.Checkbutton(left_panel, text="Recurring Order", variable=self.is_recurring_var,
#                                         font=("Arial", 10), bg="white", command=self.toggle_recurring_fields)
#         recurring_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=10)
        
#         # Recurring fields frame
#         self.recurring_frame = tk.Frame(left_panel, bg="white")
#         self.recurring_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
#         # Repeat Interval
#         tk.Label(self.recurring_frame, text="Repeat Interval:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
#         self.repeat_interval_entry = ttk.Entry(self.recurring_frame, width=10)
#         self.repeat_interval_entry.grid(row=0, column=1, pady=5, padx=5)
#         self.repeat_interval_entry.insert(0, "1")
        
#         # Repeat Unit
#         tk.Label(self.recurring_frame, text="Repeat Unit:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
#         self.repeat_unit_var = tk.StringVar(value="MINUTE")
#         repeat_unit_combo = ttk.Combobox(self.recurring_frame, textvariable=self.repeat_unit_var,
#                                          values=["MINUTE", "HOUR", "DAY", "WEEK", "MONTH"], width=10, state="readonly")
#         repeat_unit_combo.grid(row=1, column=1, pady=5, padx=5)
        
#         # Max Executions
#         tk.Label(self.recurring_frame, text="Max Executions:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
#         self.max_executions_entry = ttk.Entry(self.recurring_frame, width=10)
#         self.max_executions_entry.grid(row=2, column=1, pady=5, padx=5)
#         self.max_executions_entry.insert(0, "3")
        
#         # Initially hide recurring fields
#         self.recurring_frame.grid_remove()
        
#         # Create Order Button
#         create_btn = tk.Button(left_panel, text="Create Order", command=self.create_order,
#                               bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
#                               padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
#         create_btn.grid(row=4, column=0, columnspan=2, pady=15)
        
#         # Right panel - Orders List
#         right_panel = tk.LabelFrame(content, text="Your Orders", font=("Arial", 12, "bold"),
#                                     bg="white", padx=15, pady=15)
#         right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
#         # Refresh button
#         refresh_btn = tk.Button(right_panel, text="🔄 Refresh", command=self.load_orders,
#                                bg="#2196F3", fg="white", font=("Arial", 9),
#                                padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
#         refresh_btn.pack(anchor=tk.NE, pady=(0, 10))
        
#         # Orders listbox with scrollbar
#         list_frame = tk.Frame(right_panel, bg="white")
#         list_frame.pack(fill=tk.BOTH, expand=True)
        
#         scrollbar = tk.Scrollbar(list_frame)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
#         self.orders_listbox = tk.Listbox(list_frame, font=("Courier", 9), 
#                                          yscrollcommand=scrollbar.set, height=15)
#         self.orders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.config(command=self.orders_listbox.yview)
        
#         # Action buttons
#         action_frame = tk.Frame(right_panel, bg="white")
#         action_frame.pack(fill=tk.X, pady=10)
        
#         view_btn = tk.Button(action_frame, text="View Details", command=self.view_order_details,
#                             bg="#2196F3", fg="white", font=("Arial", 9),
#                             padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
#         view_btn.pack(side=tk.LEFT, padx=5)
        
#         update_btn = tk.Button(action_frame, text="Update", command=self.update_order,
#                               bg="#FF9800", fg="white", font=("Arial", 9),
#                               padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
#         update_btn.pack(side=tk.LEFT, padx=5)
        
#         delete_btn = tk.Button(action_frame, text="Delete", command=self.delete_order,
#                               bg="#f44336", fg="white", font=("Arial", 9),
#                               padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
#         delete_btn.pack(side=tk.LEFT, padx=5)
        
#         # Load orders
#         self.load_orders()
    
#     def toggle_recurring_fields(self):
#         """Show/hide recurring fields based on checkbox"""
#         if self.is_recurring_var.get():
#             self.recurring_frame.grid()
#         else:
#             self.recurring_frame.grid_remove()
    
#     def create_order(self):
#         """Create a new order"""
#         schedule_time = self.schedule_time_entry.get().strip()
        
#         if not schedule_time:
#             messagebox.showerror("Error", "Please enter schedule time")
#             return
        
#         # Convert to ISO format
#         try:
#             dt = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
#             schedule_time_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
#         except ValueError:
#             messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM:SS")
#             return
        
#         order_data = {
#             "schedule_time": schedule_time_iso,
#             "is_recurring": self.is_recurring_var.get()
#         }
        
#         if self.is_recurring_var.get():
#             try:
#                 order_data["repeat_interval"] = int(self.repeat_interval_entry.get())
#                 order_data["repeat_unit"] = self.repeat_unit_var.get()
#                 order_data["max_executions"] = int(self.max_executions_entry.get())
#             except ValueError:
#                 messagebox.showerror("Error", "Invalid recurring parameters")
#                 return
        
#         try:
#             headers = {"Authorization": f"Bearer {self.token}"}
#             response = requests.post(f"{self.base_url}/orders/create",
#                                     json=order_data, headers=headers)
            
#             if response.status_code == 200 or response.status_code == 201:
#                 data = response.json()
#                 messagebox.showinfo("Success", f"Order created successfully! Order ID: {data.get('order_id')}")
#                 self.load_orders()
#             else:
#                 messagebox.showerror("Error", f"Failed to create order: {response.text}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Connection error: {str(e)}")
    
#     def load_orders(self):
#         """Load and display all orders"""
#         try:
#             headers = {"Authorization": f"Bearer {self.token}"}
#             response = requests.get(f"{self.base_url}/orders/", headers=headers)
            
#             if response.status_code == 200:
#                 data = response.json()
#                 orders = data.get("orders", [])
                
#                 self.orders_listbox.delete(0, tk.END)
#                 self.orders_data = orders
                
#                 for order in orders:
#                     order_id = order.get("order_id")
#                     status = order.get("status")
#                     schedule = order.get("schedule_time", "")[:19] if order.get("schedule_time") else ""
#                     is_recurring = "R" if order.get("is_recurring") else "O"
                    
#                     display_text = f"ID: {order_id:3d} | {is_recurring} | {status:10s} | {schedule}"
#                     self.orders_listbox.insert(tk.END, display_text)
#             else:
#                 messagebox.showerror("Error", f"Failed to load orders: {response.text}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Connection error: {str(e)}")
    
#     def view_order_details(self):
#         """View details of selected order"""
#         selection = self.orders_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("Warning", "Please select an order")
#             return
        
#         order = self.orders_data[selection[0]]
        
#         details = f"""Order ID: {order.get('order_id')}
# Status: {order.get('status')}
# Schedule Time: {order.get('schedule_time', 'N/A')}
# Created At: {order.get('created_at', 'N/A')}
# Is Recurring: {'Yes' if order.get('is_recurring') else 'No'}
# Repeat Interval: {order.get('repeat_interval', 'N/A')}
# Repeat Unit: {order.get('repeat_unit', 'N/A')}
# Max Executions: {order.get('max_executions', 'N/A')}
# Execution Count: {order.get('execution_count', 'N/A')}
# Job ID: {order.get('job_id', 'N/A')}"""
        
#         messagebox.showinfo("Order Details", details)
    
#     def update_order(self):
#         """Update selected order"""
#         selection = self.orders_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("Warning", "Please select an order")
#             return
        
#         order = self.orders_data[selection[0]]
#         order_id = order.get('order_id')
        
#         # Create update dialog
#         update_window = tk.Toplevel(self.root)
#         update_window.title(f"Update Order {order_id}")
#         update_window.geometry("400x350")
#         update_window.resizable(False, False)
        
#         frame = tk.Frame(update_window, bg="white", padx=20, pady=20)
#         frame.pack(fill=tk.BOTH, expand=True)
        
#         # Schedule Time
#         tk.Label(frame, text="Schedule Time:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
#         schedule_entry = ttk.Entry(frame, width=25)
#         schedule_entry.grid(row=0, column=1, pady=5)
#         current_time = order.get('schedule_time', '')
#         if current_time:
#             schedule_entry.insert(0, current_time[:19].replace('T', ' '))
        
#         # Is Recurring
#         is_recurring_var = tk.BooleanVar(value=bool(order.get('is_recurring')))
#         tk.Checkbutton(frame, text="Recurring", variable=is_recurring_var, bg="white").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
#         # Repeat Interval
#         tk.Label(frame, text="Repeat Interval:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
#         interval_entry = ttk.Entry(frame, width=10)
#         interval_entry.grid(row=2, column=1, pady=5, sticky=tk.W)
#         interval_entry.insert(0, str(order.get('repeat_interval', 1)))
        
#         # Repeat Unit
#         tk.Label(frame, text="Repeat Unit:", font=("Arial", 10), bg="white").grid(row=3, column=0, sticky=tk.W, pady=5)
#         unit_var = tk.StringVar(value=order.get('repeat_unit', 'MINUTE'))
#         unit_combo = ttk.Combobox(frame, textvariable=unit_var, values=["MINUTE", "HOUR", "DAY", "WEEK", "MONTH"], width=10, state="readonly")
#         unit_combo.grid(row=3, column=1, pady=5, sticky=tk.W)
        
#         # Max Executions
#         tk.Label(frame, text="Max Executions:", font=("Arial", 10), bg="white").grid(row=4, column=0, sticky=tk.W, pady=5)
#         max_exec_entry = ttk.Entry(frame, width=10)
#         max_exec_entry.grid(row=4, column=1, pady=5, sticky=tk.W)
#         max_exec_entry.insert(0, str(order.get('max_executions', 3)))
        
#         def submit_update():
#             schedule_time = schedule_entry.get().strip()
#             try:
#                 dt = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
#                 schedule_time_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
#             except ValueError:
#                 messagebox.showerror("Error", "Invalid date format")
#                 return
            
#             update_data = {
#                 "schedule_time": schedule_time_iso,
#                 "is_recurring": is_recurring_var.get(),
#                 "repeat_interval": int(interval_entry.get()),
#                 "repeat_unit": unit_var.get(),
#                 "max_executions": int(max_exec_entry.get())
#             }
            
#             try:
#                 headers = {"Authorization": f"Bearer {self.token}"}
#                 response = requests.put(f"{self.base_url}/orders/{order_id}",
#                                        json=update_data, headers=headers)
                
#                 if response.status_code == 200:
#                     messagebox.showinfo("Success", "Order updated successfully!")
#                     update_window.destroy()
#                     self.load_orders()
#                 else:
#                     messagebox.showerror("Error", f"Failed to update order: {response.text}")
#             except Exception as e:
#                 messagebox.showerror("Error", f"Connection error: {str(e)}")
        
#         tk.Button(frame, text="Update Order", command=submit_update,
#                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
#                  padx=20, pady=8, relief=tk.FLAT).grid(row=5, column=0, columnspan=2, pady=20)
    
#     def delete_order(self):
#         """Delete selected order"""
#         selection = self.orders_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("Warning", "Please select an order")
#             return
        
#         order = self.orders_data[selection[0]]
#         order_id = order.get('order_id')
        
#         if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete order {order_id}?"):
#             try:
#                 headers = {"Authorization": f"Bearer {self.token}"}
#                 response = requests.delete(f"{self.base_url}/orders/{order_id}", headers=headers)
                
#                 if response.status_code == 200:
#                     messagebox.showinfo("Success", "Order deleted successfully!")
#                     self.load_orders()
#                 else:
#                     messagebox.showerror("Error", f"Failed to delete order: {response.text}")
#             except Exception as e:
#                 messagebox.showerror("Error", f"Connection error: {str(e)}")
    
#     def logout(self):
#         """Handle user logout"""
#         try:
#             headers = {"Authorization": f"Bearer {self.token}"}
#             requests.post(f"{self.base_url}/auth/logout", headers=headers)
#         except:
#             pass
        
#         self.token = None
#         self.user_email = None
#         messagebox.showinfo("Logout", "You have been logged out successfully")
#         self.show_login_page()


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = OrderSchedulerApp(root)
#     root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
import json

class OrderSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Scheduler")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # API Base URL
        self.base_url = "http://localhost:3000"
        self.token = None
        self.user_email = None
        
        # Configure styles
        self.setup_styles()
        
        # Main container
        self.main_container = tk.Frame(root, bg="#f0f0f0")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Show login page initially
        self.show_login_page()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('TButton', padding=6, relief="flat", background="#4CAF50", foreground="white")
        style.map('TButton', background=[('active', '#45a049')])
        
        # Configure entry style
        style.configure('TEntry', padding=5, relief="solid")
        
    def clear_container(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_login_page(self):
        """Display login/signup page"""
        self.clear_container()
        
        # Center frame
        frame = tk.Frame(self.main_container, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title = tk.Label(frame, text="Order Scheduler", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Email
        tk.Label(frame, text="Email:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.email_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Password
        tk.Label(frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*", font=("Arial", 11))
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Buttons frame
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        login_btn = tk.Button(btn_frame, text="Login", command=self.login, 
                             bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                             padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        login_btn.pack(side=tk.LEFT, padx=5)
        
        signup_btn = tk.Button(btn_frame, text="Sign Up", command=self.signup,
                              bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        signup_btn.pack(side=tk.LEFT, padx=5)
    
    def login(self):
        """Handle user login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        try:
            response = requests.post(f"{self.base_url}/auth/login", 
                                    json={"email": email, "password": password})
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.user_email = email
                messagebox.showinfo("Success", "Login successful!")
                self.show_orders_page()
            else:
                messagebox.showerror("Error", f"Login failed: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def signup(self):
        """Handle user signup"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        try:
            response = requests.post(f"{self.base_url}/auth/signup",
                                    json={"email": email, "password": password})
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                token = data.get("token")
                
                # After signup, perform login to get a fresh token
                if token:
                    # Try to use the signup token first
                    self.token = token
                    self.user_email = email
                    
                    # Verify the token works by attempting to load orders
                    try:
                        headers = {"Authorization": f"Bearer {self.token}"}
                        test_response = requests.get(f"{self.base_url}/orders/", headers=headers)
                        
                        if test_response.status_code == 200:
                            messagebox.showinfo("Success", "Signup successful! You are now logged in.")
                            self.show_orders_page()
                        else:
                            # Token doesn't work, need to login
                            self.perform_login_after_signup(email, password)
                    except:
                        # If test fails, try logging in
                        self.perform_login_after_signup(email, password)
                else:
                    # No token returned, try logging in
                    self.perform_login_after_signup(email, password)
            else:
                messagebox.showerror("Error", f"Signup failed: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def perform_login_after_signup(self, email, password):
        """Helper method to login after signup"""
        try:
            response = requests.post(f"{self.base_url}/auth/login",
                                    json={"email": email, "password": password})
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.user_email = email
                messagebox.showinfo("Success", "Signup successful! You are now logged in.")
                self.show_orders_page()
            else:
                messagebox.showinfo("Signup Complete", 
                                  "Account created successfully! Please login with your credentials.")
                self.show_login_page()
        except Exception as e:
            messagebox.showinfo("Signup Complete", 
                              "Account created! Please login with your credentials.")
            self.show_login_page()
    
    def show_orders_page(self):
        """Display orders management page"""
        self.clear_container()
        
        # Header
        header = tk.Frame(self.main_container, bg="#4CAF50", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"Welcome, {self.user_email}", font=("Arial", 14, "bold"),
                bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        
        logout_btn = tk.Button(header, text="Logout", command=self.logout,
                              bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                              padx=15, pady=5, relief=tk.FLAT, cursor="hand2")
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Content frame
        content = tk.Frame(self.main_container, bg="#f0f0f0")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Create Order
        left_panel = tk.LabelFrame(content, text="Create New Order", font=("Arial", 12, "bold"),
                                   bg="white", padx=15, pady=15)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Schedule Time
        tk.Label(left_panel, text="Schedule Time:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(left_panel, text="(YYYY-MM-DD HH:MM:SS)", font=("Arial", 8), bg="white", fg="gray").grid(row=0, column=1, sticky=tk.W)
        self.schedule_time_entry = ttk.Entry(left_panel, width=25)
        self.schedule_time_entry.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W)
        self.schedule_time_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Is Recurring
        self.is_recurring_var = tk.BooleanVar()
        recurring_check = tk.Checkbutton(left_panel, text="Recurring Order", variable=self.is_recurring_var,
                                        font=("Arial", 10), bg="white", command=self.toggle_recurring_fields)
        recurring_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Recurring fields frame
        self.recurring_frame = tk.Frame(left_panel, bg="white")
        self.recurring_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        # Repeat Interval
        tk.Label(self.recurring_frame, text="Repeat Interval:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.repeat_interval_entry = ttk.Entry(self.recurring_frame, width=10)
        self.repeat_interval_entry.grid(row=0, column=1, pady=5, padx=5)
        self.repeat_interval_entry.insert(0, "1")
        
        # Repeat Unit
        tk.Label(self.recurring_frame, text="Repeat Unit:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.repeat_unit_var = tk.StringVar(value="MINUTE")
        repeat_unit_combo = ttk.Combobox(self.recurring_frame, textvariable=self.repeat_unit_var,
                                         values=["MINUTE", "HOUR", "DAY", "WEEK", "MONTH"], width=10, state="readonly")
        repeat_unit_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # Max Executions
        tk.Label(self.recurring_frame, text="Max Executions:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_executions_entry = ttk.Entry(self.recurring_frame, width=10)
        self.max_executions_entry.grid(row=2, column=1, pady=5, padx=5)
        self.max_executions_entry.insert(0, "3")
        
        # Initially hide recurring fields
        self.recurring_frame.grid_remove()
        
        # Create Order Button
        create_btn = tk.Button(left_panel, text="Create Order", command=self.create_order,
                              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                              padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        create_btn.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Right panel - Orders List
        right_panel = tk.LabelFrame(content, text="Your Orders", font=("Arial", 12, "bold"),
                                    bg="white", padx=15, pady=15)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Refresh button
        refresh_btn = tk.Button(right_panel, text="🔄 Refresh", command=self.load_orders,
                               bg="#2196F3", fg="white", font=("Arial", 9),
                               padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
        refresh_btn.pack(anchor=tk.NE, pady=(0, 10))
        
        # Orders listbox with scrollbar
        list_frame = tk.Frame(right_panel, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.orders_listbox = tk.Listbox(list_frame, font=("Courier", 9), 
                                         yscrollcommand=scrollbar.set, height=15)
        self.orders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.orders_listbox.yview)
        
        # Action buttons
        action_frame = tk.Frame(right_panel, bg="white")
        action_frame.pack(fill=tk.X, pady=10)
        
        view_btn = tk.Button(action_frame, text="View Details", command=self.view_order_details,
                            bg="#2196F3", fg="white", font=("Arial", 9),
                            padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
        view_btn.pack(side=tk.LEFT, padx=5)
        
        update_btn = tk.Button(action_frame, text="Update", command=self.update_order,
                              bg="#FF9800", fg="white", font=("Arial", 9),
                              padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
        update_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(action_frame, text="Delete", command=self.delete_order,
                              bg="#f44336", fg="white", font=("Arial", 9),
                              padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Load orders
        self.load_orders()
    
    def toggle_recurring_fields(self):
        """Show/hide recurring fields based on checkbox"""
        if self.is_recurring_var.get():
            self.recurring_frame.grid()
        else:
            self.recurring_frame.grid_remove()
    
    def create_order(self):
        """Create a new order"""
        schedule_time = self.schedule_time_entry.get().strip()
        
        if not schedule_time:
            messagebox.showerror("Error", "Please enter schedule time")
            return
        
        # Convert to ISO format
        try:
            dt = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
            schedule_time_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM:SS")
            return
        
        order_data = {
            "schedule_time": schedule_time_iso,
            "is_recurring": self.is_recurring_var.get()
        }
        
        if self.is_recurring_var.get():
            try:
                order_data["repeat_interval"] = int(self.repeat_interval_entry.get())
                order_data["repeat_unit"] = self.repeat_unit_var.get()
                order_data["max_executions"] = int(self.max_executions_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid recurring parameters")
                return
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.base_url}/orders/create",
                                    json=order_data, headers=headers)
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                messagebox.showinfo("Success", f"Order created successfully! Order ID: {data.get('order_id')}")
                self.load_orders()
            elif response.status_code == 401 or response.status_code == 403:
                messagebox.showerror("Session Expired", "Your session has expired. Please login again.")
                self.logout()
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_msg)
                except:
                    pass
                messagebox.showerror("Error", f"Failed to create order: {error_msg}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def load_orders(self):
        """Load and display all orders"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/orders/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get("orders", [])
                
                self.orders_listbox.delete(0, tk.END)
                self.orders_data = orders
                
                for order in orders:
                    order_id = order.get("order_id")
                    status = order.get("status")
                    schedule = order.get("schedule_time", "")[:19] if order.get("schedule_time") else ""
                    is_recurring = "R" if order.get("is_recurring") else "O"
                    
                    display_text = f"ID: {order_id:3d} | {is_recurring} | {status:10s} | {schedule}"
                    self.orders_listbox.insert(tk.END, display_text)
            elif response.status_code == 401 or response.status_code == 403:
                # Session expired or unauthorized
                messagebox.showerror("Session Expired", "Your session has expired. Please login again.")
                self.logout()
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_msg)
                except:
                    pass
                messagebox.showerror("Error", f"Failed to load orders: {error_msg}")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def view_order_details(self):
        """View details of selected order"""
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order")
            return
        
        order = self.orders_data[selection[0]]
        
        details = f"""Order ID: {order.get('order_id')}
Status: {order.get('status')}
Schedule Time: {order.get('schedule_time', 'N/A')}
Created At: {order.get('created_at', 'N/A')}
Is Recurring: {'Yes' if order.get('is_recurring') else 'No'}
Repeat Interval: {order.get('repeat_interval', 'N/A')}
Repeat Unit: {order.get('repeat_unit', 'N/A')}
Max Executions: {order.get('max_executions', 'N/A')}
Execution Count: {order.get('execution_count', 'N/A')}
Job ID: {order.get('job_id', 'N/A')}"""
        
        messagebox.showinfo("Order Details", details)
    
    def update_order(self):
        """Update selected order"""
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order")
            return
        
        order = self.orders_data[selection[0]]
        order_id = order.get('order_id')
        
        # Create update dialog
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Order {order_id}")
        update_window.geometry("400x350")
        update_window.resizable(False, False)
        
        frame = tk.Frame(update_window, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Schedule Time
        tk.Label(frame, text="Schedule Time:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        schedule_entry = ttk.Entry(frame, width=25)
        schedule_entry.grid(row=0, column=1, pady=5)
        current_time = order.get('schedule_time', '')
        if current_time:
            schedule_entry.insert(0, current_time[:19].replace('T', ' '))
        
        # Is Recurring
        is_recurring_var = tk.BooleanVar(value=bool(order.get('is_recurring')))
        tk.Checkbutton(frame, text="Recurring", variable=is_recurring_var, bg="white").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Repeat Interval
        tk.Label(frame, text="Repeat Interval:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        interval_entry = ttk.Entry(frame, width=10)
        interval_entry.grid(row=2, column=1, pady=5, sticky=tk.W)
        interval_entry.insert(0, str(order.get('repeat_interval', 1)))
        
        # Repeat Unit
        tk.Label(frame, text="Repeat Unit:", font=("Arial", 10), bg="white").grid(row=3, column=0, sticky=tk.W, pady=5)
        unit_var = tk.StringVar(value=order.get('repeat_unit', 'MINUTE'))
        unit_combo = ttk.Combobox(frame, textvariable=unit_var, values=["MINUTE", "HOUR", "DAY", "WEEK", "MONTH"], width=10, state="readonly")
        unit_combo.grid(row=3, column=1, pady=5, sticky=tk.W)
        
        # Max Executions
        tk.Label(frame, text="Max Executions:", font=("Arial", 10), bg="white").grid(row=4, column=0, sticky=tk.W, pady=5)
        max_exec_entry = ttk.Entry(frame, width=10)
        max_exec_entry.grid(row=4, column=1, pady=5, sticky=tk.W)
        max_exec_entry.insert(0, str(order.get('max_executions', 3)))
        
        def submit_update():
            schedule_time = schedule_entry.get().strip()
            try:
                dt = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
                schedule_time_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format")
                return
            
            update_data = {
                "schedule_time": schedule_time_iso,
                "is_recurring": is_recurring_var.get(),
                "repeat_interval": int(interval_entry.get()),
                "repeat_unit": unit_var.get(),
                "max_executions": int(max_exec_entry.get())
            }
            
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.put(f"{self.base_url}/orders/{order_id}",
                                       json=update_data, headers=headers)
                
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Order updated successfully!")
                    update_window.destroy()
                    self.load_orders()
                else:
                    messagebox.showerror("Error", f"Failed to update order: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {str(e)}")
        
        tk.Button(frame, text="Update Order", command=submit_update,
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=8, relief=tk.FLAT).grid(row=5, column=0, columnspan=2, pady=20)
    
    def delete_order(self):
        """Delete selected order"""
        selection = self.orders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order")
            return
        
        order = self.orders_data[selection[0]]
        order_id = order.get('order_id')
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete order {order_id}?"):
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.delete(f"{self.base_url}/orders/{order_id}", headers=headers)
                
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Order deleted successfully!")
                    self.load_orders()
                else:
                    messagebox.showerror("Error", f"Failed to delete order: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def logout(self):
        """Handle user logout"""
        try:
            if self.token:
                headers = {"Authorization": f"Bearer {self.token}"}
                requests.post(f"{self.base_url}/auth/logout", headers=headers)
        except:
            pass
        
        self.token = None
        self.user_email = None
        self.show_login_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderSchedulerApp(root)
    root.mainloop()