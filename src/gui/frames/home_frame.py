from tkinter import ttk

class HomeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")

        labels = [
            "№",
            "Дата",
            "ФИО пациента",
            "Дата рождения",
            "Адрес",
            "Диагноз",
            "МКБ-10",
            "Код ЦАХ",
            "Врач",
            "Мед. сестра",
            "Когда закончен"
        ]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            entry = ttk.Entry(self, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            self.entries[label_text] = entry

        ttk.Button(self, text="Сохранить", command=self.on_save).grid(row=len(labels), column=0, pady=10)
        ttk.Button(self, text="Выход", command=self.quit_app).grid(row=len(labels) + 1, column=1, pady=10)
    
    def on_save(self):
        pass

    def quit_app(self):
        self.winfo_toplevel().destroy()

