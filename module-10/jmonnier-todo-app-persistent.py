import tkinter as tk
import tkinter.messagebox as msg
from tkinter import font
import os
import sqlite3

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

        self.colour_schemes = [{"bg": "#ebbcdb", "fg": "black"}, {"bg": "#d463ae", "fg": "white"}]

        current_tasks = self.load_tasks()
        for task in current_tasks:
            task_text = task[0]
            complete = task[1]
            self.add_task(None, task_text, complete, True)

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)
        
        self.bind("<Return>", self.add_task)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.tasks_canvas.bind("<Configure>", self.task_width)

    def help_message(self):
        msg.showinfo("About ToDo App", self.help_text)
    
    def add_task(self, event=None, task_text=None, complete=0, from_db=False):
        if not task_text:
            task_text = self.task_create.get(1.0, tk.END).strip()

        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.set_task_colour(len(self.tasks), new_task)
            if complete:
                new_task.configure(font=self.strike_font)

            new_task.bind("<Button-3>", self.handle_right_click)
            new_task.bind("<Button-1>", self.toggle_completion)
            new_task.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_task)

            if not from_db:
                self.save_task(task_text, complete)
        
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
            self.update_db(task.cget("text"), 1)
        else:
            task.configure(font=self.normal_font)
            self.update_db(task.cget("text"), 0)
    
    def remove_task(self, event):
        task = event.widget
        if msg.askyesno("Really Delete?", "Delete '" + task.cget("text") + "'?"):
            self.tasks.remove(event.widget)
            
            delete_task_query = "DELETE FROM tasks WHERE task=?"
            delete_task_data = (task.cget("text"),)
            self.runQuery(delete_task_query, delete_task_data)
            
            event.widget.destroy()
            self.recolour_tasks()
    
    def move_task(self, task_index, direction):
        task = self.tasks.pop(task_index)
        self.tasks.insert(task_index + direction, task)
        self.recolour_tasks()
        self.reorder_database()
    
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
    
    def reorder_database(self):
        delete_task_query = "DELETE FROM tasks"
        self.runQuery(delete_task_query)

        readd_tasks_query = "INSERT INTO tasks VALUES (?,?)"
        sqltuples = []
        for task in self.tasks:
            font_name = task.cget("font")
            font_dict = font.nametofont(font_name).actual()
            complete = font_dict["overstrike"]
            task_text = task.cget("text")
            sqltuples.append((task_text, complete))
        self.runQuery(readd_tasks_query, sqltuples)
    
    def save_task(self, task, complete):
        insert_task_query = "INSERT INTO tasks VALUES (?,?)"
        insert_task_data = (task, complete)
        self.runQuery(insert_task_query, insert_task_data)
    
    def load_tasks(self):
        load_tasks_query = "SELECT task, complete FROM tasks"
        my_tasks = self.runQuery(load_tasks_query, receive=True)

        return my_tasks
    
    def update_db(self, task_text, complete):
        update_task_query = "UPDATE tasks SET complete = ? WHERE task = ?"
        update_task_data = (complete, task_text)
        self.runQuery(update_task_query, update_task_data)
    
    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        if data:
            if isinstance(data, list):
                cursor.executemany(sql, data)
            else:
                cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        
        if receive:
            return cursor.fetchall()
        else:
            conn.commit()
        
        conn.close()
    
    @staticmethod
    def firstTimeDB():
        create_tables = "CREATE TABLE tasks (task TEXT, complete INTEGER)"
        Todo.runQuery(create_tables)

        default_task_query = "INSERT INTO tasks VALUES (?,?)"
        default_task_data = ("Add Items Below -- Right Click for Options", 0)
        Todo.runQuery(default_task_query, default_task_data)

if __name__ == "__main__":
    working_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(working_dir)
    if not os.path.isfile("tasks.db"):
        Todo.firstTimeDB()
    todo = Todo()
    todo.mainloop()