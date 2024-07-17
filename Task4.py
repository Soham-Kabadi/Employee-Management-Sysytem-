from tkinter import *
from tkinter.messagebox import *
from tkinter import scrolledtext
import matplotlib.pyplot as plt
import sqlite3
import requests

def get_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data.get('city', '') + ', ' + data.get('region', '') + ', ' + data.get('country', '')
        ent_location.delete(0, END)
        ent_location.insert(0, location)
        
        # Extract city name
        city = data.get('city', '')
        
        # Fetch temperature data using another API
        weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9b6ea3954b24675a572d6ed426c52975')
        weather_data = weather_response.json()
        
        # Check if 'main' key exists in the response
        if 'main' in weather_data:
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            ent_temperature.delete(0, END)
            ent_temperature.insert(0, f"{temperature_celsius:.2f} °C")
        else:
            showerror("Error", "Failed to fetch temperature data.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch location data: {e}")

def save_data():
    # Connect to SQLite database
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    
    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 salary REAL)''')
    
    # Validate ID
    id_val = ent_id.get()
    if not id_val:
        showerror("Error", "ID cannot be empty!")
        return
    elif not id_val.isdigit():
        showerror("Error", "ID must be a non-negative integer!")
        return
    elif int(id_val) < 0:
        showerror("Error", "ID cannot be negative!")
        return
    elif ' ' in id_val:
        showerror("Error", "ID cannot contain spaces!")
        return
    
    # Validate Name
    name_val = ent_name.get()
    if not name_val:
        showerror("Error", "Name cannot be empty!")
        return
    elif not name_val.isalpha():
        showerror("Error", "Name must contain alphabetic characters only!")
        return
    
    # Validate Salary
    salary_val = ent_salary.get()
    if not salary_val:
        showerror("Error", "Salary cannot be empty!")
        return
    elif not salary_val.replace('.', '', 1).isdigit():
        showerror("Error", "Salary must be a positive number!")
        return
    elif float(salary_val) <= 0:
        showerror("Error", "Salary must be greater than zero!")
        return
    
    # Insert data into the table
    c.execute("INSERT INTO employees (id, name, salary) VALUES (?, ?, ?)",
              (id_val, name_val, salary_val))
    
    conn.commit()
    conn.close()
    showinfo("Success", "Data saved successfully!")

def open_add_window():
    global add_window
    add_window = Toplevel(root)
    add_window.title("Add Employee")
    add_window.geometry("1000x800+50+50")
    
    f = ("Times New Roman", 16)
    
    # Labels and Entry widgets for ID, Name, and Salary
    lab_id = Label(add_window, text="Enter ID:", font=f)
    lab_id.pack(pady=5)
    global ent_id
    ent_id = Entry(add_window, font=f)
    ent_id.pack(pady=5)
    
    lab_name = Label(add_window, text="Enter Name:", font=f)
    lab_name.pack(pady=5)
    global ent_name
    ent_name = Entry(add_window, font=f)
    ent_name.pack(pady=5)
    
    lab_salary = Label(add_window, text="Enter Salary:", font=f)
    lab_salary.pack(pady=5)
    global ent_salary
    ent_salary = Entry(add_window, font=f)
    ent_salary.pack(pady=5)
   
    # Save Button
    Button(add_window, text="Save", font=f, command=save_data, height=1, width=10).pack(pady=5)
    
    # Back Button
    Button(add_window, text="Back", font=f, command=add_window.destroy, height=1, width=10).pack(pady=5)

def delete_data():
    global delete_window
    delete_window = Toplevel(root)
    delete_window.title("Delete Employee")
    delete_window.geometry("1000x800+50+50")
    
    f = ("Times New Roman", 16)
    
    # Labels and Entry widgets for ID
    lab_delete_id = Label(delete_window, text="Enter ID to delete:", font=f)
    lab_delete_id.pack(pady=5)
    global ent_delete_id
    ent_delete_id = Entry(delete_window, font=f)
    ent_delete_id.pack(pady=5)
    
    # Delete Button
    Button(delete_window, text="Delete", font=f, command=delete_employee, height=1, width=10).pack(pady=5)
    
    # Back Button
    Button(delete_window, text="Back", font=f, command=delete_window.destroy, height=1, width=10).pack(pady=5)

def delete_employee():
    # Connect to SQLite database
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    
    # Delete data from the table
    id_val = ent_delete_id.get()
    
    c.execute("DELETE FROM employees WHERE id = ?", (id_val,))
    
    if c.rowcount == 0:
        showerror("Error", "ID not found!")
    else:
        conn.commit()
        showinfo("Success", "Employee data deleted successfully!")
    
    conn.close()

def update_data():
    global update_window
    update_window = Toplevel(root)
    update_window.title("Update Employee")
    update_window.geometry("1000x800+50+50")
    
    f = ("Times New Roman", 16)
    
    # Labels and Entry widgets for ID, Name, and Salary
    lab_id = Label(update_window, text="Enter ID:", font=f)
    lab_id.pack(pady=5)
    global ent_id
    ent_id = Entry(update_window, font=f)
    ent_id.pack(pady=5)
    
    lab_name = Label(update_window, text="Enter Name:", font=f)
    lab_name.pack(pady=5)
    global ent_name
    ent_name = Entry(update_window, font=f)
    ent_name.pack(pady=5)
    
    lab_salary = Label(update_window, text="Enter Salary:", font=f)
    lab_salary.pack(pady=5)
    global ent_salary
    ent_salary = Entry(update_window, font=f)
    ent_salary.pack(pady=5)
    
    # Update Button
    Button(update_window, text="Update", font=f, command=update_employee, height=1, width=10).pack(pady=5)
    
    # Back Button
    Button(update_window, text="Back", font=f, command=update_window.destroy, height=1, width=10).pack(pady=5)

def update_employee():
    # Connect to SQLite database
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    
    # Update data in the table
    id_val = ent_id.get()
    name_val = ent_name.get()
    salary_val = ent_salary.get()
    
    # Validate input
    if not id_val or not name_val or not salary_val:
        showerror("Error", "Please fill in all fields!")
        return
    
     # Update data in the table
    c.execute("UPDATE employees SET name = ?, salary = ? WHERE id = ?",
              (name_val, salary_val, id_val))
    
    # Check if any rows were affected
    if c.rowcount == 0:
        showerror("Error", "No employee with this ID found!")
    else:
        conn.commit()
        showinfo("Success", "Employee data updated successfully!")
    
    conn.close()

def view_data():
    global view_window
    view_window = Toplevel(root)
    view_window.title("View Employees")
    view_window.geometry("1000x800+50+50")
    
    f = ("Times New Roman", 16)
    
    # Scrolled Text for displaying data
    scroll_text = scrolledtext.ScrolledText(view_window, font=f)
    scroll_text.pack(expand=True, fill='both')
    
    # Fetch data from the database
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    data = c.fetchall()
    conn.close()
    
    # Display data in the scrolled text
    for item in data:
        scroll_text.insert(INSERT, f"ID: {item[0]}, Name: {item[1]}, Salary: {item[2]}\n")

    # Back Button
    Button(view_window, text="Back", font=f, command=view_window.destroy, height=1, width=10).pack(pady=5)

def show_chart():
    # Fetch top 5 highest earning salaried employees
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5")
    data = c.fetchall()
    conn.close()
    
    # Prepare data for plotting
    names = [item[0] for item in data]
    salaries = [item[1] for item in data]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.barh(names, salaries, color='skyblue')
    plt.xlabel('Salary')
    plt.ylabel('Employee Name')
    plt.title('Top 5 Highest Earning Salaried Employees')
    plt.tight_layout()
    plt.show()

root = Tk()
root.title("E.M.S")
root.geometry("1000x800+50+50")
f = ("Times New Roman", 30, "bold")

btn_add = Button(root, text="Add", font=f, command=open_add_window, height=1, width=10)
btn_update = Button(root, text="Update", font=f, command=update_data, height=1, width=10)
btn_view = Button(root, text="View", font=f, command=view_data, height=1, width=10)
btn_delete = Button(root, text="Delete", font=f, command=delete_data, height=1, width=10)
btn_charts = Button(root, text="Charts", font=f, command=show_chart,height=1, width=10)
lab_location = Label(root, text="Location: ", font=f)
ent_location = Entry(root, font=f)
lbl_temp = Label(root, text="Temperature:", font=f)
ent_temperature = Entry(root, font=f)
  
btn_add.pack(pady=5)
btn_update.pack(pady=5)
btn_view.pack(pady=5)
btn_delete.pack(pady=5)
btn_charts.pack(pady=5)
lab_location.pack(pady=5)
ent_location.pack(pady=5)
lbl_temp.pack(pady=5)
ent_temperature.pack(pady=5)

# Automatically get location and temperature
get_location()

root.mainloop()
