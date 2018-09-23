from chat_bot_server_dir.work_database import work_database
from chat_bot_server_dir.intent_func import get_user_email
from server_dir.slack_message_sender import send_channel_message
from server_dir.slack_message_sender import send_direct_message

import os, random

def sentence_processing_main(intent_type, slack_code, param0, param1, param2):
    message = "default"

    if(intent_type == 1):
        message = approved_file_logic(slack_code, param0, param1)

    elif(intent_type == 2):
        message = lock_file_logic(slack_code, param0, param1, param2)

    elif(intent_type == 3):
        message = code_history_logic(slack_code, param0, param1, param2)

    elif(intent_type == 4):
        message = ignore_file_logic(slack_code, param0, param1)

    elif(intent_type == 5):
        message = check_conflict_logic(slack_code, param0)

    elif(intent_type == 6):
        message = other_working_status_logic(slack_code, param0, param1)

    elif(intent_type == 7):
        message = send_message_channel_logic(param0, param1, param2)

    elif(intent_type == 8):
        message = send_message_direct_logic(param0, param1, param2)

    elif(intent_type == 9):
        message = recommend_solve_conflict_logic(param0, param1)

    elif(intent_type == 10):
        message = greeting_logic(slack_code)

    elif(intent_type == 11):
        message = bye_logic()

    elif(intent_type == 12):
        message = """I don't know what are you talking about. I am conflict detect chatbot, and I have 12 talking features : 
        #1. ignore_file : It functions like gitignore. A user can customize his/her ignore files.
        #2. lock_file : A user can lock his/her files. If other users try to modify the related file of the lock_file, chatbot gives them a warning.
        # 3. code_history : A user can ask who wrote certain code lines.
        # 4. ignore_alarm : A user can ignore direct and indirect conflicts.
        # 5. check_conflict : Before a user starts to work, the user can check if he/she generates conflict or not on the working file
        # 6. working_status : A user can ask about other user's working status
        # 7. channel_message : A user can let chatbot give a message to channel.
        # 8. user_message : A user can let chatbot give a message to other users.
        # 9. recommend : A user can ask chatbot to recommend reaction to conflict.
        # 10. user_recognize : Chatbot knows when last time a user connected is, so bot can greet the user with time information. ex) It's been a while~
        # 11. greeting : Chatbot can greet users.
        # 12. complimentary_close : Chatbot can say good bye.
        # 13. detect_direct_conflict : Chatbot can detect direct conflict and severity.
        # 14. detect_indirect_conflict : Chatbot can detect indirect conflict and severity.
"""

    return message

def approved_file_logic(slack_code, approve_set, remove_list):
    print(slack_code)
    print("approve !! : " + str(approve_set))
    print("remove !! : " + str(remove_list))
    w_db = work_database()
    approve_list = list(approve_set)

    if(len(approve_list) != 0):
        w_db.add_approved_list(slack_code=slack_code,
                               req_approved_set=approve_set)
        message = random.choice(shell_dict['feat_ignore_file'])

        print(approve_list)
        message = message.format(approve_list[0])

    if(len(remove_list) != 0):
        w_db.remove_approved_list(slack_code=slack_code,
                                  remove_approve_list=remove_list)

        message = random.choice(shell_dict['feat_unignore_file'])
        message = message.format(remove_list[-1])

    w_db.close()
    return message


def lock_file_logic(slack_code, request_lock_set, remove_lock_list, lock_time):
    w_db = work_database()

    m1 = ""
    m2 = ""

    if(request_lock_set != {}):
        message = random.choice(shell_dict['feat_lock_file'])
        w_db.add_lock_list(slack_code, request_lock_set, lock_time)
        #m1 = "add lock file : " + str(request_lock_set)
        ele = ','.join(list(request_lock_set))
        message = message.format(ele)
    if(remove_lock_list != []):
        message = random.choice(shell_dict['feat_unlock_file'])
        w_db.remove_lock_list(slack_code, remove_lock_list)
        #m2 = "remove lock file : " +str(remove_lock_list)
        ele = ','.join(remove_lock_list)
        message = message.format(ele)

    # message = m1 + " / " + m2


    w_db.close()
    return message


def code_history_logic(slack_code, file_path, start_line, end_line):
    w_db = work_database()

    project_name = w_db.read_project_name(slack_code)
    engaging_user_list = get_user_email(project_name, file_path, start_line, end_line)

    #message = "This is code history : " + str(engaging_user_list)

    message = random.choice(shell_dict['feat_history_logic'])
    user_name = ""
    for name in engaging_user_list:
        nickname = w_db.convert_git_id_to_slack_id(name)
        user_name = user_name + nickname + ', '
    user_name = user_name[:-2]
    nickname = w_db.convert_git_id_to_slack_id(user_name)
    message =message.format(nickname,start_line,end_line)

    w_db.close()
    return message

