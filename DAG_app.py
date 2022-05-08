# declarative answer grader UI

# Import tkinter:
from tkinter import*
from tkinter import ttk

# Import other answer_grading files:
from python_files.classes import *
from python_files.import_export_functions import *

# import additional tools:
import sys
import re


#TKinter Window:
root = Tk()
root.title("Answer Grader")
root.geometry("900x500")




############################## GLOBAL VARIABLES #############################

# variables:
global count # Counter for imported IDs
global current_frames_p1 # current frames that are displayed in the main window
global imported_questions # List for objects of imported questions
global current_question # question that is displayed in Detail-View
global curr_rated_constraint # current constraint to rate
global curr_grading_answer # current answer to grade

# initial values:
count = 1 # Start counting at 1
current_frames_p1 = [] # List
imported_questions = [] # List
current_question = ""
curr_rated_constraint = ""
curr_grading_answer = ""




################################## FUNCTIONS #################################

# Import/Export functions:----------------------------------------------------

# Import raw Mohler2009 data:
def import_file_mohler_txt():
    """
    (1) Import one or multiple questions from Mohler2009 with
        import_mohler_txt() from import_export_functions.py to import.

    (2) NLP pre-process for all questions/answers with pre_process_question()
        from classes.py

    (3) generate event-log objects with generate_event_log() from classes.py
    """
    # Global variables used:
    global count
    global current_frames_p1
    global imported_questions
    # Use the import function and give each question an ID with count:
    mohler_imports = import_mohler_txt(count)
    # append the imported questions to the imported_questions list and insert
    # them into the question_tree:
    for new_question in mohler_imports:
        imported_questions.append(new_question[0])
        question_tree.insert(parent="", index="end", iid=count, text="",
                             values=(new_question[0].q_id,
                                    new_question[0].q_text,
                                    new_question[1]))
        # pre-process the imported question and generate an event-log object
        # for the question:
        new_question[0].pre_process_question()
        new_question[0].generate_event_log()
        # Increment count by 1
        count +=1
        # NOTE: the import_mohler_txt() function also has an own counter for
        # the question IDs it imports. The global count variable has to be
        # incremented here for each question, to catch up with the internal
        # counter of the import_mohler_txt() function.

    # Frame-Handling: Display the QUESTION-OVERVIEW after importing:
    for frame in current_frames_p1:
        panel_1.forget(frame)
    if len(question_tree.get_children()) > 0:
        panel_1.add(display_frame)
        panel_1.add(question_tree)
        current_frames_p1=[display_frame,question_tree]

# Export event log as .xes for current question
def export_event_log_btn():
    """
    Export the event log of the current question.

    Uses the export_event_log() function.
    """
    # global variables used:
    global current_question
    orig_file = current_question.original_file_name # file name of current qst
    event_log = current_question.event_log # event-log object of current qst
    event_log.export_event_log_xes(original_file_name=orig_file)

# Import DECLARE file for current question
def import_declare_btn():
    """
    Import a DECLARE file for the current question and check constraints of the
    student answers.

    Uses import_mined_declare() function.
    """
    # global variables used:
    global current_question
    orig_file = current_question.original_file_name # file name of current qst
    event_log = current_question.event_log # event-log object of current qst
    # Import the DECLARE file:
    event_log.import_mined_declare(original_file_name=orig_file)
    # Check which constraints each student-answer fulfills:
    current_question.check_constraints()

# Export analysis as .csv for current question:
def export_csv():
    """
    Export a .csv for the current_question with export_data_const_incl_a_b()
    function.
    """
    export_data_const_incl_a_b(question=current_question)


# Constraint rating functions:------------------------------------------------

