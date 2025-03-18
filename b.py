import tkinter as tk
import time
from tkinter import messagebox

# Hàm kiểm tra giờ học và hiển thị thông báo
def check_time():
    current_time = time.localtime()
    current_hour = current_time.tm_hour
    current_minute = current_time.tm_min
    current_time_str = time.strftime("%H:%M:%S", current_time)
    
    label_time.config(text="Current Time: " + current_time_str)

    # Giả sử giờ học là 8:30 và 14:00
    # if (current_hour == 8 and current_minute == 30) or (current_hour == 14 and current_minute == 0):
    #     messagebox.showinfo("Reminder", "It's time for your English lesson!")
    if current_hour == 21:
        messagebox.showinfo("Reminder", "It's time for your English lesson!")

    # Cập nhật lại sau mỗi 60 giây
    window.after(60000, check_time)

# Tạo cửa sổ ứng dụng
window = tk.Tk()
window.title("English Lesson Reminder")

# Label hiển thị giờ hiện tại
label_time = tk.Label(window, font=("Arial", 20))
label_time.pack(pady=20)

# Gọi hàm kiểm tra thời gian
check_time()

# Bắt đầu chạy ứng dụng
window.mainloop()
