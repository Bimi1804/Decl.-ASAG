# declarative answer grader: class definitions

#----------IMPORTS-----------------------------------------------------
# import structure for .xes event-logs files:
from python_files.xes_structure import *

# import nltk-package for NLP pre-processing:
import nltk # nltk package: https://www.nltk.org/data.html
from nltk.stem import WordNetLemmatizer # for lemmatization
from nltk.corpus import stopwords # for stopword removal
from nltk.tokenize import word_tokenize # for stopword removal
# set variables for NLP pre-processing:
lemmatizer = WordNetLemmatizer() # lemmatization function
stop_words = set(stopwords.words('english')) # english stop-words
removable_items = [".", ","] # additional strings that should be removed

# import tkinter for dialog-windows:
#import tkinter as tk
from tkinter.filedialog import askopenfilenames # dialog for opening a file
from tkinter.filedialog import askopenfilename # dialog for opening a file
from tkinter.filedialog import asksaveasfilename # dialog for saving a file
#root = tk.Tk()
#root.withdraw()

# import abstract base class (abc):
from abc import (ABC,abstractmethod) # for abstract class and abstract method


#------Global Functions----------------------------------------------------
class Tools:
    """"
    Class for all global functions

    Methods
    --------
    pre_process(original_text) : str[0..*]
        Pre-processes a string into a list of words.
    """
    def __init__(self):
        pass
    def pre_process(self,original_text):
        """
        Pre-processes an original_text as string into processed_text as a list.

        Parameters
        ----------
        original_text : str
            The original_text as a string

        Returns
        -------
        processed_text : str[0..*]
            A list with indidivual words
         """

        # transform words into only lowercase and tokenize them:
        word_tokens = word_tokenize(original_text.lower())
        words_without_stop = [] # store non-stop-words
        for w in word_tokens:
            # append non-stop-words to words_without_stop:
            if w not in stop_words:
                words_without_stop.append(w)

        # lemmatization of words_without_stop:
        processed_text = [] # store lemmatized words
        for word in words_without_stop:
            lemma_word = lemmatizer.lemmatize(word)
            processed_text.append(lemma_word)

        # remove additional words or symbols:
        final_processed_text = [] # final processed words
        for word in processed_text:
            if word not in removable_items:
                final_processed_text.append(word)
        return final_processed_text
tools = Tools() # instantiation of the Tools class

#---------------------------Answer-grading Classes------------------------------

