

Declarative Answer Grader (DAG)

a Tool for "Declarative Process Mining for Short Answer Grading"

- by Markus Bimassl
- For the course "Information Systems Engineering - Course V" 
- at Vienna University of Economics and Business







Tool description:
--------------------------------------------------------------------------------------
This tool can import and display short answer questions, pre-process the answers for 
process discovery and generate an event-log in .xes for it.
A DECLARE file (.decl) that was discovered from the exported event-log can be imported.
The discovered constraints can be rated as important or not important, and the answers 
can be graded.
To support answer grading, the tool will highlight the important constraints that an 
answer fulfills.






File descriptions:
--------------------------------------------------------------------------------------

CODE:
----
DAG_app.py:
The main file that holds the code for the UI. 

classes.py:
Holds the classes and their functions.

import_export_functions.py:
Holds general import/export functions.

xes_structure.py:
Holds the .xes template for the event-log export as .xes.



Additional files/folder:
-----------------------
mohler_files:
Holds the following files/folders.

Mohler_questions_raw:
The raw questions from the Mohler 2009 dataset. If one wants to import their own
questions, they should bring them into the same format as these questions.

event_logs:
Event-logs for all raw mohler2009 questions, that were already produced with this tool.

mined_DECLARE:
Discovered DECLARE files, based on the provided event-logs. These .decl files were 
produced with RuM. 
"Co_existence-files" -> only the co-existence[A,B] constraint,
			min. constraints support = 10%
"All_cons-files" -> all binary constraints,
		    min. constraint support = 10%







How to install and run the tool:
--------------------------------------------------------------------------------------
The tool was written in python 3.10.1

To use it, download the files in the folder structure that they are in. Then, execute
the DAG_app.py script.







How to use the tool:
--------------------------------------------------------------------------------------

To start the tool execute the DAG_app.py script.


Import Questions:
To import a new question, press the "import" button. Currently the tool will only
correctly detect the format of the Mohler 2009 questions, that are in the mohler_files
folder.
Multiple files can also be supported at once -> just select multiple files in the
open-file dialog.


Remove Questions:
To remove a question, select it in the tree-view per left-click. Then press the 
"remove" button.
Multiple questions can be removed at once -> Select multiple questions with 
"shift + mouse-click" or "str + mouseclick" and then press the remove button.


Show Question details / Show Answers to a question:
Double-click the question in the tree. In the answers-view, you can go back to the 
question-view by clicking on the "<-" button.
You can also get back to the questions-view from anywhere by clicking the "Main_view"
button.


Export Event-log:
To export an event-log in .xes for the currently displayed question in the answers-
view, click the "Export Event-log" button and save the .xes file.


Import DECLARE:
To import a discovered DECLARE file (.decl) for the currently displayed question, 
click on the "Import DECLARE" button and select the .decl file.
NOTE: Be careful to import the right DECLARE-file for the right question!


Rate Constraints:
This will only work, if you imported a DECLARE file for the question.
To rate the discovered constraints of a question, press the "Rate Constraints" 
button in the answers-view.
A new frame will display:
- The question
- the number of remaining unrated constraints
- An example answer that fulfills the current constraint to rate (if the answer
  has A and B in it, they will be highlighted yellow)
- The name of the constraint in the format <Constraint> [<A>,<B>]
- Buttons for "Important" or "Not important"


Grade Answers:
To grade answers of a question, press the "Grade Answers" button in the 
answers-view.
A new frame will display:
- the question
- the current answer to grade ( A and B of the important constraints that the 
  answer fulfills, are highlighted in green)
- the important constraints that are fulfilled by the answer
- an entry field, to enter the grade (no specific format needed)
- a "grade" button that will take the entered grade from the entry field and
  store it in the answer object.


Export data as .csv:
To export the data from a question, press the "Export .csv" button in the 
answer-view.
This will generate a .csv in the format:
["Student_id","new_grade","mohler_grade","cons_incl_a_b"]
- Student_id = the student-id of an answer
- new_grade = the grade that was entered in "Grade Answers"
- mohler_grade = the original grade from the mohler-file
- cons_incl_a_b = the number of fulfilled constraints of the answer, where A and B
		  are also in the answer.






Credits:
--------------------------------------------------------------------------------------

RuM:
The RuM-Tool was used to create the .decl files of the event-logs.
The DECLARE-Templates described in RuM were also the template for the integration of
the constraints in this tool. The positive and negative examples for each template in
RuM were used to test the constraint-functions.
https://rulemining.org/


Tkinter Tutorials from the Codemy.com Youtube channel:
These were the main source to learn, how to use tkinter to generate the UI.
https://www.youtube.com/c/Codemycom


Mohler 2009 dataset:
The dataset from the Mohler 2009 study was used to test the tool. The import function
was built for this data.
Mohler, M., & Mihalcea, R. (2009, March). Text-to-text semantic similarity for automatic 
short answer grading. In Proceedings of the 12th Conference of the European Chapter of 
the ACL (EACL 2009) (pp. 567-575).






License:
--------------------------------------------------------------------------------------

MIT License

Copyright (c) 2022 Markus Bimassl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.








