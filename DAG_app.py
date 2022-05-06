# declarative answer grader UI
from tkinter import*
from tkinter import ttk
from python_files.classes import *
from python_files.import_export_functions import *
import sys
import re

root = Tk()
root.title("Answer Grader")
root.geometry("900x500")

# Counter for imported IDs
global count
count = 1

global current_frames_p1
current_frames_p1=[]

imported_questions = []
def import_file_mohler_txt():
    global count
    global current_frames_p1
    mohler_imports = import_mohler_txt(count)
    for new_question in mohler_imports:
        imported_questions.append(new_question[0])
        question_tree.insert(parent="", index="end", iid=count, text="",
                             values=(new_question[0].q_id,
                                    new_question[0].q_text,
                                    new_question[1]))
        new_question[0].pre_process_question()
        new_question[0].generate_event_log()
        count +=1
    for frame in current_frames_p1:
        panel_1.forget(frame)
    if len(question_tree.get_children()) > 0:
        panel_1.add(display_frame)
        panel_1.add(question_tree)
        current_frames_p1=[display_frame,question_tree]


# Remove records:
def remove_selected():
    len_children = len(question_tree.get_children())
    selected = question_tree.selection()
    len_selection = len(selected)
    for record in selected:
        q_id = question_tree.item(record)["values"][0]
        question = ""
        for qst in imported_questions:
            if qst.q_id == q_id:
                question = qst
        imported_questions.remove(question)
        question_tree.delete(record)
    if  len_children == len_selection:
        panel_1.forget(question_tree)
        panel_1.forget(display_frame)


# Side-Bar:-------------------------------------
side_frame = Frame(root, width=300)
side_frame.pack(side="left",anchor=W, fill=Y)
#side_frame.grid(row=1,column=1)
space_left = ttk.Label(side_frame, text="")
space_left.grid(row=1,column=1)
space_right = ttk.Label(side_frame, text="")
space_right.grid(row=1,column=3)

# Import/add - Button
import_btn = Button(side_frame, text="Import", command=import_file_mohler_txt)
import_btn.grid(row=3, column=2)



# Main Window:-----------------------------------
main_frame = Frame(root)
main_frame.pack(expand=True,fill="both")

# Panel-Window for main_frame:
panel_1 = PanedWindow(main_frame,bd=1,orient=VERTICAL, bg="black")
panel_1.pack(fill=BOTH,expand=1)

# Display-Frame for displaying data about the selected item:
display_frame = Frame(panel_1)

# Question - Text:
question_label = ttk.Label(display_frame, text="Question: ")
question_label.grid(row=1,column=1,sticky=W)
question_display = ttk.Label(display_frame, text="")
question_display.grid(row=1,column=2,sticky=W)
# Number of Student answers:
number_std_answ_label = ttk.Label(display_frame, text="Student answers: ")
number_std_answ_label.grid(row=2,column=1,sticky=W)
number_std_answ_display = ttk.Label(display_frame, text="")
number_std_answ_display.grid(row=2,column=2,sticky=W)
# Constraints rated "x from all":
cons_label = ttk.Label(display_frame, text="Constraints rated: ")
cons_label.grid(row=3, column=1, sticky=W)
cons_display = ttk.Label(display_frame, text="", foreground="")
cons_display.grid(row=3, column=2, sticky=W)
# Answers graded "y from all":
answ_graded_label = ttk.Label(display_frame, text="Answers graded: ")
answ_graded_label.grid(row=4, column=1, sticky=W)
answ_graded_display = ttk.Label(display_frame, text="", foreground="")
answ_graded_display.grid(row=4, column=2, sticky=W)
#------------------


# Remove selected
remove_selected = Button(display_frame, text="Remove", command=remove_selected)
remove_selected.grid(row=10,column=1, sticky=W)

