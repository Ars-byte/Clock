import tkinter as tk
import customtkinter as ctk
import time

class ChronometerApp:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root.title("Clock")
        self.root.geometry("600x800")

        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed_time = 0
        self.stopwatch_job = None

        self.clock_job = None

        self.timer_running = False
        self.timer_remaining_seconds = 0
        self.timer_initial_duration = 0
        self.timer_job = None

        self.create_main_widgets()
        self.create_tabs_and_content()
        self.update_clock()

    def create_main_widgets(self):
        top_bar_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_bar_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

        self.exit_button = ctk.CTkButton(
            top_bar_frame,
            text="Exit",
            width=100,
            command=self.root.quit,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a"
        )
        self.exit_button.pack(side=tk.RIGHT)

        self.author_label = ctk.CTkLabel(top_bar_frame, text="by: Ars byte", text_color="gray")
        self.author_label.pack(side=tk.RIGHT, padx=(0,10))


        bottom_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 10))
        self.blank_label = ctk.CTkLabel(bottom_frame, text="", text_color="white")
        self.blank_label.pack(side=tk.RIGHT)


    def create_tabs_and_content(self):
        self.tab_view = ctk.CTkTabview(self.root, fg_color="#2b2b2b")
        self.tab_view.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.stopwatch_tab = self.tab_view.add("Stopwatch")
        self.clock_tab = self.tab_view.add("Clock")
        self.timer_tab = self.tab_view.add("Timer")

        self.create_stopwatch_widgets(self.stopwatch_tab)
        self.create_clock_widgets(self.clock_tab)
        self.create_timer_widgets(self.timer_tab)
        
        self.tab_view.set("Stopwatch")

    def create_stopwatch_widgets(self, tab):
        self.stopwatch_time_label = ctk.CTkLabel(
            tab,
            text="00:00:00.000",
            font=("Helvetica", 36),
            text_color="#e0e0e0"
        )
        self.stopwatch_time_label.pack(pady=(40, 20), expand=True)

        stopwatch_buttons_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stopwatch_buttons_frame.pack(pady=20)

        self.stopwatch_toggle_button = ctk.CTkButton(
            stopwatch_buttons_frame,
            text="Start",
            command=self.toggle_stopwatch,
            width=120,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a"
        )
        self.stopwatch_toggle_button.grid(row=0, column=0, padx=10)

        self.stopwatch_reset_button = ctk.CTkButton(
            stopwatch_buttons_frame,
            text="Reset",
            command=self.reset_stopwatch,
            width=120,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a"
        )
        self.stopwatch_reset_button.grid(row=0, column=1, padx=10)

    def toggle_stopwatch(self):
        if not self.stopwatch_running:
            if self.stopwatch_elapsed_time == 0:
                self.stopwatch_start_time = time.time()
            else: 
                self.stopwatch_start_time = time.time() - self.stopwatch_elapsed_time
            self.stopwatch_running = True
            self.stopwatch_toggle_button.configure(text="Pause")
            self.update_stopwatch_display()
        else: 
            self.stopwatch_running = False
            self.stopwatch_toggle_button.configure(text="Continue")
            if self.stopwatch_job:
                self.root.after_cancel(self.stopwatch_job)
                self.stopwatch_job = None

    def reset_stopwatch(self):
        if self.stopwatch_job:
            self.root.after_cancel(self.stopwatch_job)
            self.stopwatch_job = None
        self.stopwatch_running = False
        self.stopwatch_elapsed_time = 0
        self.stopwatch_start_time = 0
        self.stopwatch_time_label.configure(text="00:00:00.000")
        self.stopwatch_toggle_button.configure(text="Start")

    def update_stopwatch_display(self):
        if self.stopwatch_running:
            self.stopwatch_elapsed_time = time.time() - self.stopwatch_start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(self.stopwatch_elapsed_time))
            milliseconds = f".{int((self.stopwatch_elapsed_time % 1) * 1000):03d}"
            self.stopwatch_time_label.configure(text=formatted_time + milliseconds)
            self.stopwatch_job = self.root.after(10, self.update_stopwatch_display)

    def create_clock_widgets(self, tab):
        self.clock_label = ctk.CTkLabel(
            tab,
            text="00:00:00",
            font=("Helvetica", 48, "bold"),
            text_color="#e0e0e0"
        )
        self.clock_label.pack(pady=(50,0), expand=True, fill="both", anchor="center")

    def update_clock(self):
        if hasattr(self, 'clock_label'):
            current_time = time.strftime("%H:%M:%S")
            self.clock_label.configure(text=current_time)
        self.clock_job = self.root.after(1000, self.update_clock)

    def create_timer_widgets(self, tab):
        input_frame = ctk.CTkFrame(tab, fg_color="transparent")
        input_frame.pack(pady=10)

        set_time_label = ctk.CTkLabel(input_frame, text="Set Time:", font=("Helvetica", 14))
        set_time_label.grid(row=0, column=0, columnspan=6, pady=(0,5))

        hours_label = ctk.CTkLabel(input_frame, text="Hours:", width=60)
        hours_label.grid(row=1, column=0, padx=5)
        self.timer_hours_entry = ctk.CTkEntry(input_frame, width=50, justify="center")
        self.timer_hours_entry.grid(row=1, column=1, padx=5)
        self.timer_hours_entry.insert(0, "0")

        minutes_label = ctk.CTkLabel(input_frame, text="Minutes:", width=60)
        minutes_label.grid(row=1, column=2, padx=5)
        self.timer_minutes_entry = ctk.CTkEntry(input_frame, width=50, justify="center")
        self.timer_minutes_entry.grid(row=1, column=3, padx=5)
        self.timer_minutes_entry.insert(0, "0")

        seconds_label = ctk.CTkLabel(input_frame, text="Seconds:", width=60)
        seconds_label.grid(row=1, column=4, padx=5)
        self.timer_seconds_entry = ctk.CTkEntry(input_frame, width=50, justify="center")
        self.timer_seconds_entry.grid(row=1, column=5, padx=5)
        self.timer_seconds_entry.insert(0, "5")

        self.timer_display_label = ctk.CTkLabel(
            tab,
            text="00:00:00",
            font=("Helvetica", 36),
            text_color="#e0e0e0"
        )
        self.timer_display_label.pack(pady=20, expand=True)

        timer_buttons_frame = ctk.CTkFrame(tab, fg_color="transparent")
        timer_buttons_frame.pack(pady=10)

        self.timer_toggle_button = ctk.CTkButton(
            timer_buttons_frame,
            text="Start",
            command=self.toggle_timer,
            width=120,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a"
        )
        self.timer_toggle_button.grid(row=0, column=0, padx=10)

        self.timer_reset_button = ctk.CTkButton(
            timer_buttons_frame,
            text="Reset",
            command=self.reset_timer,
            width=120,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a"
        )
        self.timer_reset_button.grid(row=0, column=1, padx=10)


    def toggle_timer(self):
        if not self.timer_running:
            if self.timer_remaining_seconds == 0: 
                try:
                    h = int(self.timer_hours_entry.get() or "0")
                    m = int(self.timer_minutes_entry.get() or "0")
                    s = int(self.timer_seconds_entry.get() or "0")
                    self.timer_initial_duration = h * 3600 + m * 60 + s
                    if self.timer_initial_duration <= 0:
                        self.timer_display_label.configure(text="Invalid Input")
                        return
                    self.timer_remaining_seconds = self.timer_initial_duration
                except ValueError:
                    self.timer_display_label.configure(text="Invalid Input")
                    return
            
            if self.timer_remaining_seconds > 0 :
                self.timer_running = True
                self.timer_toggle_button.configure(text="Pause")
                self.update_timer_display()
        else: 
            self.timer_running = False
            self.timer_toggle_button.configure(text="Continue")
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
                self.timer_job = None

    def reset_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False
        self.timer_remaining_seconds = 0
        self.timer_initial_duration = 0
        self.timer_display_label.configure(text="00:00:00")
        self.timer_toggle_button.configure(text="Start")


    def update_timer_display(self):
        if self.timer_running and self.timer_remaining_seconds > 0:
            self.timer_remaining_seconds -= 1
            self.timer_display_label.configure(text=self.format_time_hhmmss(self.timer_remaining_seconds))
            self.timer_job = self.root.after(1000, self.update_timer_display)
        elif self.timer_remaining_seconds == 0 and self.timer_running : # Check timer_running to ensure it was running
            self.timer_running = False
            self.timer_display_label.configure(text="Time's Up!")
            self.root.bell() 
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
                self.timer_job = None
            self.timer_toggle_button.configure(text="Start")


    def format_time_hhmmss(self, total_seconds):
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def on_closing(self):
        if self.stopwatch_job:
            self.root.after_cancel(self.stopwatch_job)
        if self.clock_job:
            self.root.after_cancel(self.clock_job)
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = ChronometerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
