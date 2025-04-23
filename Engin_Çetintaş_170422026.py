import tkinter as tk
from tkinter import messagebox


class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kişiye Göre Görev Yöneticisi")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frame = tk.Frame(self)
        self.frame.pack(padx=20, pady=20)

        self.create_widgets()

        self.people_tasks = {}

    def create_widgets(self):
        label_num_people = tk.Label(self.frame, text="Kişi Sayısı:", font=("Arial", 12))
        label_num_people.grid(row=0, column=0, padx=5, pady=5)

        self.num_people_entry = tk.Entry(self.frame, width=5, font=("Arial", 12))
        self.num_people_entry.grid(row=0, column=1, padx=5, pady=5)

        num_people_button = tk.Button(self.frame, text="Onayla", command=self.get_people_list, font=("Arial", 12))
        num_people_button.grid(row=0, column=2, padx=5, pady=5)

        self.person_entries = []
        self.task_entries = []

    def get_people_list(self):
        num_people = self.num_people_entry.get()

        if not num_people:
           # messagebox.showerror("Hata", "Burası boş bırakılamaz!")
            return

        num_people = int(num_people)

        for widget in self.frame.winfo_children():
            widget.destroy()
        self.person_entries.clear()
        self.task_entries.clear()

        for i in range(num_people):
            self.create_person_task_entries(i)

        add_for_all_button = tk.Button(self.frame, text="Herkese Ekle", command=self.add_task_for_all,
                                       font=("Arial", 12))
        add_for_all_button.grid(row=num_people + 2, column=1, columnspan=2, padx=5, pady=5)

        self.selected_person = tk.StringVar(self)
        self.selected_person.set("")
        self.listbox = tk.Listbox(self.frame, width=40, height=10, font=("Arial", 12))
        self.listbox.grid(row=num_people + 3, columnspan=4, pady=10)

        delete_button = tk.Button(self.frame, text="Sil", command=self.delete_task, font=("Arial", 12))
        delete_button.grid(row=num_people + 4, column=1, padx=5, pady=5)

        complete_button = tk.Button(self.frame, text="Tamamla", command=self.complete_task, font=("Arial", 12))
        complete_button.grid(row=num_people + 4, column=2, padx=5, pady=5)

        clear_button = tk.Button(self.frame, text="Listeyi Temizle", command=self.clear_list, font=("Arial", 12))
        clear_button.grid(row=num_people + 5, columnspan=2, padx=5, pady=5)

        self.load_tasks_from_file()
        self.update_listbox()

    def create_person_task_entries(self, i):
        label_person = tk.Label(self.frame, text=f"Kişi {i + 1} İsmi:", font=("Arial", 12))
        label_person.grid(row=i + 1, column=0, padx=5, pady=5)

        entry_person = tk.Entry(self.frame, width=20, font=("Arial", 12))
        entry_person.grid(row=i + 1, column=1, padx=5, pady=5)
        self.person_entries.append(entry_person)

        label_task = tk.Label(self.frame, text=f"Kişi {i + 1} Görevi:", font=("Arial", 12))
        label_task.grid(row=i + 1, column=2, padx=5, pady=5)

        entry_task = tk.Entry(self.frame, width=20, font=("Arial", 12))
        entry_task.grid(row=i + 1, column=3, padx=5, pady=5)
        self.task_entries.append(entry_task)

    # ...

    def add_task_for_all(self):
        for i, person_entry in enumerate(self.person_entries):
            person = person_entry.get()
            task = self.task_entries[i].get()
            if person and task:
                if person in self.people_tasks:
                    self.people_tasks[person].append(task)
                else:
                    self.people_tasks[person] = [task]
            elif not person and task:
                # messagebox.showerror("Hata", f"Burası boş bırakılamaz!")
                return
            elif person and not task:
                # messagebox.showerror("Hata", f"Burası boş bırakılamaz!")
                return
        self.update_listbox()

    def delete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_task = self.listbox.get(selected_index)
            if selected_task.endswith("- Tamamlandı"):
                # messagebox.showwarning("Uyarı", "Tamamlanmış görevleri silemezsiniz.")
                pass
            else:
                for person, tasks in self.people_tasks.items():
                    if selected_task in tasks:
                        tasks.remove(selected_task)
                self.update_listbox()

    # ...

    def complete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_task = self.listbox.get(selected_index)
            if not selected_task.endswith("- Tamamlandı"):
                for person, tasks in self.people_tasks.items():
                    if selected_task in tasks:
                        task_index = tasks.index(selected_task)
                        tasks[task_index] += " - Tamamlandı"
                self.update_listbox()

    def clear_list(self):
        self.save_tasks_to_file()
        self.people_tasks = {}
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for person, tasks in self.people_tasks.items():
            self.listbox.insert(tk.END, f"{person}'s Tasks:")
            for task in tasks:
                self.listbox.insert(tk.END, task)
                if task.endswith("- Tamamlandı"):
                    self.listbox.itemconfig(tk.END, {'bg': 'lightgrey'})
            self.listbox.insert(tk.END, "")

    def save_tasks_to_file(self):
        with open("tasks.txt", "w") as file:
            for person, tasks in self.people_tasks.items():
                file.write(f"{person}:\n")
                for task in tasks:
                    file.write(f"{task}\n")
                file.write("\n")

    def load_tasks_from_file(self):
        try:
            with open("tasks.txt", "r") as file:
                person = ""
                for line in file:
                    line = line.strip()
                    if line.endswith(":"):
                        person = line[:-1]
                        self.people_tasks[person] = []
                    elif line and person:
                        self.people_tasks[person].append(line)
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_tasks_to_file()
        self.destroy()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