# Select item in list:
def selectItem_qst(a):
    cur_item = question_tree.focus()
    q_id = question_tree.item(cur_item)["values"][0]
    question = ""
    for qst in imported_questions:
        if qst.q_id == q_id:
            question = qst
    question_display.configure(text=question.q_text)
    number_std_answ_display.configure(text=str(len(question.student_answers)))
    rated_cons = 0
    if len(question.event_log.mined_constraints) == 0:
        cons_display.configure(text = "Please import Constraints", foreground="red")
    else:
        for cons in question.event_log.mined_constraints:
            if cons.essential_for_rightness is not None:
                rated_cons += 1
        max_cons = len(question.event_log.mined_constraints)
        cons_display.configure(text = str(rated_cons) + " from " + str(max_cons),
                               foreground="")

    if rated_cons == 0:
        answ_graded_display.configure(text = "Please rate all Constraints", foreground="red")
    else:
        graded_answ = 0
        for answ in question.student_answers:
            if answ.new_grade is not None:
                graded_answ += 1
        max_answ = len(question.student_answers)
        answ_graded_display.configure(text = str(graded_answ) + " from " + str(max_answ),
                               foreground="")

# Question-Tree:---------------------------------------------------------

question_tree = ttk.Treeview(panel_1)
question_tree["columns"] = ("Q_object","Question", "file")

# Formate columns:
question_tree.column("#0", width=0, stretch=NO)
question_tree.column("Q_object", anchor=W,width=10)
question_tree.column("Question", anchor=W,width=300)
question_tree.column("file",anchor=W,width=300)
# Create headings:
question_tree.heading("#0",text="")
question_tree.heading("Q_object", text="Q_object", anchor=W)
question_tree.heading("Question",text="Question",anchor=W)
question_tree.heading("file", text="file", anchor=W)

question_tree["displaycolumns"] = ("Question", "file")

# on left mouse-button: select item
question_tree.bind('<ButtonRelease-1>', selectItem_qst)


global current_question
current_question = ""

def display_curr_question():
    global current_question
    global current_frames_p1
    for frame in current_frames_p1:
        panel_1.forget(frame)
    qst_disp_answ.configure(text = current_question.q_text)
    panel_1.add(display_frame_answ)
    panel_1.add(button_frame_answ)
    panel_1.add(answ_tree)
    current_frames_p1=[display_frame_answ,button_frame_answ,answ_tree]
    fill_answer_tree(current_question)

def on_double_click_qst(event):
    global current_question
    global current_frames_p1
    cur_item = question_tree.focus()
    q_id = question_tree.item(cur_item)["values"][0]
    for qst in imported_questions:
        if qst.q_id == q_id:
            current_question = qst
    display_curr_question()

question_tree.bind("<Double-1>", on_double_click_qst)


#------------------ANSWER-VIEW-------------------------------------------------
display_frame_answ = Frame(panel_1)
button_frame_answ = Frame(panel_1)

# Question - Text:
qst_lab_answ = ttk.Label(display_frame_answ, text="Question: ")
qst_lab_answ.grid(row=1,column=1,sticky=W)
qst_disp_answ = ttk.Label(display_frame_answ, text="")
qst_disp_answ.grid(row=1,column=2,sticky=W)

# Student-ID:
stud_id_label = ttk.Label(display_frame_answ, text="Student-ID: ")
stud_id_label.grid(row=2,column=1,sticky=W)
stud_id_disp = ttk.Label(display_frame_answ, text="")
stud_id_disp.grid(row=2,column=2,sticky=W)

# Student-Answ:
stud_answ_lab = ttk.Label(display_frame_answ, text="Student-Answer: ")
stud_answ_lab.grid(row=3,column=1,sticky=W)
stud_answ_disp = ttk.Label(display_frame_answ, text="")
stud_answ_disp.grid(row=3,column=2,sticky=W)

#Grade:
grade_label = ttk.Label(display_frame_answ, text="Grade: ")
grade_label.grid(row=4,column=1,sticky=W)
grade_disp = ttk.Label(display_frame_answ, text="")
grade_disp.grid(row=4,column=2,sticky=W)



# ---- Button functions:

def back_to_qst():
    global current_frames_p1
    for frame in current_frames_p1:
        panel_1.forget(frame)
    panel_1.add(display_frame)
    panel_1.add(question_tree)
    current_frames_p1 = [display_frame,question_tree]

def export_event_log_btn():
    global current_question
    orig_file = current_question.original_file_name
    event_log = current_question.event_log
    event_log.export_event_log_xes(original_file_name=orig_file)