class Question:
    """
    The Question of an Exam

    Parameters
    ----------
    q_id : str
        To directly store the question ID
    q_text : str
        To directly store the question text
    original_file_name : str
        The file name of the raw import file

    Attributes
    ----------
    q_id : str
        Store the question ID
    q_text : str
        Store the question text
    original_file_name : str
        Store original_file_name
    pre_processed_question_text : str[0..*]
        The question text after NLP pre-processing
    student_answers : Student_answer[0..*]
        Holds the student answers
    teacher_answers : Teacher_answer[0..*]
        Holds the teacher answers
    event_log : Event_log
        Holds the Event_log

    Methods
    ---------
    pre_process_question(): Question
        Pre-processing the original question,student- and teacher-answer texts
    generate_event_log(): Event_log
        Generate an Event_log object
    check_constraints(): Question
        Check which mined constraints are fulfilled by the answers
    calculate_rightness():
        Calculate the "rightness" of answers
    display_cons():
        Displays all processed answer texts and the fulfilled constraints.
    display_cons_incl_a_b():
        Displays all processed answer texts and the fulfilled constraints where
        A and B are included in the processed answer.
    """
    def __init__(self,q_id,q_text,original_file_name):
        self.q_id = q_id
        self.q_text = q_text
        self.original_file_name = original_file_name
        self.pre_processed_question_text = []
        self.student_answers = []
        self.teacher_answers = []
        self.event_log = ""

    def pre_process_question(self):
        """
        NLP pre-processing of the question text and the student- and teacher-
        answers

        Stores the processed text in the objects (Question, Student_answer,
                                                  Teacher_answer)

        Parameters
        ----------
        None

        Returns
        -------
        self
            Returns the Question object
        """
        # Use the pre-process method from the Tools class:
        self.pre_processed_question_text = tools.pre_process(self.q_text)
        for i in self.student_answers:
            i.pre_processed_answer_text = tools.pre_process(i.answer_text)
        for i in self.teacher_answers:
            i.pre_processed_answer_text = tools.pre_process(i.answer_text)
        return self

    def generate_event_log(self):
        """
        Generates an event-log from all student answers in a .xes format

        Parameters
        ----------
        None

        Returns
        -------
        self.event_log
            The created Event_log object
        """
        log_traces = "" # store traces(answers) of the log
        for answ in self.student_answers:
            trace_events = "" # store events(words) of a trace
            order = 1 # the order of the events(words)
            for word in answ.pre_processed_answer_text:
                # use xes-template for events and fill {word} and {order}:
                trace_events += xes_template.xes_event.format(word=word,
                                                                order=order)
                order += 1 # increment order
            # use xes-template for traces and fill with {student_id} and
            # {trace_events}:
            log_traces += xes_template.xes_trace.format(trace_id=answ.student_id,
                                                        events=trace_events)
        # use xes-template for log-head and fill with {log_traces}:
        xes_log = xes_template.xes_head.format(traces=log_traces)
        # Create a new Event_log object with xes_log as log-string:
        self.event_log = Event_log(question=self, event_log_string=xes_log)
        return self.event_log

    def check_constraints(self):
        """
        Check which constraints are fulfilled by the student_answers

        The fulfilled constraints of each answer are stored in the
        Student_answer object
        """
        # loop over all discovered constraints:
        for const in self.event_log.mined_constraints:
            # loop over the student answers:
            for answ in self.student_answers:
                # check if the answer fulfills the constraint:
                if const.constraint_type.conformance_check(const,answ) is True:
                    # Append constraint to the answer's fulfilled constraints
                    answ.fulfilled_constraints.append(const)
        return self

    def calculate_rightness():
        # calculate the "rightness of answers"
        # This function will create an event-log an declaratively mine for
        # constraints...
        pass

    def display_cons(self):
        """
        Displays all processed answer texts and the fulfilled constraints.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for answ in self.student_answers:
            print( "["+ answ.student_id + "] " + str(answ.pre_processed_answer_text))
            for const in answ.fulfilled_constraints:
                print(const.constraint_type.constraint_type_name + "[" +
                const.activity_a.activity_text + ", " +
                const.activity_b.activity_text + "]")

    def display_cons_incl_a_b(self):
        """
        Display the processed answer texts and all constraints where A and B
        are also included in the answer.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for answ in self.student_answers:
            print( "["+ answ.student_id + "] " + str(answ.pre_processed_answer_text))
            answer = answ.pre_processed_answer_text
            for const in answ.fulfilled_constraints:
                a = const.activity_a.activity_text
                b = const.activity_b.activity_text
                if a in answer and b in answer:
                    print(const.constraint_type.constraint_type_name + "[" +
                          const.activity_a.activity_text + ", " +
                          const.activity_b.activity_text + "]")

class Answer(ABC):
    """
    The abstract Answer class

    Parameters
    ----------
    question : Question
        The Question object to which the answer belongs
    answer_text : str
        The answer text as a string

    Attributes
    ----------
    question : Question
        To store the Question object
    answer_text : str
        To store the answer text
    pre_processed_answer_text : str[0..*]
        A list of words that were processed from answer_text
    fulfilled_constraints : Constraint[0..*]
        A list with all fulfilled Constraint objects
    """
    def __init__(self,question,answer_text):
        if type(question) is not Question:
            return False
        self.question = question
        self.answer_text = answer_text
        self.pre_processed_answer_text = []
        self.fulfilled_constraints = []

