# Description: This is the main file to run the debate between two LLM AI agents
# Author: Arash Khalilian (ATK)

import autogen
import config
import json
import datetime

setup = {
    "debate_question": "Explore the potential of generative AI in creating personalized learning experiences. How might it adapt educational content to suit individual learning styles and needs specially for schools?",
    "max_total_rounds": 50,
    "max_initial_rounds": 4,
    "max_questions": 2,
    "max_rounds_for_each_question": 2,
    "manager_llm_config" : config.llm_config_mistral ,
    "speaker_selection_method" : "round_robin" #"round_robin",

}

agents = [
    {"name": "Audience-Representative", "llm_config": config.llm_config_mistral},
    {"name": "Mistral1", "llm_config": config.llm_config_mistral},
    {"name": "Mistral2", "llm_config": config.llm_config_mistral},
]

#    {"name": "Mixtral-AI", "llm_config": config.llm_config_dolphin_mixtral},
#    {"name": "GPT-AI",     "llm_config": config.llm_config_gpt_gpt_4_0613},   

print("#######################################################")
print("################## Debate Question ####################")
print(setup["debate_question"])
print("#######################################################")
print("################## Agent Specification #################")   
print(f"## Agent 1: {agents[1]['name']} - Model: {agents[1]['llm_config']}")
print(f"## Agent 2: {agents[2]['name']} - Model: {agents[2]['llm_config']}")
print("#######################################################")
print("################## Debate Transcript ###################")
print("#######################################################")


user_proxy = autogen.UserProxyAgent(
    name=agents[0]['name'],
    llm_config=agents[0]['llm_config'],
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    system_message=f'''
        Your name is "Audience Representative" and you are the representative of the audience. You start the debate by asking the debate question. 
        Listen to the debate and after {setup["max_initial_rounds"]} rounds of debate between debaters ask only one questions from the debaters on behalf of the audience related to topic and their debate. Keep the questions concise and directly related to the topic.
        Do not summarize the discussion and do not generate debate.        
    '''
)

agent1 = autogen.AssistantAgent(
    name=agents[1]['name'],
    llm_config=agents[1]['llm_config'],
    system_message='Your name is ' + agents[1]['name'] + '. You are a human philosopher and scientist. You are debating. Focus on the core discussion points and avoid formalities such as expressions of gratitude or appreciation. Let\'s keep the conversation concise and directly related to the topic. Do not summarize previous discussions at all.'
)

agent2 = autogen.AssistantAgent(
    name=agents[2]['name'],
    llm_config=agents[2]['llm_config'],
    system_message='Your name is ' + agents[2]['name'] + '. You are a human philosopher and scientist. You are debating. Focus on the core discussion points and avoid formalities such as expressions of gratitude or appreciation. Let\'s keep the conversation concise and directly related to the topic. Do not summarize previous discussions at all.'
)

# Create a groupchat
groupchat = autogen.GroupChat(
    agents=[agent1, agent2, user_proxy ], # Setting the agents
    messages=[],  
    max_round=setup['max_total_rounds'],
    speaker_selection_method= setup["speaker_selection_method"] ,  # Setting the speaker selection method
    allow_repeat_speaker=False  # Ensuring no consecutive repeats of speakers
)

# Create a manager
manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config= setup['manager_llm_config'],
    system_message=f'''
        Choose one agent to answer each time. Listen to the debate and after {setup["max_initial_rounds"]} rounds of debate between debaters ask questions from the debaters on behalf of the audience related to topic and their debate. Keep the questions concise and directly related to the topic.
        Let them debate about the question for {setup["max_rounds_for_each_question"]} rounds and then ask the next audience question. Only ask {setup["max_questions"]} question.
        After the final debate on the last question. Evaluate the debate and give a grade from 0 to 100 to each debater and terminate the discussion/debate.
        Do not summarize the discussion at all.
        '''
)

# Start the debate
user_proxy.initiate_chat(manager, message=setup['debate_question'])

'''
# New variables to track rounds and switch modes
initial_round_counter = 0
question_counter = 0
question_round_counter = 0

# Process messages
while groupchat.is_active:
    if initial_round_counter < setup['max_initial_rounds']:
        manager.process_next_message()
        initial_round_counter += 1
        
    elif question_counter < setup['max_question_rounds'] and (question_round_counter == 0 or question_round_counter >= setup['max_rounds_for_each_question']) :
        # Change speaker to user_proxy for asking questions
        user_proxy.ask_followup_question(manager)  # Implement this method as per your requirements
        question_counter += 1
        question_round_counter = 1
    elif question_round_counter > 0 and question_round_counter < setup['max_rounds_for_each_question']:
        # continue answering question
        manager.process_next_message()
        question_round_counter += 1
    else :
        # evaluate and finish the debate
        user_proxy.evaluate(manager)
        groupchat.is_active = False
        break

'''

# Writing the result to a text file
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
formatted_text_datetime = current_datetime.strftime("%Y %m %d  %H %M %S")


# Writing the result to a text file
file_name_text = f'{config.output_path}AIsDebate_{agents[0]["name"]}_vs_{agents[1]["name"]}_{formatted_datetime}.txt'
with open(file_name_text, 'w') as file:
    file.write(f"# Debate Question: {setup['debate_question']}\n")
    file.write(f"# Date and Time: {formatted_text_datetime}\n")
    file.write("# Agents Specification:\n")
    file.write(f"## Agent 1: {agent1.name} - Model: {agent1.llm_config}\n")
    file.write(f"## Agent 2: {agent2.name} - Model: {agent2.llm_config}\n")
    file.write("#######################################################\n")
    for message in groupchat.messages:
        file.write(f"{message['name']}: {message['content']}\n")
print(f"# Result saved to {file_name_text}")


# Writing the result to a JSON file
file_name_json = f'{config.output_path}AIsDebate_{agents[0]["name"]}_vs_{agents[1]["name"]}_{formatted_datetime}.json'
debate_info = {
    "debate_question": setup["debate_question"],
    "date_and_time": formatted_text_datetime,
    "agent1": {
        "name": agent1.name,
        "model": agent1.llm_config
    },
    "agent2": {
        "name": agent2.name,
        "model": agent2.llm_config
    },
    "messages": groupchat.messages
}
with open(file_name_json, 'w') as file:
    json.dump(debate_info, file)
print(f"# Result saved to {file_name_json}")