def import_declare_btn():
    global current_question
    orig_file = current_question.original_file_name
    event_log = current_question.event_log
    event_log.import_mined_declare(original_file_name=orig_file)
    current_question.check_constraints()

def highlight(field, word, whole_text, color):
    starts = []
    ends = []
    for m in re.finditer(word, whole_text):
        starts.append("1." + str(m.start()))
        ends.append("1." + str(m.start() + len(word)))
    for i in range(len(starts)):
        field.tag_add("here" + starts[i], starts[i], ends[i])
        field.tag_config("here" + starts[i], background=color)

global curr_rated_constraint
curr_rated_constraint = ""

def rate_const():
    global current_question
    global current_frames_p1
    global curr_rated_constraint

    unrated_counter = 0
    unrated_const = []
    for const in current_question.event_log.mined_constraints:
        if const.essential_for_rightness is None:
            unrated_counter +=1
            unrated_const.append(const)
    # Display Question-Detail-View if all constraints are rated:
    if unrated_counter == 0:
        display_curr_question()
    # Display next constraint to rate:
    if unrated_counter != 0:
        for frame in current_frames_p1:
            panel_1.forget(frame)
        panel_1.add(rate_const_frame)
        current_frames_p1 = [rate_const_frame]
        # Fill Labels:
        curr_rated_constraint = unrated_const[0]
        rcfrm_question_disp.configure(text=current_question.q_text)
        const_remain_disp.configure(text=unrated_counter)
        # Get Details about constraint:
        act_a = curr_rated_constraint.activity_a.activity_text
        act_b = curr_rated_constraint.activity_b.activity_text
        const_type = curr_rated_constraint.constraint_type.constraint_type_name
        # Get an example answer for the constraint:
        example_answ = ""
        for answ in current_question.student_answers:
            if curr_rated_constraint in answ.fulfilled_constraints:
                if example_answ == "":
                    example_answ = answ.answer_text
        # Display example answer:
        example_answ_txt.configure(state=NORMAL)
        example_answ_txt.delete("1.0", END)
        example_answ_txt.insert(INSERT,example_answ)
        highlight(field = example_answ_txt, word = act_a,
                  whole_text = example_answ, color = "yellow")
        highlight(field = example_answ_txt, word = act_b,
                  whole_text = example_answ, color = "yellow")
        example_answ_txt.configure(state=DISABLED)
        # Display constraint:
        constr_explanation.configure(text= const_type + "[" + act_a + "," + act_b + "]")



#current_question

def export_csv():
    export_data_const_incl_a_b(question=current_question)

#-----BUttons:
# Export Event-log button
export_event_log = Button(button_frame_answ, text="Export Event-log",
                          command=export_event_log_btn)
export_event_log.grid(row=10,column=1)

# Import DECLARE button:
import_declare = Button(button_frame_answ, text="Import DECLARE",
                        command=import_declare_btn)
import_declare.grid(row=10,column=2)

#Rate Constraints button:
rate_const_btn = Button(button_frame_answ, text="Rate Constraints",
                        command=rate_const)
rate_const_btn.grid(row=10,column=3)

#Export to .csv:
export_csv_btn = Button(button_frame_answ, text="Export .csv",
                        command=export_csv)
export_csv_btn.grid(row=10,column=5)

# Back-to question overview:
back_btn = Button(button_frame_answ, text="<-", command=back_to_qst)
back_btn.grid(row=10,column=6)




# ------functions for Answer Tree----------
def fill_answer_tree(current_question):
    for item in answ_tree.get_children():
        answ_tree.delete(item)
    for answ in current_question.student_answers:
        answ_tree.insert(parent="", index="end", text="",
                        values=(answ.student_id,
                                answ.answer_text,
                                answ.new_grade,
                                answ.grade))

def selectItem_answ(event):
    curItem = answ_tree.focus()
    student_id = answ_tree.item(curItem)["values"][0]
    curr_student = ""
    for qst in imported_questions:
        for stud in qst.student_answers:
            if str(stud.student_id) == str(student_id):
                curr_student = stud
    stud_id_disp.configure(text=curr_student.student_id)
    stud_answ_disp.configure(text=curr_student.answer_text)
    grade_disp.configure(text=curr_student.new_grade)
    if curr_student.new_grade is None:
        grade_disp.configure(text="")


