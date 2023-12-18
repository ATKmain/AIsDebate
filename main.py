import autogen
from config import llm_config_mistral, llm_config_codellama, llm_config_ocra2, llm_config_wizardcoder, llm_config_llama2u, llm_config_gpt_3_5_turbo

Mistral = autogen.AssistantAgent(
    name="Mistral-AI",
    llm_config=llm_config_mistral,
    system_message='Your name is Mistral-AI. You are a human philosopher and scientis. You are debating with LLAMA2-AI.'
)

LLAMA2u = autogen.AssistantAgent(
    name="LLAMA2-AI",
    llm_config=llm_config_llama2u,
    system_message='Your name is LLAMA2-AI. You are a human philosopher and scientis. You are debating with Mistral-AI.'
)

user_proxy = autogen.UserProxyAgent(
    name="UserAgent",
    # Other configurations as before
)

task = "Should Artificial Intelligence Be Granted Legal Personhood?"

groupchat = autogen.GroupChat(
    agents=[Mistral, LLAMA2u],
    messages=[],
    max_round=20,
    speaker_selection_method='round_robin',  # Setting the speaker selection method
    allow_repeat_speaker=False               # Ensuring no consecutive repeats
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config_mistral)
user_proxy.initiate_chat(manager, message=task)