def ignore_file_logic(slack_code, ignore_list, approval):
    w_db = work_database()
    print("ignore : " + str(ignore_list))
    project_name = w_db.read_project_name(slack_code)
    w_db.add_update_ignore(project_name, ignore_list, slack_code, approval)
    message = ""

    if approval == 1 and ignore_list == 1:
        message = random.choice(shell_dict['feat_ignore_alarm_direct'])
    elif approval == 1 and ignore_list == 2:
        message = random.choice(shell_dict['feat_ignore_alarm_indirect'])
    elif approval == 0 and ignore_list == 1:
        message = random.choice(shell_dict['feat_unignore_alarm_direct'])
    elif approval == 0 and ignore_list == 2:
        message = random.choice(shell_dict['feat_unignore_alarm_indirect'])
    w_db.close()
    return message


def check_conflict_logic(slack_code, file_name):
    w_db = work_database()
    message = ""

    project_name = w_db.read_project_name(slack_code)
    print("project_ name test : ", project_name)
    direct_conflict_flag, indirect_conflict_flag = w_db.is_conflict(project_name, slack_code, file_name)

    if((direct_conflict_flag == True) and (indirect_conflict_flag == True)):
        message = random.choice(shell_dict['feat_conflict_di'])
    elif((direct_conflict_flag == True) and (indirect_conflict_flag == False)):
        message = random.choice(shell_dict['feat_conflict_d'])
    elif((direct_conflict_flag == False) and (indirect_conflict_flag == True)):
        message = random.choice(shell_dict['feat_conflict_i'])
    else:
        message = "I think it'll not cause any conflict."

    w_db.close()
    return message


def other_working_status_logic(slack_code, slack_name, git_id):
    w_db = work_database()

    working_data = w_db.get_user_working_status(git_id)

    message = random.choice(shell_dict['feat_working_status'])
    message = message.format(slack_name, working_data)

    w_db.close()
    return message


def send_message_channel_logic(channel, msg, user_name):
    msg = msg.replace("?", "")
    channel_msg = user_name + " announce : " + msg
    send_channel_message(channel, channel_msg)
    message = random.choice(shell_dict['feat_announce'])
    message = message.format(channel)
    return message


def send_message_direct_logic(slack_code, msg, user_name):
    w_db = work_database()

    target_user = w_db.slack_code_to_slack_name(slack_code)
    msg = msg.replace("?","")
    msg = user_name + " gives message : " + msg
    send_direct_message(slack_code, msg)
    message = random.choice(shell_dict['feat_send_message_user'])
    message = message.format(target_user)
    w_db.close()
    return message


# Finn can not
def recommend_solve_conflict_logic(user1_git_id, user2_git_id):
    w_db = work_database()

    u1, w1, u2, w2 = w_db.recommendation(user1_git_id, user2_git_id)
    user1_slack_id = w_db.convert_git_id_to_slack_id(u1)
    user2_slack_id = w_db.convert_git_id_to_slack_id(u2)

    if u1 == user1_git_id:
        message = random.choice(shell_dict['feat_recommend_change'])
        message = message.format(user2_slack_id, user2_slack_id)
    else:
        message = random.choice(shell_dict['feat_recommend_not_change'])
        message = message.format(user1_slack_id, user1_slack_id)

    w_db.close()
    return message


def greeting_logic(slack_code):
    w_db = work_database()
    message = ""

    last_connection = w_db.user_recognize(slack_code)

    if(last_connection == 1):
        message = random.choice(shell_dict['feat_greetings'])

    # Finn can not
    elif(last_connection == 2):
        message = random.choice(shell_dict['feat_greetings2'])
    elif(last_connection == 3):
        message = random.choice(shell_dict['feat_greetings3'])
    else:
        message = random.choice(shell_dict['feat_greetings'])

    w_db.close()

    return message


def bye_logic():
    message = random.choice(shell_dict['feat_goodbye'])
    return message



shell_dict = dict()

for path, dirs, files in os.walk('../situation_shell') :
    for file in files :
        file_name, ext = os.path.splitext(file)
        if ext == '.txt' :
            shell_dict[file_name] = list()
            with open(os.path.join(path, file) , 'r', encoding="UTF-8") as f :
                for line in f.readlines() :
                    shell_dict[file_name].append(line.strip())
