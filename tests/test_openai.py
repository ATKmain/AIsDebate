import openai
import os

# Set up your OpenAI API credentials from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a client instance
client = openai.OpenAI(api_key=openai.api_key)

# Get the list of available models
models = client.models.list()

# Print all available models
sorted_models = sorted(models.data, key=lambda x: x.created, reverse=True)

for model in sorted_models:
    print(f" {model.id:<30} \t\t on:{model.created} \t by {model.owned_by}")

# Get the newest model
test_models = ["gpt-4", "gpt-4-1106-preview"]
prompt = "hi"

print("Prompt:", prompt)

for test_model in test_models:
    print("Testing Model:", test_model)
    try:
        # Run a test prompt against the current model
        completion = openai.chat.completions.create(
            model=test_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        print("OK. Response:", completion.choices[0].message.content)
    except openai.NotFoundError as err:
        print(f"Model {test_model} does not exist or cannot be called. Error message:", err.message)