class Teacher_answer(Answer):
    """
    Sub-class of Answer

    A teacher answer of a question

    Adds itself to the list of teacher answers of the question when created

    Additional Parameters
    --------------------
    None
    """
    def __init__(self,question,answer_text):
        super().__init__(question,answer_text)
        # Add the object to the teacher_answers list of the Question object
        # that is given as Parameter:
        question.teacher_answers.append(self)

class Student_answer(Answer):
    """
    Sub-class of Answer

    A student answer of a question

    Adds itself to the list of student answers of the question when created

    Additional Parameters
    ---------------------
    student_id : str
        The student-ID of a student, so answers can be assigned to the right
        student
    grade = None : str
        The grade or points that were given to the student answer

    Additional Attributes
    --------------------
    student_id : str
        To store student_id
    calculated_rightness : int
        To store the calculated rightness of a student answer
    grade : str
        To store grade
    """
    def __init__(self,question,answer_text,student_id,grade=None):
        super().__init__(question,answer_text)
        self.student_id = student_id
        self.calculated_rightness = None
        self.grade = grade
        self.new_grade = None
        # Add the object to the student_answer list of the Question object
        # that is given as Parameter:
        question.student_answers.append(self)

class Event_log:
    """
    The event-log that is generated for a question

    Parameters
    ----------
    question : Question
        The Question object which the Event_log belongs to
    event_log_string : str
        The actual event-log in a .xes structure as a string

    Attributes
    ----------
    question : Question
        To store question
    event_log_xes : str
        To store event_log_string
    mined_activities : Activity[0..*]
        To store the mined activities of the event-log
    mined_constraints : Constraint[0..*]
        To store the mined constraints of the event-log

    Methods
    -------
    export_event_log_xes(output_file=None,original_file_name=""): str
        Exports the event-log in a .xes file
    import_mined_declare(import_file=None,original_file_name=""): Event_log
        Imports a .decl file to store the discovered activities and constraints
    mining()
        This would be the included miner
    """
    def __init__(self, question, event_log_string):
        self.question = question
        self.event_log_xes = event_log_string
        self.mined_activities = []
        self.mined_constraints = []

    def export_event_log_xes(self,output_file=None,original_file_name=""):
        """
        Exports the event-log as a .xes file

        Parameters
        ----------
        output_file = None : str
            The file path to the file where the event-log should be stored.
            If this is None, then a dialog window will open to save the file.
        original_file_name : str
            The file name of the raw input file for the question. This is
            displayed in the file-saving-window.

        Returns
        -------
        output_file : str
            Returns the path to the output_file
        """
        if output_file is None:
            # Open file dialog to type in file-name (only .xes):
                # Default file-name is question-ID + "_log"
            output_file = asksaveasfilename(
                                title="Export event-log for: " +
                                                original_file_name,
                                filetypes=[('Event-Log', '*.xes')],
                                defaultextension="xes",
                                initialfile=self.question.q_id + "_log")
        if output_file != "": # Only write to the file if it exists/has a name
            with open(output_file, "w") as file_xes:
                file_xes.write(self.event_log_xes)
        return output_file

    def import_mined_declare(self,import_file=None,original_file_name=""):
        """
        Import a .decl file and create Activity and Constraint objects based on
        the content of the .decl file.

        Activity and Constraint objects will be created.

        Parameters
        ----------
        import_file=None : str
            The file path to the file that should be imported.
            If this is None, then a dialog window will open to choose the file.
        original_file_name : str
            The file name of the raw input file for the question. This is
            displayed in the file-opening-window.

        Returns
        -------
        self
        """
        if import_file is None:
            # open file-dialog to choose the .decl import-file:
            import_file = askopenfilename(title="Import DECLARE file for:" +
                                                        original_file_name,
                                            filetypes=[('DECLARE', '*.decl')])
        with open(import_file, "r") as raw_decl:
            raw_decl_file = raw_decl.read()
        decl_file = raw_decl_file.split("\n") # split at each new line
        decl_file.remove("") # remove any empty lines

        constraints = [] # store the lines that define constraints
        for line in decl_file:
            # if the line defines an activity, then create and store a new
            # Activity object:
            if "activity" in line:
                new_activity = Activity(self, line[len("activity")+1:])
            else:
                # if not, then append the line to the constraints list:
                constraints.append(line)

        for line in constraints:
            # Structure of .decl files: <constraint>[<activity_a>, <activity_b>]
            first_marker = line.find("[") # Find the index of  [
            second_marker = line.find("]") # Find the index of ]
            constraint = line[:first_marker] # This is the <constraint>
            activities = line[first_marker+1:second_marker] # Both activities
            mid_marker = activities.find(",") # The marker between the
                                              # activities
            activity_a_word = activities[:mid_marker] # Activity A
            activity_b_word = activities[mid_marker+2:] # Activity B
            for act in self.mined_activities:
                # Get the Activity objects for the activities A and B of the
                # constraint
                if act.activity_text == activity_a_word:
                    activity_a = act
                if act.activity_text == activity_b_word:
                    activity_b = act
            for c_t in constraint_types:
                # Get the constraint type of the constraint
                if c_t.constraint_type_name == constraint:
                    constraint_type = c_t
            # Create a new constraint object
            new_constraint = Constraint(activity_a, activity_b, constraint_type)
        return self

    def mining():
        #This would be the declarative process Miner
        pass

    def rate_constraints(self):
        """
        Rate all constraints of an event-log. If they are essential for the
        "rightness" of an answer.

        Display the original answer and the constraint. Ask the user if the
        constraint is important for the rightness of the answer (Yes/No).

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for cons in self.mined_constraints:
            example_answ = ""
            for answ in self.question.student_answers:
                if example_answ is not None:
                    if cons in answ.fulfilled_constraints:
                        cons_a = cons.activity_a.activity_text
                        cons_b = cons.activity_b.activity_text
                        proc_answ = answ.pre_processed_answer_text
                        if cons_a in proc_answ and cons_b in proc_answ:
                            example_answ = answ.answer_text
            print("Q: " + self.question.q_text)
            print("Student: " + example_answ)
            print(cons.constraint_type.constraint_type_name + "[" +
                    cons.activity_a.activity_text + "," +
                    cons.activity_b.activity_text + "]")
            user_input = ""
            while user_input not in ["y", "n"]:
                user_input = input("Important?(y/n): ")
                if user_input.lower() == "y":
                    rightness = True
                if user_input.lower() == "n":
                    rightness = False
                cons.essential_for_rightness = rightness
                print("")


class Activity:
    """
    An Activity that was discovered from an event-log

    Appends itself to the mined_activities-list of the Event_log object that
    created it.

    Parameters
    ----------
    event_log : Event_log
        The Event_log objects to which the Activity belongs
    activity_text : str
        The actual text (word) of the activity
    activity_support=100 : int
        The support of the activity that was discovered by the miner

    Attributes
    ----------
    event_log : Event_log
        Store event_log
    activity_text : str
        Store activity_text
    activity_support : int
        Store activity_support
    """
    def __init__(self,event_log,activity_text,activity_support=100):
        self.event_log = event_log
        self.activity_text = activity_text
        self.activity_support = activity_support
        self.event_log.mined_activities.append(self)

class Constraint:
    """
    A constraint that was discovered from an event-log

    Appends itself to the mined_constraints-list of the Event_log object that
    created it.

    Parameters
    ---------
    activity_a : Activity
        The activity A of the constraint
    activity_b : Activity
        The activity B of the constraint
    constraint_type : Constraint_type
        The constraint-type (constraint-template) of the constraint
    constraint_support=100 : int
        The support of the constraint that was discovered by the miner

    Attributes
    ----------
    activity_a : Activity
        To store activity A
    activity_b : Activity
        To store activity B
    constraint_type : Constraint_type
        To store the constraint type
    constraint_support : int
        To store the constraint support
    essential_for_rightness : bool
        If the constraint is important for the rightness of an answer (Yes/No)
    """

    def __init__(self,activity_a, activity_b,
                constraint_type, constraint_support=100):
        # Type-checking of inputs:
        if type(constraint_type) is not Constraint_type:
            print("Constraint-type is not a Constraint_type-object")
            return False
        if type(activity_a) is not Activity:
            print("Activity-A is not an Activity-object")
            return False
        if type(activity_b) is not Activity:
            print("Activity-B is not an Activity-object")
            return False
        self.activity_a = activity_a
        self.activity_b = activity_b
        self.constraint_type = constraint_type
        self.constraint_support = constraint_support
        self.essential_for_rightness = None
        self.activity_a.event_log.mined_constraints.append(self)

class Constraint_type:
    """
    A Constraint-type (constraint-template)

    Parameters
    ----------
    constraint_type_name : str
        The name of the constraint-type

    Attributes
    ----------
    constraint_type_name : str
        To store the constraint_type_name

    Methods
    -------
    conformance_check(constraint,answer) : bool
        Checks if the given answer fulfills the given constraint
    """
    def __init__(self,constraint_type_name):
        self.constraint_type_name = constraint_type_name

    def conformance_check(self,constraint,answer):
        """
        Checks if the given answer fulfills the given constraint

        Parameters
        ----------
        constraint : Constraint
            The constraint that the answer will be checked for
        answer : Answer
            The answer that will be checked (a subclass of Answer)

        Returns
        -------
        return_value : bool
            True - the answer fulfills the constraint
            False - the answer does not fulfill the constraint
        """
        # Type-checking of inputs:
        if type(constraint) is not Constraint:
            print("Constraint given is not a Constraint-Object")
            return False
        if not issubclass(type(answer),Answer):
            print("Answer given is not an Answer-Object")
            return False

        act_a = constraint.activity_a.activity_text # the text-string of act. A
        act_b = constraint.activity_b.activity_text # the text-string of act. B
        processed_answer = answer.pre_processed_answer_text # pre-processed text
                                                            # of the answer
        return_value = False
        # Use the conformance check that belongs to the constraint-type
        #Binary Positive Constraints:----
        # X_Existence----
        if self.constraint_type_name == "Co-Existence":
            return_value = self.__co_existence_check(act_a,act_b,
                                                     processed_answer)
        if self.constraint_type_name == "Responded Existence":
            return_value = self.__responded_existence_check(act_a,act_b,
                                                           processed_answer)

        # Simple_X----
        if self.constraint_type_name == "Precedence":
            return_value = self.__precedence_check(act_a,act_b,processed_answer)
        if self.constraint_type_name == "Response":
            return_value = self.__response_check(act_a,act_b,processed_answer)
        if self.constraint_type_name == "Succession":
            return_value = self.__succession_check(act_a,act_b,processed_answer)

        # Alterate_X----
        if self.constraint_type_name == "Alternate Precedence":
            return_value = self.__alternate_precedence_check(act_a,act_b,
                                                             processed_answer)
        if self.constraint_type_name == "Alternate Response":
            return_value = self.__alternate_response_check(act_a,act_b,
                                                           processed_answer)
        if self.constraint_type_name == "Alternate Succession":
            return_value = self.__alternate_succession_check(act_a,act_b,
                                                           processed_answer)

        # Chain_X----
        if self.constraint_type_name == "Chain Precedence":
            return_value = self.__chain_precedence_check(act_a,act_b,
                                                           processed_answer)
        if self.constraint_type_name == "Chain Response":
            return_value = self.__chain_response_check(act_a,act_b,
                                                           processed_answer)
        if self.constraint_type_name == "Chain Succession":
            return_value = self.__chain_succession_check(act_a,act_b,
                                                           processed_answer)
        return return_value

    #Binary Positive Constraints:----
    # X_Existence----
    def __co_existence_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Co-Existence[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # Check if A and B are both NOT in the answer:
        if act_a not in processed_answer and act_b not in processed_answer:
            return True
        # Check if A and B are both in the answer:
        if act_a in processed_answer and act_b in processed_answer:
            return True
        else:
            # If only A or only B is in the answer:
            return False

    def __responded_existence_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Responded Existence[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A not in answer:
        if act_a not in processed_answer:
            return True
        # False if A in answer but B not in answer
        if act_a in processed_answer and act_b not in processed_answer:
            return False
        # True if A is in the answer and B is in the answer
        return True

    # Simple_X----
    def __precedence_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Precedence[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        checking = processed_answer # store the answer
        if act_b not in checking:
            # if B not in the answer:
            return True
        while act_b in checking:
            # as long as B is in the answer:
            act_b_index = checking.index(act_b) # find index of B
            if act_a not in checking[:act_b_index]:
                # If A is not before B:
                return False
            # Continue with the part of the answer after the first B
            checking = checking[act_b_index+1:]
        # If the answer does not violate the constraint:
        return True

    def __response_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Response[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A is not in processed_answer:
        if act_a not in processed_answer:
            return True
        # False if A in answer but B not in answer:
        if act_a in processed_answer and act_b not in processed_answer:
            return False
        checking = processed_answer
        while act_a in checking:
            # False if A is in remaining answer but B is not:
            if act_b not in checking:
                return False
            marker_a = checking.index(act_a)
            # False if A is the last element:
            if marker_a == len(checking)-1:
                return False
            if act_b not in checking[marker_a:]:
                return False
            checking = checking[marker_a+1:]
        return True

    def __succession_check(self,act_a, act_b,processed_answer):
        """
        Checks if the answer fulfills Succession[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A and B are not in the answer:
        if act_a not in processed_answer and act_b not in processed_answer:
            return True
        # False if only A or only B is in the answer:
        if act_a not in processed_answer or act_b not in processed_answer:
            return False
        checking = processed_answer
        while act_a in checking:
            if act_b not in checking:
                return False
            marker_a = checking.index(act_a)
            marker_b = checking.index(act_b)
            # False if A is the last element of the answer:
            if marker_a == len(checking)-1:
                return False
            # False if B comes before A:
            if marker_a > marker_b:
                return False
            # Continue after B:
            checking = checking[marker_b+1:]
        return True

    # Alternate X
    def __alternate_precedence_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Alternate Precedence[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if B is not in the answer:
        if act_b not in processed_answer:
            return True
        # False if B is in the answer but no A is in the answer:
        if act_b in processed_answer and act_a not in processed_answer:
            return False
        checking = processed_answer
        # Check if every B is preceded by an A
        while act_b in checking:
            # False if B is in the remaining answer but no A:
            if act_a not in checking:
                return False
            marker_b = checking.index(act_b) # index of first B
            marker_a = checking.index(act_a) # index of first A
            # False if A is not before B
            if marker_b < marker_a:
                return False
            # continue with the remaining answer after B
            checking = checking[marker_b+1:]
        return True

    def __alternate_response_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Alternate Response[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A not in the answer:
        if act_a not in processed_answer:
            return True
        # False if A in the answer but no B:
        if act_a in processed_answer and act_b not in processed_answer:
            return False
        checking = processed_answer
        # Check if every A is followed by B without A between:
        while act_a in checking:
            # False if no B in remaining answer:
            if act_b not in checking:
                return False
            marker_a = checking.index(act_a)                # index of first A
            marker_b = checking.index(act_b)                # index of first B
            # False if B before A:
            if marker_b < marker_a:
                return False
            # False if an A is between first A and first B
            if act_a in checking[marker_a+1:marker_b]:
                return False
            checking.pop(marker_a)                          # remove first A
            checking.pop(checking.index(act_b))             # remove first B
        return True

    def __alternate_succession_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Alternate Succession[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A and B are not in the answer:
        if act_a not in processed_answer and act_b not in processed_answer:
            return True
        # False if only A or only B is in the answer:
        if act_a not in processed_answer or act_b not in processed_answer:
            return False
        checking = processed_answer
        # Check as long as A or B are in the remaining answer:
        while act_a in checking or act_b in checking:
            # False if one of them is not in the reamaining answer:
            if act_a not in checking:
                return False
            if act_b not in checking:
                return False
            marker_a = checking.index(act_a)                # index of first A
            marker_b = checking.index(act_b)                # index of first B
            # False if A follows B:
            if marker_a > marker_b:
                return False
            # False if an A is between first A and first B
            if act_a in checking[marker_a+1:marker_b]:
                return False
            checking.pop(marker_a)                          # remove first A
            checking.pop(checking.index(act_b))             # remove first B
        return True

    # Chain X
    def __chain_precedence_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Chain Precedence[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if B is not in the answer:
        if act_b not in processed_answer:
            return True
        # False if B is in answer but A is not in answer:
        if act_b in processed_answer and act_a not in processed_answer:
            return False
        checking = processed_answer
        while act_b in checking:
            marker_b = checking.index(act_b)
            # False if B is the first element:
            if marker_b == 0:
                return False
            # False if A is not directly before B:
            if checking[marker_b-1] != act_a:
                return False
            checking.pop(marker_b)
            checking.pop(checking.index(act_a))
        return True

    def __chain_response_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Chain Reponse[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A is not in answer:
        if act_a not in processed_answer:
            return True
        # False if A is in answer but B is not in answer:
        if act_a in processed_answer and act_b not in processed_answer:
            return False
        checking = processed_answer
        while act_a in checking:
            # False if B not in remaining answer:
            if act_b not in checking:
                return False
            marker_a = checking.index(act_a)       # index of first A
            # False if A is the last element:
            if marker_a == len(checking)-1:
                return False
            # False is A is not immediately followed by B:
            if checking[marker_a+1] != act_b:
                return False
            checking.pop(marker_a)
            checking.pop(checking.index(act_b))
        return True

    def __chain_succession_check(self,act_a,act_b,processed_answer):
        """
        Checks if the answer fulfills Chain Succession[A,B]

        Parameters
        ----------
        act_a : str
            The actual text (word) of activity A
        act_b : str
            The actual text (word) of activity B
        processed_answer : str[0..*]
            the list of processed words of the answer

        Returns
        -------
        True -> If the answer fulfills the constraint
        False -> If the answer does not fulfill the constraint
        """
        # True if A and B are not in answer:
        if act_a not in processed_answer and act_b not in processed_answer:
            return True
        # False if only A or only B is in answer:
        if act_a not in processed_answer or act_b not in processed_answer:
            return False
        checking = processed_answer
        while act_a in checking or act_b in checking:
            # False if only A or only B in reamining answer:
            if act_b not in checking or act_a not in checking:
                return False
            marker_a = checking.index(act_a)        # index of the first A
            # False if A is the last element:
            if marker_a == len(checking)-1:
                return False
            # False is A is not immediately followed by B:
            if checking[marker_a+1] != act_b:
                return False
            checking.pop(marker_a)
            checking.pop(checking.index(act_b))
        return True

#-----------------------------------------------------------------------------
coexistence = Constraint_type("Co-Existence") # instantiation of "Co-Existence"
precedence = Constraint_type("Precedence")
alternate_precedence = Constraint_type("Alternate Precedence")
alternate_response = Constraint_type("Alternate Response")
alternate_succession = Constraint_type("Alternate Succession")
chain_precedence = Constraint_type("Chain Precedence")
chain_response = Constraint_type("Chain Response")
chain_succession = Constraint_type("Chain Succession")
responded_existence = Constraint_type("Responded Existence")
response = Constraint_type("Response")
succession = Constraint_type("Succession")

constraint_types = [coexistence,precedence,alternate_precedence,
                    alternate_response, alternate_succession,chain_precedence,
                    chain_response,chain_succession,responded_existence,
                    response,succession]