# Rate Constraints:
def rate_const():
    """
    Rate the constraints of a question.
    """
    # global variables used:
    global current_question
    global current_frames_p1
    global curr_rated_constraint
    unrated_counter = 0 # Counter for all unrated constraints.
    unrated_const = [] # List of all unrated constraints.
    # Get all unrated constraints of a question:
    for const in current_question.event_log.mined_constraints:
        if const.essential_for_rightness is None:
            unrated_counter +=1
            unrated_const.append(const)
    # Display Question-Detail-View if all constraints are rated:
    if unrated_counter == 0:
        display_curr_question()
    # Display next constraint to rate if there are unrated constraints:
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
        # Display example answer with highlights:
        example_answ_txt.configure(state=NORMAL)
        example_answ_txt.delete("1.0", END)
        example_answ_txt.insert(INSERT,example_answ)
        highlight(field = example_answ_txt, word = act_a,
                  whole_text = example_answ, color = "yellow")
        highlight(field = example_answ_txt, word = act_b,
                  whole_text = example_answ, color = "yellow")
        example_answ_txt.configure(state=DISABLED)
        # Display constraint:
        constr_explanation.configure(text=const_type+"["+act_a+","+act_b+"]")

# Rate importance of current constraint:
def rate_importance(yesno):
    """
    Rate the importance of the current constraint to be rated.

    Parameters
    ----------
    yesno : str
        Defines it the constraint is important or not.
        "yes" -> True
        "no" -> False
    """
    global curr_rated_constraint
    if yesno == "yes":
        curr_rated_constraint.essential_for_rightness = True
    if yesno == "no":
        curr_rated_constraint.essential_for_rightness = False
    # Use the rate_const() function to display the next constraint:
    rate_const()

# Important-Yes function
def rate_imp_yes():
    """
    Calls the rate_importance(yesno) function with "yes".
    """
    rate_importance("yes")

# Important-No function
def rate_imp_no():
    """
    Calls the rate_importance(yesno) function with "no".
    """
    rate_importance("no")


# Answer grading functions:---------------------------------------------------

# Answer grading view:
def grading():
    """
    Grade the answers of a question.
    """
    # Global variables used:
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
        # Enable the modification of the text-field, clear it, and insert the
        # current student answer to grade:
        grading_answ_txt.configure(state=NORMAL)
        grading_answ_txt.delete("1.0", END)
        grading_answ_txt.insert(INSERT,answ_txt)
        # Highlight A and B of the constraints in the student answer:
        for const in imp_constr:
            act_a = const.activity_a.activity_text
            act_b = const.activity_b.activity_text
            highlight(field = grading_answ_txt, word = act_a,
                      whole_text = answ_txt, color = "green")
            highlight(field = grading_answ_txt, word = act_b,
                      whole_text = answ_txt, color = "green")
        # Disable the modification of the text-field:
        grading_answ_txt.configure(state=DISABLED)
        # Display how many important constraints are fulfilled by the answer:
        imp_constr = len(curr_qst_imp_constr())
        imp_answ_constr = len(curr_answ_imp_constr())
        grading_imp_const_disp.configure(text=str(imp_answ_constr)+" from "+str(imp_constr))

# grade the current answer:
def grade_curr_answ(event):
    """
    Store the entered grade in the Student-answer object.
    """
    # Global variables used:
    global curr_grading_answer
    # Get the user input from the grading_box:
    grade = grading_box.get()
    # Save the entered grade in the student-answer object:
    curr_grading_answer.new_grade = grade
    # Clear the entry-field:
    grading_box.delete(0,"end")
    # Display the next answer to grade:
    grading()


# Question-Tree View functions:-----------------------------------------------

# Remove selected questions in QUESTION-OVERVIEW:
def remove_selected():
    """
    Remove the currently selected question from tree and imported questions.
    If question tree is empty: hide the tree and the display frame.
    """
    # Global variables used:
    global imported_questions
    # Remove the selected record from the question_tree and from the
    # imported_questions list.
    for record in question_tree.selection():
        # get the question-ID from a record:
        q_id = question_tree.item(record)["values"][0]
        question = ""
        # Find the question-object that has the same question-ID as the record:
        for qst in imported_questions:
            if qst.q_id == q_id:
                question = qst
        # remove the question object and the record:
        imported_questions.remove(question)
        question_tree.delete(record)
    # Frame-Handling: If question-tree is empty after removing
    #                 -> then hide the question-tree and the question-display.
    if len(question_tree.get_children()) < 1:
        panel_1.forget(question_tree)
        panel_1.forget(display_frame)

