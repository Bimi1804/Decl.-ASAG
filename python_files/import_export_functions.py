# Answer grading functions
from python_files.classes import *
import csv # for creating .csv files

original_file_name = "" # To store the file-name of the imported file globally
                        # (!) This should be changed in future iterations (!)
                        # Can be stored in the Question-object

#----------------Mohler2009 import from txt file--------------------------------
def import_mohler_txt(question_id=0):
    """
    Import raw Mohler 2009 data.

    Input-file may only containt ONE question and has to be in .txt
    Structure of input-file:
        Question: <question-text>
        Answer: <teacher-answer-text>

        <grade> [ <student-ID> ] <student-answer-text>
        ...

    Parameters
    ----------
    import_file=None : str
        The path to the import-file

    Returns
    -------
    returned_imports : List
        A list with elements [new_question,original_file_name]

        new_question : Question
            The created Question object
        original_file_name : str
            The file-path of the imported file
    """
    # open file-dialog to choose file
    returned_imports = []
    import_files = askopenfilenames(title="Import Mohler2009 question")
    for file in import_files:
        original_file_name = str(file) # store file-name
        with open(file, encoding="utf-8") as raw_dataset_file:
            raw_dataset_txt = raw_dataset_file.read() # read the import_file
        dataset_list = raw_dataset_txt.split("\n") # Split raw dataset into a list
        # initial clearing of import-data
        for i in range(len(dataset_list)):
            cleared_line = (dataset_list[i].replace("\t","").
                                replace("<br>","").
                                replace("-", "")
                            )
            dataset_list[i] = cleared_line
        # Look for the "Question:..." and store the question-text
        question = "" # store the question-text
        for line in dataset_list:
            if "Question:" in line:
                question = line
                dataset_list.remove(line)
                question = question.replace("Question:", "")
        # Look for the teacher-answer and store the answer-text:
        teacher_answers = [] # store teacher-answer-text
        for line in dataset_list:
            if "Answer:" in line:
                teacher_answer = line.replace("Answer:", "")
                teacher_answers.append(teacher_answer)
                dataset_list.remove(line)
        # Look for the student-answers:
        # All student-answers have the student-ID in []
        answer_list = [] # store student-answers
        for line in dataset_list:
            if "[" in line or "]" in line:
                answer_list.append(line)
        # Create the Question-object:
        new_question = Question(q_id = "Q." + str(question_id), q_text=question)
        question_id += 1
        # Create Teacher_answer objects:
        for i in teacher_answers:
            teacher_answer = Teacher_answer(question=new_question,answer_text=i)
        # Create Student_answer objects:
        for i in answer_list:
            # structure of student-answers in Mohler_raw:
            # <grade> [ <student-ID> ] <answer-text>
            first_marker = i.find("[")
            second_marker = i.find("]")
            student_answer = Student_answer(
                                    question = new_question,
                                    answer_text = i[second_marker+1:],
                                    student_id = i[first_marker+1:second_marker],
                                    grade = i[:first_marker])
        returned_imports.append([new_question, original_file_name])
    return returned_imports


def export_data_as_csv(question=None, export_file=None, original_file_name=""):
    """
    Export the discovered data about the student-answers of a question

    Parameters
    ----------
    question=None: Question
        The Question object to which the student-answers belong.
    export_file=None : str
        The file to which the data should be exported. Opens a file-dialog if
        it is None.
    original_file_name : str
        The name of the original raw_data file. Will be displayed as title of
        file-dialog window.

    Returns
    -------
    export_file : str
        The path to the exported file.
    """
    # Type-checking of question
    if question is None or type(question) is not Question:
        print("Please enter a question-object")
        return False
    # Open file-dialog is export_file is None
    if export_file is None:
        export_file = asksaveasfilename(
                        title="Export Analysis Data for: " + original_file_name,
                        filetypes=[('CSV','*.csv')],
                        defaultextension="csv",
                        initialfile=question.q_id + "_analysis")
    if export_file != "":
        # Define the header for the .csv
        header = ["Student_id","grade","number_of_constraints"]
        with open(export_file,"w",newline="") as file:
            writer=csv.writer(file)
            writer.writerow(header) # write header into file
            # write rows with sutdent_id, grade, number of fulfilled constraints
            for answ in question.student_answers:
                writer.writerow([answ.student_id,
                                answ.grade,
                                len(answ.fulfilled_constraints)])
    return export_file


def export_data_const_incl_a_b(question=None, export_file=None,
                                original_file_name=""):
    # Type-checking of question
    if question is None or type(question) is not Question:
        print("Please enter a question-object")
        return False
    # Open file-dialog is export_file is None
    if export_file is None:
        export_file = asksaveasfilename(
                        title="Export Analysis Data for: " + original_file_name,
                        filetypes=[('CSV','*.csv')],
                        defaultextension="csv",
                        initialfile=question.q_id + "_analysis")
    if export_file != "":
        # Define the header for the .csv
        header = ["Student_id","grade","cons_incl_a_b"]
        with open(export_file,"w",newline="") as file:
            writer=csv.writer(file)
            writer.writerow(header) # write header into file
            # write rows with sutdent_id, grade, number of fulfilled constraints
            for answ in question.student_answers:
                cons_incl_a_b = []
                pro_answ = answ.pre_processed_answer_text
                # Only include constraints where A and B are in the answer:
                for cons in answ.fulfilled_constraints:
                    cons_a = cons.activity_a.activity_text
                    cons_b = cons.activity_b.activity_text
                    if  cons_a in pro_answ and cons_b in pro_answ:
                        cons_incl_a_b.append(cons)
                writer.writerow([answ.student_id,
                                answ.grade,
                                len(cons_incl_a_b)])
    return export_file
