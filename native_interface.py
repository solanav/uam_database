from PIL import ImageTk, Image
import tkinter as tk
import json

USERS_FILE = "users.json"
IMAGE_FOLDER = "images/"
DEFAULT_IMAGE = IMAGE_FOLDER + "f1"

def spaces(str):
    return " " * (10 - len(str))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        def show_image(evt):
            w = evt.widget
            i = int(w.curselection()[0])
            v = w.get(i)[1:]

            try:
                render = ImageTk.PhotoImage(Image.open(IMAGE_FOLDER + v.split("]")[0]))
            except Exception as e:
                print(e)
                render = ImageTk.PhotoImage(Image.open(DEFAULT_IMAGE))
            
            img.configure(image=render)
            img.image = render

        def search():
            name = e1.get().lower()
            surname = e2.get().lower()

            results.delete(0, tk.END)

            with open(USERS_FILE) as user_list:
                data = json.load(user_list)
                sorted_data = sorted(data['users'], key=lambda kv:kv['surname'])
                for result in sorted_data:
                    if (name and surname):
                        if (name in result['name'].lower() and surname in result['surname'].lower()):
                            results.insert(tk.END, "[" + result['id'] + "]" + spaces(result['id']) + result['name'] + " " + ''.join(result['surname']))
                    elif (name and not surname):
                        if (name in result['name'].lower()):
                            results.insert(tk.END, "[" + result['id'] + "]" + spaces(result['id']) + result['name'] + " " + ''.join(result['surname']))
                    elif (not name and surname):
                        if (surname in result['surname'].lower()):
                            results.insert(tk.END, "[" + result['id'] + "]" + spaces(result['id']) + result['name'] + " " + ''.join(result['surname']))

        l1 = tk.Label(self, text="Name:", font='TkFixedFont')
        l2 = tk.Label(self, text="Surname:", font='TkFixedFont')

        l1.grid(row=0, sticky='e')
        l2.grid(row=1, sticky='e')

        e1 = tk.Entry(self)
        e2 = tk.Entry(self)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        b1 = tk.Button(self, text="search", command=search, font='TkFixedFont')
        b1.grid(row=2, column=1, sticky='ew')

        render = ImageTk.PhotoImage(Image.open(DEFAULT_IMAGE))
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=2, rowspan=3, columnspan=1)
        
        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(row=3, column=3, sticky='ns')
        
        scrollbar2 = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar2.grid(row=4, columnspan=3, sticky='ew', )

        results = tk.Listbox(self, yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set, font='TkFixedFont')
        results.bind('<<ListboxSelect>>', show_image)
        results.grid(row=3, columnspan=3, sticky='nsew', ipady=40)

        scrollbar.config(command=results.yview)
        scrollbar2.config(command=results.xview)

def main():
    root = tk.Tk()
    root.title("You fuckin' creep...")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()