# Display Data about selected question in QUESTION-OVERVIEW:
def selectItem_qst(event):
    """
    Display data about the selected item in the question tree.
    """
    # Global variables used:
    global imported_questions
    # Variables for the selected item in the tree:
    cur_item = question_tree.focus()
    q_id = question_tree.item(cur_item)["values"][0]
    # Find the question-object that belongs to the item in the tree:
    question = ""
    for qst in imported_questions:
        if qst.q_id == q_id:
            question = qst
    # Display Question-Text and the number of student answers:
    question_display.configure(text=question.q_text)
    number_std_answ_display.configure(text=str(len(question.student_answers)))
    # Display the Number of rated Constraints as "X from ..."
    # If there are no discovered/mined constraints -> Display Info that
    # constraint sould be imported.
    rated_cons = 0 # Counter for the rated constraints
    if len(question.event_log.mined_constraints) == 0:
        cons_display.configure(text = "Please import Constraints",
                                foreground="red")
    else:
        for cons in question.event_log.mined_constraints:
            if cons.essential_for_rightness is not None:
                rated_cons += 1
        max_cons = len(question.event_log.mined_constraints)
        cons_display.configure(text=str(rated_cons) + " from " + str(max_cons),
                               foreground="")
    # Display the number of graded answers as "X from ..."
    # If no constraints are rated -> Display Info that constraints should be
    # rated.
    if rated_cons == 0:
        answ_graded_display.configure(text = "Please rate all Constraints",
                                        foreground="red")
    else:
        graded_answ = 0
        for answ in question.student_answers:
            if answ.new_grade is not None:
                graded_answ += 1
        max_answ = len(question.student_answers)
        answ_graded_display.configure(text=str(graded_answ)+" from "+str(max_answ),
                                        foreground="")

# On double click: Open selected question in DETAIL-View
def on_double_click_qst(event):
    """
    Displays the Detail-View of a question item that is double-cicked in the
    question-tree.

    Uses the display_curr_question() function to display the question.
    """
    # Global variables used:
    global current_question
    global imported_questions
    cur_item = question_tree.focus()
    q_id = question_tree.item(cur_item)["values"][0]
    for qst in imported_questions:
        if qst.q_id == q_id:
            current_question = qst
    display_curr_question()


# Answer-Tree View functions:-------------------------------------------------

# Display Question in DETAIL-VIEW
def display_curr_question():
    """
    Displays the Detail-View and answer-tree for the current_question var.

    Uses fill_answer_tree(current_question) to fill the answer tree.
    """
    # Global variables used:
    global current_question
    global current_frames_p1
    # forget every currently diplayed frame in the main-window:
    for frame in current_frames_p1:
        panel_1.forget(frame)
    # Add detail-view frames:
    panel_1.add(display_frame_answ)
    panel_1.add(button_frame_answ)
    panel_1.add(answ_tree)
    # Display the question-text of the current_question:
    qst_disp_answ.configure(text = current_question.q_text)
    # Save current-frames:
    current_frames_p1=[display_frame_answ,button_frame_answ,answ_tree]
    # Fill the answer tree:
    fill_answer_tree()

# Fill answer tree with answers from current_question:
def fill_answer_tree():
    """
    Fill the answer tree with the student answers of the current_question.
    """
    # Global variables used:
    global current_question
    # Remove all items that are currently in the answer-tree
    # NOTE: These could be answers from a previously selected question.
    for item in answ_tree.get_children():
        answ_tree.delete(item)
    # Fill the answer tree with the student-answers of the current_question.
    for answ in current_question.student_answers:
        answ_tree.insert(parent="", index="end", text="",
                        values=(answ.student_id, answ.answer_text,
                                answ.new_grade, answ.grade))

