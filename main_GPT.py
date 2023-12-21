import autogen
import config
import json
import datetime


agents = [
    {"name": "Mixtral-AI", "llm_config": config.llm_config_dolphin_mixtral},
    {"name": "GPT-AI",     "llm_config": config.llm_config_gpt_gpt_4_0613},
]
agent1 = autogen.AssistantAgent(
    name=agents[0]['name'],
    llm_config=agents[0]['llm_config'],
    system_message='Your name is '+agents[0]['name']+'. You are a human philosopher and scientist. You are debating with '+agents[1]['name']+'. Focus on the core discussion points and avoid formalities such as expressions of gratitude or appreciation. Let\'s keep the conversation concise and directly related to the topic. Do not summerise discussion at all.'
)

agent2 = autogen.AssistantAgent(
    name=agents[1]['name'],
    llm_config=agents[1]['llm_config'],
    system_message='Your name is GPT-AI. You are a human philosopher and scientist. You are debating with Mixtral-AI. Focus on the core discussion points and avoid formalities such as expressions of gratitude or appreciation. Let\'s keep the conversation concise and directly related to the topic.'
)

user_proxy = autogen.UserProxyAgent(
    name="UserAgent",
    # Other configurations as before
)

#task = "Should Artificial Intelligence Be Granted Legal Personhood?"
task = "Explore the potential of generative AI in creating personalized learning experiences. How might it adapt educational content to suit individual learning styles and needs?"

groupchat = autogen.GroupChat(
    agents=[agent1, agent2],
    messages=[],
    max_round=15,
    speaker_selection_method='round_robin',  # Setting the speaker selection method
    allow_repeat_speaker=False               # Ensuring no consecutive repeats
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=config.llm_config_dolphin_mixtral)
user_proxy.initiate_chat(manager, message=task)

# Writing the result to a text file
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

file_name_text = f'{config.output_path}AIsDebate_{agents[0]["name"]}_vs_{agents[1]["name"]}_{formatted_datetime}.txt'
with open(file_name_text, 'w') as file:
    for message in groupchat.messages:
        file.write(f"{message['sender']}: {message['content']}\n")

# Writing the result to a JSON file
file_name_json = f'{config.output_path}AIsDebate_{agents[0]["name"]}_vs_{agents[1]["name"]}_{formatted_datetime}.json'
with open(file_name_json, 'w') as file:
    json.dump(groupchat.messages, file)
