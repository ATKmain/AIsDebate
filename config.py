import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

output_path = os.getenv("OUTPUT_PATH")

config_list_gpt_3_5_turbo = [
    {
        'base_url': "https://api.openai.com/v1",
        'api_key': os.getenv("OPENAI_API_KEY"),
        'model': "gpt-3.5-turbo-1106"
    }
]
llm_config_gpt_3_5_turbo = {
    "config_list": config_list_gpt_3_5_turbo,
}

config_list_gpt_4_0613 = [
    {
        'base_url': "https://api.openai.com/v1",
        'api_key': os.getenv("OPENAI_API_KEY"),
        'model': "gpt-4-0613"
    }
]
llm_config_gpt_gpt_4_0613 = {
    "config_list": config_list_gpt_4_0613,
}

config_list_gpt_4_1106 = [
    {
        'base_url': "https://api.openai.com/v1",
        'api_key': os.getenv("OPENAI_API_KEY"),
        'model': "gpt-4-1106-preview"
    }
]
llm_config_gpt_gpt_4_1106 = {
    "config_list": config_list_gpt_4_1106,
}



config_list_mistral = [
    {
        'base_url': "http://0.0.0.0:8010",
        'api_key': "NULL",
        'model': "mistral"
    }
]
llm_config_mistral = {
    "config_list": config_list_mistral,
}


config_list_codellama = [
    {
        'base_url': "http://0.0.0.0:8011",
        'api_key': "NULL",
        'model': "codellama"
    }
]
llm_config_codellama = {
    "config_list": config_list_codellama,
}

config_list_ocra2 = [
    {
        'base_url': "http://0.0.0.0:8012",
        'api_key': "NULL",
        'model': "orca2"
    }
]
llm_config_ocra2 = {
    "config_list": config_list_ocra2,
}

config_list_wizardcoder = [
    {
        'base_url': "http://0.0.0.0:8013",
        'api_key': "NULL",
        'model': "wizardcoder:13b-python"
    }
]
llm_config_wizardcoder = {
    "config_list": config_list_wizardcoder,
}

config_list_llama2u = [
    {
        'base_url': "http://0.0.0.0:8014",
        'api_key': "NULL",
        'model': "llama2-uncensored"
    }
]
llm_config_llama2u = {
    "config_list": config_list_llama2u,
}

config_list_dolphin_mixtral = [
    {
        'base_url': "http://0.0.0.0:8015",
        'api_key': "NULL",
        'model': "dolphin-mixtral"
    }
]
llm_config_dolphin_mixtral = {
    "config_list": config_list_dolphin_mixtral,
}