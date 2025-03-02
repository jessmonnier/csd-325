'''
Jess Monnier
CSD-325 Assignment 10.2
1 March 2025
'''

import tkinter as tk
import tkinter.messagebox as msg
from tkinter import font

# Create class derived from main tkinter module for use in app
class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        # Handle scenarios when tasks are or are not fed to a new program instance
        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks
        
        # Get the default font in order to create strikethrough & non-strikethrough
        # This is for marking task completion
        self.default_font = font.nametofont("TkDefaultFont").actual()
        self.strike_font = font.Font(family=self.default_font["family"], 
                                     size=self.default_font["size"],
                                     overstrike=1)
        self.normal_font = font.Font(family=self.default_font["family"], 
                                     size=self.default_font["size"],
                                     overstrike=0)
        
        # Set text for the Help button in the File menu.
        self.help_text = """
Left-click a task to toggle completion (strikethrough = complete).
Right-click a task for a menu of options:
    Toggle completion
    Remove from app
    Move up or down"""
        
        # Set up the tkinter frame/canvas foundational widgets
        self.tasks_canvas = tk.Canvas(self)

        self.tasks_frame = tk.Frame(self.tasks_canvas)
        self.text_frame = tk.Frame(self)

        # First step in creating a scrollable app to account for tasklist
        # growing beyond the height of the app
        self.scrollbar = tk.Scrollbar(self.tasks_canvas, orient="vertical", 
                                      command=self.tasks_canvas.yview)

        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Set title, dimensions
        self.title("J Monnier To-Do App")
        self.geometry("300x400")

        # Create a File menu
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # Add options to the File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Help", command=self.help_message)
        file_menu.add_command(label="Exit", command=self.destroy)
        
        # Create the text input users will use to create new tasks
        self.task_create = tk.Text(self.text_frame, height=3, bg="white", fg="black",
                                   font=self.normal_font)

        # Pack the canvas for tasks, the scrollbar
        self.tasks_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Not actually sure what this one does, it was in tutorial code
        self.canvas_frame = self.tasks_canvas.create_window((0, 0), 
                                                            window=self.tasks_frame, 
                                                            anchor="n")
        
        # Pack task creation input, task frame; focus the task creation widget
        # so users can start typing in there as soon as the app opens
        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        # Create the "how to" initial task, including binding right and left click actions
        todo1 = tk.Label(self.tasks_frame, text="Add Items Below -- Right Click for Options", bg="#ebbcdb",
                         fg="black", pady=10)
        todo1.bind("<Button-3>", self.handle_right_click)
        todo1.bind("<Button-1>", self.toggle_completion)

        # Add the new task to the list of tasks
        self.tasks.append(todo1)

        # Pack the tasks from task list into tasks_frame in order
        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)
        
        # Bind some actions to enable scrolling, auto-resizing, hitting enter to add new task
        self.bind("<Return>", self.add_task)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.tasks_canvas.bind("<Configure>", self.task_width)

        # Set the alternating color scheme options
        self.colour_schemes = [{"bg": "#ebbcdb", "fg": "black"}, {"bg": "#d463ae", "fg": "white"}]

    # Create a popup help message when users select Help from File menu
    def help_message(self):
        msg.showinfo("About ToDo App", self.help_text)
    
    # Method for adding new tasks
    def add_task(self, event=None):

        # Strip leading space/new lines from the task name
        task_text = self.task_create.get(1.0, tk.END).strip()

        # Make sure the task has a name, then add it
        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.set_task_colour(len(self.tasks), new_task)

            new_task.bind("<Button-3>", self.handle_right_click)
            new_task.bind("<Button-1>", self.toggle_completion)
            new_task.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_task)
        
        # Remove text from the task_create input so it's fresh for the user
        self.task_create.delete(1.0, tk.END)
    
    # Create a right click menu for each task & handle choosing each option
    def handle_right_click(self, event):
        
        # Get the index of the clicked task in case they want to reorder it
        task_index = self.tasks.index(event.widget)

        # Create the menu, add commands
        popup_menu = tk.Menu(self.tasks_frame, tearoff=0)
        popup_menu.add_command(label="Toggle Completion", command=lambda: self.toggle_completion(event))
        popup_menu.add_command(label="Remove Task", command=lambda: self.remove_task(event))
        
        # Ensure move up/move down only appear in the menu when appropriate
        if task_index > 0:
            popup_menu.add_command(label="Move Up", command=lambda: self.move_task(task_index, -1))
        if task_index < len(self.tasks)-1:
            popup_menu.add_command(label="Move Down", command=lambda: self.move_task(task_index, 1))
        
        # Control where the menu "spawns"
        popup_menu.tk_popup(event.x_root, event.y_root)
    
    # Function to handle toggling strikethrough/non-strikethrough to represent task completion
    def toggle_completion(self, event):
        task = event.widget
        font_name = task.cget("font")
        font_dict = font.nametofont(font_name).actual()
        if font_dict['overstrike'] == 0:
            task.configure(font=self.strike_font)
        else:
            task.configure(font=self.normal_font)
    
    # Function to handle removing a task, including popup confirmation box
    def remove_task(self, event):
        task = event.widget
        if msg.askyesno("Really Delete?", "Delete '" + task.cget("text") + "'?"):
            self.tasks.remove(event.widget)
            event.widget.destroy()
            self.recolour_tasks()
    
    # Function to handle reordering tasks (move up/move down)
    def move_task(self, task_index, direction):
        
        # Pop the task out of the task list and into a variable
        task = self.tasks.pop(task_index)

        # Insert the task at the appropriate index based on up/down movement
        self.tasks.insert(task_index + direction, task)

        # Recolor the tasks to maintain alternating color
        self.recolour_tasks()
    
    # Function to maintain alternating color scheme for tasks when things change
    def recolour_tasks(self):
        for index, task in enumerate(self.tasks):
            task.pack_forget() # Forget original pack order (needed for reordering)
            task.pack(side=tk.TOP, fill=tk.X) # repack
            self.set_task_colour(index, task) # set color
    
    # Function to set color based on pre-defined color scheme and index modulo 2
    def set_task_colour(self, position, task):
        _, task_style_choice = divmod(position, 2)

        my_scheme_choice = self.colour_schemes[task_style_choice]

        task.configure(bg=my_scheme_choice["bg"])
        task.configure(fg=my_scheme_choice["fg"])

    # Handle auto-resizing if user resizes window
    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
    
    # More auto-resizing
    def task_width(self, event):
        canvas_width = event.width
        self.tasks_canvas.itemconfig(self.canvas_frame, width = canvas_width)
    
    # Handle scrolling
    def mouse_scroll(self, event):
        if event.delta:
            self.tasks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            
            self.tasks_canvas.yview_scroll(move, "units")

# Ensure the app runs when this python script is run directly
if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()