# Show Data from selected answer:
def selectItem_answ(event):
    """
    Display information about the currently selected answer.
    """
    # global variables used:
    global imported_questions
    # Store selected item:
    curItem = answ_tree.focus()
    student_id = answ_tree.item(curItem)["values"][0]
    # Find the student-answer object that belongs to the currently selected
    # answer in the answer-tree:
    curr_student = ""
    for qst in imported_questions:
        for stud in qst.student_answers:
            if str(stud.student_id) == str(student_id):
                curr_student = stud
    # Display information about the currently selected answer:
    stud_id_disp.configure(text=curr_student.student_id)
    stud_answ_disp.configure(text=curr_student.answer_text)
    grade_disp.configure(text=curr_student.new_grade)
    if curr_student.new_grade is None:
        grade_disp.configure(text="")

# Back to QUESTION-VIEW:
def back_to_qst():
    """
    Displays the QUESTION-OVERVIEW.
    """
    # Global variables used:
    global current_frames_p1
    # Forget current frames:
    for frame in current_frames_p1:
        panel_1.forget(frame)
    # Add the question-tree and the overview display:
    panel_1.add(display_frame)
    panel_1.add(question_tree)
    # Add current displays to current_frames_p1:
    current_frames_p1 = [display_frame,question_tree]


# Additional functions:-------------------------------------------------------

# Highlight words in text:
def highlight(field, word, whole_text, color):
    """
    Highlight words in a text-field in a specific background color.

    Parameters
    ----------
    field : TK.TEXT
        The tk text-field in which words should be highlighted.
    word : str
        The word that should be highlighted.
    whole_text : str
        The whole text that is in the text field.
    color : str
        The background color for the highlighting.
    """
    starts = []
    ends = []
    # Find all start- and end- indexes for all occurences of the given word
    # in the whole text:
    for m in re.finditer(word, whole_text):
        starts.append("1." + str(m.start()))
        ends.append("1." + str(m.start() + len(word)))
    # Create the highlight-tags for each occurence of the given word in the
    # whole text:
    for i in range(len(starts)):
        field.tag_add("here" + starts[i], starts[i], ends[i])
        field.tag_config("here" + starts[i], background=color)

# All important constraints of the current question:
def curr_qst_imp_constr():
    """
    Finds all constraints of the current_question that are rated as important.

    Returns
    -------
    important_constr : Constraint[0..*]
        List of all Constraint-objects of the current-question that are rated
        as important.
    """
    # Global variables used:
    global current_question
    # Find all important constraints of the current-question and return them
    # as a list of objects:
    important_constr = []
    for constr in current_question.event_log.mined_constraints:
        if constr.essential_for_rightness is True:
            important_constr.append(constr)
    return important_constr

# The important constraints that are fulfilled by the current answer:
def curr_answ_imp_constr():
    """
    Returns all important constraints that are fulfilled by the current
    student answer AND where A and B exist in the student answer.

    Returns
    -------
    important_answ_constr : Constraint[0..*]
        List of Constraint objects of all important constraints that are
        fulfilled by the current student answer to grade.
    """
    # Global variables used:
    global curr_grading_answer
    # Get all important constraints of the current question:
    all_constr = curr_qst_imp_constr()
    # Store all important answers that:
    # - are fulfilled by the current student answer to grade
    # - Where A and B exist in the student answer.
    important_answ_constr = []
    for constr in curr_grading_answer.fulfilled_constraints:
        proc_txt = curr_grading_answer.pre_processed_answer_text
        act_a = constr.activity_a.activity_text
        act_b = constr.activity_b.activity_text
        if act_a in proc_txt and act_b in proc_txt:
            if constr in all_constr:
                important_answ_constr.append(constr)
    return important_answ_constr




##################################### FRAMES ##################################

# --------------------------MAIN----------------------------------------
# Side-Bar:
side_frame = Frame(root, width=300)
side_frame.pack(side="left",anchor=W, fill=Y)
# Main Window:
main_frame = Frame(root)
main_frame.pack(expand=True,fill="both")
# Panel-Window for main_frame:
panel_1 = PanedWindow(main_frame,bd=1,orient=VERTICAL, bg="black")
panel_1.pack(fill=BOTH,expand=1)


