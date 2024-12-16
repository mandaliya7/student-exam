import tkinter as tk
from tkinter import messagebox
import pandas as pd
import subprocess
import sys

# Read the exam CSV file
csv_file_path = 'exam.csv'
questions_df = pd.read_csv(csv_file_path)

# Get the username from the command line arguments
username = sys.argv[1] if len(sys.argv) > 1 else "User"

class ExamApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("RTO Online Exam")
        self.current_question = 0
        self.score = 0
        self.questions = questions_df.to_dict('records')
        self.var = tk.IntVar(value=-1)  # Using a single IntVar for Radiobuttons
        self.selected_answers = [-1] * len(self.questions)  # Store answers for each question

        # Initial window size
        self.window_width = int(self.root.winfo_screenwidth() * 0.8 * 1.2)
        self.window_height = int(self.root.winfo_screenheight() * 0.8 * 1.2)
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.config(bg="#f4f4f9")

        # Create a frame to hold all content
        frame_width = 800
        frame_height = 650
        frame = tk.Frame(self.root, bg='#ffffff', bd=12, relief='ridge', width=frame_width, height=frame_height)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        # Title Section
        self.title_label = tk.Label(frame, text="MSQ", font=("Arial", 36, "bold"), bg='white', fg='#0056b3')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Welcome message with username
        self.welcome_label = tk.Label(frame, text=f"Welcome, {username}!", font=("Arial", 18), bg='white', fg='#555')
        self.welcome_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Question number and total number of questions
        self.question_progress_label = tk.Label(frame, text="", font=("Arial", 16), bg='white', fg='#007bff')
        self.question_progress_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Question label
        self.question_label = tk.Label(frame, text="", wraplength=600, justify="left", bg='white', fg='#333', font=("Arial", 18))
        self.question_label.grid(row=3, column=0, columnspan=2, pady=20)

        # Create a new frame for the options, to use grid layout for 2x2
        options_frame = tk.Frame(frame, bg='white')
        options_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Option buttons (radio buttons for single selection)
        self.option_buttons = []
        option_labels = ['A', 'B', 'C', 'D']  # Labels for the options A, B, C, D
        for i in range(4):
            button = tk.Radiobutton(options_frame, text="", variable=self.var, value=i, bg='white', fg='#333', font=("Arial", 14), indicatoron=0, padx=20, pady=10, width=40)
            self.option_buttons.append(button)

        # Layout options in 2x2 grid and label them as A, B, C, D
        for i, button in enumerate(self.option_buttons):
            row = i // 2  # Determines the row number (0 or 1)
            col = i % 2   # Determines the column number (0 or 1)
            button.grid(row=row, column=col, padx=20, pady=10, sticky="ew")  # Use sticky="ew" to expand across columns
            button.config(text=f"{option_labels[i]}. ")  # Add A, B, C, D labels

        # Navigation buttons
        self.previous_button = tk.Button(frame, text="Previous", command=self.previous_question, bg="#28a745", fg="white", font=("Arial", 16), width=20)
        self.previous_button.grid(row=5, column=0, pady=10, padx=20, sticky="ew")

        self.submit_button = tk.Button(frame, text="Next", command=self.submit_answer, bg="#007bff", fg="white", font=("Arial", 16), width=20)
        self.submit_button.grid(row=5, column=1, pady=10, padx=20, sticky="ew")

        # Show the first question
        self.show_question()

    def show_question(self):
        question = self.questions[self.current_question]
        self.question_label.config(text=f"Q{self.current_question + 1}: {question['question']}")
        options = [question['option1'], question['option2'], question['option3'], question['option4']]
        self.var.set(self.selected_answers[self.current_question])  # Set previously selected answer if exists
        for i, option in enumerate(options):
            self.option_buttons[i].config(text=f"{['A', 'B', 'C', 'D'][i]}. {option}")

        # Update progress indicator
        self.question_progress_label.config(text=f"Question {self.current_question + 1} of {len(self.questions)}")

    def animate_selection(self):
        selected_index = self.var.get()

        if selected_index != -1:
            selected_button = self.option_buttons[selected_index]

            # Change color of selected option (animation effect)
            selected_button.config(bg="#d4edda")  # Light green for selection
            self.root.after(300, lambda: selected_button.config(bg="white"))  # Reset to white after 300ms

    def on_hover(self, event):
        """Change background color when the user hovers over an option."""
        event.widget.config(bg="#e9ecef")  # Light gray on hover

    def on_leave(self, event):
        """Revert the background color when the hover ends."""
        if self.var.get() == -1 or self.var.get() != self.option_buttons.index(event.widget):
            event.widget.config(bg="white")  # Reset background to white

    def submit_answer(self):
        selected_answer = self.var.get()

        if selected_answer == -1:
            messagebox.showwarning("Warning", "You must select an answer!")
            return

        # Store the selected answer for the current question
        self.selected_answers[self.current_question] = selected_answer

        correct_answer = self.questions[self.current_question]['answer']
        selected_text = self.option_buttons[selected_answer].cget("text")

        if correct_answer == selected_text:
            self.score += 1

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.end_exam()

    def previous_question(self):
        """Navigate to the previous question."""
        if self.current_question > 0:
            self.current_question -= 1
            self.show_question()

    def end_exam(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Exam completed! Your score: {self.score}/{len(self.questions)}", font=("Arial", 20, "bold"), bg='white', fg='#007bff').pack(pady=30)
        tk.Button(self.root, text="Logout", command=self.logout, bg="#007bff", fg="white", font=("Arial", 16), width=20).pack(pady=30)

    def logout(self):
        self.root.destroy()
        subprocess.run(['python3', 'registration.py'])  # Redirect to registration.py

def start_exam():
    try:
        root = tk.Tk()
        username = sys.argv[1] if len(sys.argv) > 1 else "User"
        app = ExamApp(root, username)
        root.mainloop()
    except KeyboardInterrupt:
        print("Exam interrupted by the user. Exiting gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    start_exam()