#------Answer Tree-------------
answ_tree = ttk.Treeview(panel_1)
answ_tree["columns"] = ("Student-ID","Answer", "Grade", "Mohler_Grade")

# Formate columns:
answ_tree.column("#0", width=0, stretch=NO)
answ_tree.column("Student-ID", anchor=W,width=10)
answ_tree.column("Answer", anchor=W,width=300)
answ_tree.column("Grade",anchor=W,width=10)
answ_tree.column("Mohler_Grade",anchor=W,width=10)

# Create headings:
answ_tree.heading("#0",text="")
answ_tree.heading("Student-ID", text="Student-ID", anchor=W)
answ_tree.heading("Answer",text="Answer",anchor=W)
answ_tree.heading("Grade", text="Grade", anchor=W)
answ_tree.heading("Mohler_Grade", text="Mohler-Grade", anchor=W)


# on left mouse-button: select item
answ_tree.bind('<ButtonRelease-1>', selectItem_answ)


#---------RATE CONSTRAINTS-----------------------------

rate_const_frame = Frame(panel_1)

# Question - Text
rcfrm_question_lab = ttk.Label(rate_const_frame, text="Question: ")
rcfrm_question_lab.grid(row=1,column=1,sticky=W)
rcfrm_question_disp = ttk.Label(rate_const_frame, text="")
rcfrm_question_disp.grid(row=1,column=2,sticky=W)

# Unrated constraints counter:
const_remain_lab = ttk.Label(rate_const_frame, text="Unrated Constraints: ")
const_remain_lab.grid(row=2,column=1,sticky=W)
const_remain_disp = ttk.Label(rate_const_frame, text="")
const_remain_disp.grid(row=2,column=2,sticky=W)

# Example answer:
# Label "Example: "
exmple_answ_lab = ttk.Label(rate_const_frame, text="Example: ")
exmple_answ_lab.grid(row=3,column=1,sticky=W)

# Frame for Text field:
example_answ_frm = Frame(rate_const_frame,height=100,width=170)
example_answ_frm.grid(row=3,column=2,sticky=W)
example_answ_frm.grid_propagate(False)

# Text field for example answer:
exmple_txt_height = 5
exmple_txt_width = 70
example_answ_txt = Text(example_answ_frm, height=exmple_txt_height,
                        width=exmple_txt_width, wrap ="word")
example_answ_txt.pack(side=LEFT)
example_answ_txt.configure(state=DISABLED)

# Constraint explanation:
constr_explanation = ttk.Label(rate_const_frame, text="")
constr_explanation.grid(row=4,column=2,sticky=W)



# Rating Buttons:---------
# button functions:
def rate_importance(yesno):
    global curr_rated_constraint
    if yesno == "yes":
        curr_rated_constraint.essential_for_rightness = True
    if yesno == "no":
        curr_rated_constraint.essential_for_rightness = False
    rate_const()

# Important-Yes function
def rate_imp_yes():
    rate_importance("yes")

# Important-No function
def rate_imp_no():
    rate_importance("no")

# Important-Yes Button
imp_yes_btn = Button(rate_const_frame, text="Important", command=rate_imp_yes)
imp_yes_btn.grid(row=10,column=1)

# Important - No Button
imp_no_btn = Button(rate_const_frame, text="Not important", command=rate_imp_no)
imp_no_btn.grid(row=10,column=2)





#----------- Grade Answers------------------------------
grading_frame = Frame(panel_1)

# Question - Text
grading_qst_lab = ttk.Label(grading_frame, text="Question: ")
grading_qst_lab.grid(row=1,column=1,sticky=W)
grading_qst_disp = ttk.Label(grading_frame, text="")
grading_qst_disp.grid(row=1,column=2,sticky=W)

# Student-Answer
grading_answ_lab = ttk.Label(grading_frame, text="Answer: ")
grading_answ_lab.grid(row=2,column=1,sticky=W)