# ----------------SIDE BAR----------------------------------------------
space_left = ttk.Label(side_frame, text="")
space_left.grid(row=1,column=1)
space_right = ttk.Label(side_frame, text="")
space_right.grid(row=1,column=3)


# -----------------------QUESTION OVERVIEW------------------------------
# Display-Frame for displaying data about the selected item:
display_frame = Frame(panel_1)


# ----------------------- ANSWERS VIEW ---------------------------------
display_frame_answ = Frame(panel_1)
button_frame_answ = Frame(panel_1)


# ----------------------- RATE CONSTRAINTS VIEW ------------------------
rate_const_frame = Frame(panel_1)
# Frame for Example answer text-field:
example_answ_frm = Frame(rate_const_frame,height=100,width=170)
example_answ_frm.grid(row=3,column=2,sticky=W)
example_answ_frm.grid_propagate(False)


# ----------------------- GRADE ANSWER VIEW ----------------------------
grading_frame = Frame(panel_1)
# Frame for Text field:
grading_answ_frm = Frame(grading_frame,height=100,width=170)
grading_answ_frm.grid(row=2,column=2,sticky=W)
grading_answ_frm.grid_propagate(False)




################################ TEXT & BUTTONS ###############################

# ----------------------- SIDE BAR --------------------------------------
# BUTTON: Import Mohler2009 raw question:
import_btn = Button(side_frame, text="Import", command=import_file_mohler_txt)
import_btn.grid(row=3, column=2)

# Side Panel: Menu button
main = Button(side_frame, text="Main_view", command=back_to_qst)
main.grid(row=2, column=2)


# ----------------------- QUESTION OVERVIEW -----------------------------
# TEXT: Question - Text:
question_label = ttk.Label(display_frame, text="Question: ")
question_label.grid(row=1,column=1,sticky=W)
question_display = ttk.Label(display_frame, text="")
question_display.grid(row=1,column=2,sticky=W)

# TEXT: Number of Student answers:
number_std_answ_label = ttk.Label(display_frame, text="Student answers: ")
number_std_answ_label.grid(row=2,column=1,sticky=W)
number_std_answ_display = ttk.Label(display_frame, text="")
number_std_answ_display.grid(row=2,column=2,sticky=W)

# TEXT: Constraints rated "x from all":
cons_label = ttk.Label(display_frame, text="Constraints rated: ")
cons_label.grid(row=3, column=1, sticky=W)
cons_display = ttk.Label(display_frame, text="", foreground="")
cons_display.grid(row=3, column=2, sticky=W)

# TEXT: Answers graded "y from all":
answ_graded_label = ttk.Label(display_frame, text="Answers graded: ")
answ_graded_label.grid(row=4, column=1, sticky=W)
answ_graded_display = ttk.Label(display_frame, text="", foreground="")
answ_graded_display.grid(row=4, column=2, sticky=W)

# BUTTON: Remove selected question
remove_selected = Button(display_frame, text="Remove", command=remove_selected)
remove_selected.grid(row=10,column=1, sticky=W)


# ----------------------- ANSWERS VIEW ---------------------------------
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

# BUTTON: Export Event-log
export_event_log = Button(button_frame_answ, text="Export Event-log",
                          command=export_event_log_btn)
export_event_log.grid(row=10,column=1)

# BUTTON: Import DECLARE
import_declare = Button(button_frame_answ, text="Import DECLARE",
                        command=import_declare_btn)
import_declare.grid(row=10,column=2)

# BUTTON: Rate Constraints
rate_const_btn = Button(button_frame_answ, text="Rate Constraints",
                        command=rate_const)
rate_const_btn.grid(row=10,column=3)

# BUTTON: Export to .csv
export_csv_btn = Button(button_frame_answ, text="Export .csv",
                        command=export_csv)
export_csv_btn.grid(row=10,column=5)

# BUTTON: Back-to question overview
back_btn = Button(button_frame_answ, text="<-", command=back_to_qst)
back_btn.grid(row=10,column=6)


