import tkinter as tk
import tkinter.messagebox as msg
from tkinter import font

class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks
        
        self.default_font = font.nametofont("TkDefaultFont").actual()
        self.strike_font = font.Font(family=self.default_font["family"], 
                                     size=self.default_font["size"],
                                     overstrike=1)
        self.normal_font = font.Font(family=self.default_font["family"], 
                                     size=self.default_font["size"],
                                     overstrike=0)
        
        self.help_text = """
Left-click a task to toggle completion (strikethrough = complete).
Right-click a task for a menu of options:
    Toggle completion
    Remove from app
    Move up or down"""
        
        self.tasks_canvas = tk.Canvas(self)

        self.tasks_frame = tk.Frame(self.tasks_canvas)
        self.text_frame = tk.Frame(self)

        self.scrollbar = tk.Scrollbar(self.tasks_canvas, orient="vertical", 
                                      command=self.tasks_canvas.yview)

        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title("J Monnier To-Do App")
        self.geometry("300x400")

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Help", command=self.help_message)
        file_menu.add_command(label="Exit", command=self.destroy)
        
        self.task_create = tk.Text(self.text_frame, height=3, bg="white", fg="black",
                                   font=self.normal_font)

        self.tasks_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame = self.tasks_canvas.create_window((0, 0), 
                                                            window=self.tasks_frame, 
                                                            anchor="n")
        
        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        todo1 = tk.Label(self.tasks_frame, text="Add Items Below -- Right Click for Options", bg="#ebbcdb",
                         fg="black", pady=10)
        todo1.bind("<Button-3>", self.handle_right_click)
        todo1.bind("<Button-1>", self.toggle_completion)

        self.tasks.append(todo1)

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)
        
        self.bind("<Return>", self.add_task)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.tasks_canvas.bind("<Configure>", self.task_width)

        self.colour_schemes = [{"bg": "#ebbcdb", "fg": "black"}, {"bg": "#d463ae", "fg": "white"}]

    def help_message(self):
        msg.showinfo("About ToDo App", self.help_text)
    
    def add_task(self, event=None):
        task_text = self.task_create.get(1.0, tk.END).strip()

        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.set_task_colour(len(self.tasks), new_task)

            new_task.bind("<Button-3>", self.handle_right_click)
            new_task.bind("<Button-1>", self.toggle_completion)
            new_task.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_task)
        
        self.task_create.delete(1.0, tk.END)
    
    def handle_right_click(self, event):
        task_index = self.tasks.index(event.widget)
        popup_menu = tk.Menu(self.tasks_frame, tearoff=0)
        popup_menu.add_command(label="Toggle Completion", command=lambda: self.toggle_completion(event))
        popup_menu.add_command(label="Remove Task", command=lambda: self.remove_task(event))
        if task_index > 0:
            popup_menu.add_command(label="Move Up", command=lambda: self.move_task(task_index, -1))
        if task_index < len(self.tasks)-1:
            popup_menu.add_command(label="Move Down", command=lambda: self.move_task(task_index, 1))
        popup_menu.tk_popup(event.x_root, event.y_root)
    
    def toggle_completion(self, event):
        task = event.widget
        font_name = task.cget("font")
        font_dict = font.nametofont(font_name).actual()
        if font_dict['overstrike'] == 0:
            task.configure(font=self.strike_font)
        else:
            task.configure(font=self.normal_font)
    
    def remove_task(self, event):
        task = event.widget
        if msg.askyesno("Really Delete?", "Delete '" + task.cget("text") + "'?"):
            self.tasks.remove(event.widget)
            event.widget.destroy()
            self.recolour_tasks()
    
    def move_task(self, task_index, direction):
        task = self.tasks.pop(task_index)
        self.tasks.insert(task_index + direction, task)
        self.recolour_tasks()
    
    def recolour_tasks(self):
        for index, task in enumerate(self.tasks):
            task.pack_forget()
            task.pack(side=tk.TOP, fill=tk.X)
            self.set_task_colour(index, task)
    
    def set_task_colour(self, position, task):
        _, task_style_choice = divmod(position, 2)

        my_scheme_choice = self.colour_schemes[task_style_choice]

        task.configure(bg=my_scheme_choice["bg"])
        task.configure(fg=my_scheme_choice["fg"])

    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
    
    def task_width(self, event):
        canvas_width = event.width
        self.tasks_canvas.itemconfig(self.canvas_frame, width = canvas_width)
    
    def mouse_scroll(self, event):
        if event.delta:
            self.tasks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            
            self.tasks_canvas.yview_scroll(move, "units")

if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()