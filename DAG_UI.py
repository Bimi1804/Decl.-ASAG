# declarative answer grader UI
from tkinter import*
from tkinter import ttk
from python_files.classes import *
from python_files.import_export_functions import *

root = Tk()
root.title("Answer Grader")
root.geometry("500x500")

imported_questions = []
def import_file_mohler_txt():
    global count
    mohler_imports = import_mohler_txt(count)
    for new_question in mohler_imports:
        imported_questions.append(new_question[0])
        question_tree.insert(parent="", index="end", iid=count, text="",
                             values=(new_question[0].q_text, new_question[1]))
        count +=1

# Remove records:
def remove_selected():
    x = question_tree.selection()
    for record in x:
        question_tree.delete(record)


# Import/add
add_question = Button(root, text="Import", command=import_file_mohler_txt)
add_question.pack(pady=20)


# Define Tree:
question_tree = ttk.Treeview(root)
question_tree["columns"] = ("Question", "file")

# Formate columns:
question_tree.column("#0", width=0, stretch=NO)
question_tree.column("Question", anchor=W,width=300)
question_tree.column("file",anchor=W,width=300)
# Create headings:
question_tree.heading("#0",text="")
question_tree.heading("Question",text="Question",anchor=W)
question_tree.heading("file", text="file", anchor=W)

question_tree.pack(pady=20)

global count
count = 1

# Remove selected
remove_selected = Button(root, text="Remove", command=remove_selected)
remove_selected.pack(pady=10)

# Select item in list:
def selectItem(a):
    curItem = question_tree.focus()
    #print (question_tree.item(curItem)["values"][0])
    label.configure(text=question_tree.item(curItem)["values"][0])

# on left mouse-button: select item
question_tree.bind('<ButtonRelease-1>', selectItem)

# The label that show the question text when selecting an item
label = ttk.Label(root, text="")
label.pack(pady=10)


def show_widget():
    question_tree.pack()
    b1.configure(text="Hide", command=hide_widget)
def hide_widget():
    question_tree.pack_forget()
    b1.configure(text="Show", command=show_widget)

b1 = ttk.Button(root, text="Hide", command=hide_widget)
b1.pack(pady=20)



root.mainloop()
