# Answer grading tool


from python_files.classes import *
from python_files.import_export_functions import *


# (1) import raw data--------------------------------------------------------
question_list = import_mohler_txt(question_id="Q")
question = question_list[0]
original_file_name = question_list[1]


# (3) Generate an Event-log from data----------------------------------------

question.pre_process_question()
question.generate_event_log()
#question.event_log.export_event_log_xes(original_file_name=original_file_name)

#(4) Import constraints from mining-output-----------------------------------

question.event_log.import_mined_declare(original_file_name=original_file_name)


# (5) Check which constraints are in which answers---------------------------

question.check_constraints()

#-------Export grades + number of co-existence-----------------

#export_data_const_incl_a_b(question=question,original_file_name=original_file_name)

question.event_log.rate_constraints()

#question.display_cons_incl_a_b()


for cons in question.event_log.mined_constraints:
    print(cons.constraint_type.constraint_type_name + "[" +
            cons.activity_a.activity_text + "," +
            cons.activity_b.activity_text + "] -> " +
            str(cons.essential_for_rightness))


#
