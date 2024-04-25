import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk
import requests

def send_get_request(url, headers=None, auth=None):
    try:
        response = requests.get(url, headers=headers, auth=auth)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return 500, str(e)

def send_post_request(url, data, headers=None, auth=None):
    try:
        response = requests.post(url, data=data, headers=headers, auth=auth)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return 500, str(e)

def send_request(url, method, username, password):
    headers = {"User-Agent": "Mozilla/5.0"}
    auth = None
    if username and password:
        auth = (username.get(), password.get())
    
    if method.get() == "GET":
        status_code, response = send_get_request(url.get(), headers=headers, auth=auth)
    else:
        # استخدام بيانات تسجيل الدخول في الطلب POST
        status_code, response = send_post_request(url.get(), {"username": username.get(), "password": password.get()}, headers=headers, auth=auth)
    
    # إذا كان هناك استجابة، عرضها مع المعلومات المدخلة
    if response:
        response_with_user_info = f"Status Code: {status_code}\nResponse: {response}\n\nUsername: {username.get()}\nPassword: {password.get()}"
    else:
        response_with_user_info = f"Status Code: {status_code}\nResponse: No response\n\nUsername: {username.get()}\nPassword: {password.get()}"
    
    messagebox.showinfo("Response", response_with_user_info)

root = tk.Tk()
root.title("PyBrowser")

# Frame لعرض الصورة
image_frame = tk.Frame(root)
image_frame.grid(row=0, column=0, columnspan=2)

# فتح الصورة باستخدام PIL
img = Image.open("imgg.PNG")

# تحويل الصورة إلى PhotoImage
image = ImageTk.PhotoImage(img)

# عرض الصورة داخل Label داخل Frame
image_label = tk.Label(image_frame, image=image)
image_label.pack()

# Frame للعناصر الأخرى
form_frame = tk.Frame(root)
form_frame.grid(row=1, column=0, columnspan=2)

tk.Label(form_frame, text="URL:").grid(row=0, column=0)
url_entry = tk.Entry(form_frame)
url_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Method:").grid(row=1, column=0)
method_options = ["GET", "POST"]
method = tk.StringVar(root)
method.set(method_options[0])
method_menu = tk.OptionMenu(form_frame, method, *method_options)
method_menu.grid(row=1, column=1)

tk.Label(form_frame, text="Username:").grid(row=2, column=0)
username_entry = tk.Entry(form_frame)
username_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Password:").grid(row=3, column=0)
password_entry = tk.Entry(form_frame, show="*")
password_entry.grid(row=3, column=1)

# تعريف الأزرار
send_button = tk.Button(form_frame, text="Send Request", command=partial(send_request, url_entry, method, username_entry, password_entry))
send_button.grid(row=4, columnspan=2)

# تحديث لون الخلفية لكافة الأزرار
for child in form_frame.winfo_children():
    if isinstance(child, tk.Button):
        child.config(bg="#FFC0CB")

root.mainloop()