# Frame for Text field:
grading_answ_frm = Frame(grading_frame,height=100,width=170)
grading_answ_frm.grid(row=2,column=2,sticky=W)
grading_answ_frm.grid_propagate(False)

# Text field for answer to grade:
grading_txt_height = 5
grading_txt_width = 70
grading_answ_txt = Text(grading_answ_frm, height=grading_txt_height,
                        width=grading_txt_width, wrap ="word")
grading_answ_txt.pack(side=LEFT)
grading_answ_txt.configure(state=DISABLED)

# Number of important constraints (X from ALL):
grading_imp_const_lab = ttk.Label(grading_frame, text="Important Constraints: ")
grading_imp_const_lab.grid(row=3,column=1,sticky=W)
grading_imp_const_disp = ttk.Label(grading_frame, text="")
grading_imp_const_disp.grid(row=3,column=2,sticky=W)

# Entry field: Grade
grading_box = Entry(grading_frame)
grading_box.grid(row=4,column=1)


global curr_grading_answer
curr_grading_answer = ""

def curr_qst_imp_constr():
    global current_question
    important_constr = []
    for constr in current_question.event_log.mined_constraints:
        if constr.essential_for_rightness is True:
            important_constr.append(constr)
    return important_constr

def curr_answ_imp_constr():
    global current_question
    global curr_grading_answer
    all_constr = curr_qst_imp_constr()
    important_answ_constr = []
    for constr in curr_grading_answer.fulfilled_constraints:
        proc_txt = curr_grading_answer.pre_processed_answer_text
        act_a = constr.activity_a.activity_text
        act_b = constr.activity_b.activity_text
        if act_a in proc_txt and act_b in proc_txt:
            if constr in all_constr:
                important_answ_constr.append(constr)
    return important_answ_constr

def grading():
    global current_question
    global current_frames_p1
    global curr_grading_answer
    # Get all answers that dont have a grade:
    ungraded_counter = 0
    ungraded_answ = []
    for answ in current_question.student_answers:
        if answ.new_grade is None:
            ungraded_counter +=1
            ungraded_answ.append(answ)
    # Display Question-Detail-View if all answers are graded:
    if ungraded_counter == 0:
        display_curr_question()
    # Display next answer to grade:
    if ungraded_counter != 0:
        for frame in current_frames_p1:
            panel_1.forget(frame)
        panel_1.add(grading_frame)
        current_frames_p1 = [grading_frame]
        curr_grading_answer = ungraded_answ[0]
        grading_qst_disp.configure(text=current_question.q_text)
        # Display Student-Answer:
        answ_txt = curr_grading_answer.answer_text
        imp_constr = curr_answ_imp_constr()

        grading_answ_txt.configure(state=NORMAL)
        grading_answ_txt.delete("1.0", END)
        grading_answ_txt.insert(INSERT,answ_txt)

        for const in imp_constr:
            act_a = const.activity_a.activity_text
            act_b = const.activity_b.activity_text
            highlight(field = grading_answ_txt, word = act_a,
                      whole_text = answ_txt, color = "green")
            highlight(field = grading_answ_txt, word = act_b,
                      whole_text = answ_txt, color = "green")
        grading_answ_txt.configure(state=DISABLED)

        imp_constr = len(curr_qst_imp_constr())
        imp_answ_constr = len(curr_answ_imp_constr())
        grading_imp_const_disp.configure(text= str(imp_answ_constr) + " from " + str(imp_constr))

def grade_curr_answ(a=None):
    global curr_grading_answer
    grade = grading_box.get()
    curr_grading_answer.new_grade = grade
    grading_box.delete(0,"end")
    grading()


# "grade" button
add_record = Button(grading_frame, text="grade", command=grade_curr_answ)
add_record.grid(row=4,column=2, sticky=W)
root.bind("<Return>", grade_curr_answ)

# Grade Answers button:
grade_answ_btn = Button(button_frame_answ, text="Grade Answers", command=grading)
grade_answ_btn.grid(row=10,column=4)

# Side Panel: Menu button
main = Button(side_frame, text="Main_view", command=back_to_qst)
main.grid(row=2, column=2)





root.mainloop()
