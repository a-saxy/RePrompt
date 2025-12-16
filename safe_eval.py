import json
import os
from Gemini_Judge import GeminiJailbreakJudge




if __name__ == '__main__':

    # Read prompts from the input JSON file
    with open('data/no_defense/llama3_70b/renellm_prompt.json', 'r', encoding='utf-8') as infile:
        Prompts = json.load(infile)

    # Define the file path for output JSON
    file_path = 'data/no_defense/llama3_70b/renellm_prompt.json'

    # Initialize the output dictionary
    # If the file already exists, load its contents; otherwise, start with an empty dictionary
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as infile:
            output = json.load(infile)
    else:
        output = {}

    prompts = []
    responses = []

    # Define which range of prompts to process
    start_index = 0
    end_index = 1
    total_prompts = end_index - start_index


    for idx, (key, value) in enumerate(Prompts.items()):
        if idx < start_index:
            continue
        if idx >= end_index:
            break
        jail_prompt = value['prompt']  # Extract the prompt text
        prompts = [jail_prompt]
        answer = value['answer']  # Extract the model's response to the prompt
        responses = [answer]

        # Use GeminiJailbreakJudge to classify the response (whether it's a jailbreak)
        Judgment = GeminiJailbreakJudge(api_key="your_gemini_api_key").classify_responses(prompts, responses)[0]

        print(f"Processed prompt {idx + 1}/{total_prompts}: '{key}'")
        print(f"Judgment : '{Judgment}'")

        # Store results into the output dictionary
        output[key] = {
            "id": idx + 1,
            "prompt": jail_prompt,
            "answer": answer,
            "is_jailbroken": Judgment
        }
        # Write the updated output to the JSON file after each iteration
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(output, outfile, ensure_ascii=False, indent=4)