#---------------------------- RATE CONSTRAINTS ------------------------------
# TEXT: Question-text
rcfrm_question_lab = ttk.Label(rate_const_frame, text="Question: ")
rcfrm_question_lab.grid(row=1,column=1,sticky=W)
rcfrm_question_disp = ttk.Label(rate_const_frame, text="")
rcfrm_question_disp.grid(row=1,column=2,sticky=W)

# TEXT: Unrated constraints counter
const_remain_lab = ttk.Label(rate_const_frame, text="Unrated Constraints: ")
const_remain_lab.grid(row=2,column=1,sticky=W)
const_remain_disp = ttk.Label(rate_const_frame, text="")
const_remain_disp.grid(row=2,column=2,sticky=W)

# TEXT: "Example: "
exmple_answ_lab = ttk.Label(rate_const_frame, text="Example: ")
exmple_answ_lab.grid(row=3,column=1,sticky=W)

# TEXT: field for example answer:
exmple_txt_height = 5
exmple_txt_width = 70
example_answ_txt = Text(example_answ_frm, height=exmple_txt_height,
                        width=exmple_txt_width, wrap ="word")
example_answ_txt.pack(side=LEFT)
example_answ_txt.configure(state=DISABLED)

# TEXT: Constraint explanation:
constr_explanation = ttk.Label(rate_const_frame, text="")
constr_explanation.grid(row=4,column=2,sticky=W)

# BUTTON: Important-Yes
imp_yes_btn = Button(rate_const_frame,text="Important",command=rate_imp_yes)
imp_yes_btn.grid(row=10,column=1)
# BUTTON: Important - No
imp_no_btn = Button(rate_const_frame,text="Not important",command=rate_imp_no)
imp_no_btn.grid(row=10,column=2)


#---------------------------- GRADE ANSWERS --------------------------------
# TEXT: Question-text
grading_qst_lab = ttk.Label(grading_frame, text="Question: ")
grading_qst_lab.grid(row=1,column=1,sticky=W)
grading_qst_disp = ttk.Label(grading_frame, text="")
grading_qst_disp.grid(row=1,column=2,sticky=W)

# TEXT: Student-Answer
grading_answ_lab = ttk.Label(grading_frame, text="Answer: ")
grading_answ_lab.grid(row=2,column=1,sticky=W)

# TEXT: Text field for answer to grade
grading_txt_height = 5
grading_txt_width = 70
grading_answ_txt = Text(grading_answ_frm, height=grading_txt_height,
                        width=grading_txt_width, wrap ="word")
grading_answ_txt.pack(side=LEFT)
grading_answ_txt.configure(state=DISABLED)

# TEXT: Number of important constraints (X from ALL)
grading_imp_const_lab = ttk.Label(grading_frame,text="Important Constraints: ")
grading_imp_const_lab.grid(row=3,column=1,sticky=W)
grading_imp_const_disp = ttk.Label(grading_frame, text="")
grading_imp_const_disp.grid(row=3,column=2,sticky=W)

# ENTRY: Entry field for grade
grading_box = Entry(grading_frame)
grading_box.grid(row=4,column=1)

# BUTTON: "grade"
add_record = Button(grading_frame, text="grade", command=grade_curr_answ)
add_record.grid(row=4,column=2, sticky=W)
root.bind("<Return>", grade_curr_answ)

# BUTTON: Grade Answers
grade_answ_btn = Button(button_frame_answ, text="Grade Answers", command=grading)
grade_answ_btn.grid(row=10,column=4)




#################################### TREES ###################################

# ------------------- QUESTION-Tree-----------------------------------
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

# Columns to display:
question_tree["displaycolumns"] = ("Question", "file")

# BIND: on left mouse-button: select item
question_tree.bind('<ButtonRelease-1>', selectItem_qst)

# BIND: open question-detail-view on double click:
question_tree.bind("<Double-1>", on_double_click_qst)


# ------------------- ANSWER-Tree-----------------------------------
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

# BIND: on left mouse-button: select item
answ_tree.bind('<ButtonRelease-1>', selectItem_answ)




###############################################################################
root.mainloop()
