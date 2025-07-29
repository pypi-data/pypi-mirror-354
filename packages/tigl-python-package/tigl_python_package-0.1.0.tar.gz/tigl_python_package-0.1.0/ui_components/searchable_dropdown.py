import tkinter as tk

class SearchableDropdown(tk.Frame):
    def __init__(self, parent, label_text, options, var=None, width=30, font=("Segoe UI", 11), bg="#1e1e1e", fg="#ffffff", **kwargs):
        super().__init__(parent, bg=bg)
        self.var = var or tk.StringVar()
        self.options = options
        self.filtered_options = options.copy()
        self.font = font
        self.bg = bg
        self.fg = fg

        self.label = tk.Label(self, text=label_text, font=font, bg=bg, fg=fg, width=25, anchor="w")
        self.label.grid(row=0, column=0, padx=10, pady=6, sticky="w")

        self.placeholder = f"Select {label_text.replace(':','').strip()}"
        if not self.var.get():
            self.var.set(self.placeholder)

        self.entry = tk.Entry(self, textvariable=self.var, font=font, bg="#2d2d2d", fg=fg, width=width)
        self.entry.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.entry.bind("<KeyRelease>", self.update_listbox)
        self.entry.bind("<Button-1>", self.clear_placeholder)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)

        # scrollbar ---
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.listbox = tk.Listbox(self, font=font, bg="#2d2d2d", fg=fg, width=width, height=6, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(row=1, column=1, padx=10, pady=(0,6), sticky="w")
        self.scrollbar.grid(row=1, column=2, sticky="nsw", pady=(0,6))

        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.grid_remove()
        self.scrollbar.grid_remove()

        self.update_listbox()

    def clear_placeholder(self, event=None):
        self.var.set("")
        self.update_listbox()
        self.listbox.grid()
        self.scrollbar.grid()

    def restore_placeholder(self, event=None):
        # Only restore placeholder if empty or not a valid option
        if not self.var.get() or self.var.get() not in self.options:
            self.var.set(self.placeholder)

    def update_listbox(self, event=None):
        search = self.var.get().lower()
        # Don't filter if placeholder is present
        if self.var.get() == self.placeholder:
            filtered = self.options
        else:
            filtered = [opt for opt in self.options if search in opt.lower()]
        self.filtered_options = filtered
        self.listbox.delete(0, tk.END)
        for opt in self.filtered_options:
            self.listbox.insert(tk.END, opt)
        if self.filtered_options and self.var.get() != self.placeholder:
            self.listbox.grid()
            self.scrollbar.grid()
        else:
            self.listbox.grid_remove()
            self.scrollbar.grid_remove()

    def show_listbox(self, event=None):
        self.update_listbox()
        self.listbox.grid()
        self.scrollbar.grid()

    def on_select(self, event):
        if self.listbox.curselection():
            value = self.filtered_options[self.listbox.curselection()[0]]
            self.var.set(value)
            self.listbox.grid_remove()
            self.scrollbar.grid_remove()