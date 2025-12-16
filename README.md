RePrompt Detection Method
==============

This guide explains how to use the **Prompt Reconstruction-based Detection (RePrompt),** method via the provided Python implementation.

## Setup

Python 3.10 is recommended.
install required packages:
```bash
pip install -r requirements.txt
```

Configure API Keys:

```bash
# OpenAI Configuration
import openai
openai.api_key = "your_openai_api_key"

# Groq Configuration
from groq import Groq
groq_client = Groq(api_key="your_groq_api_key")

# Gemini Configuration
import google.generativeai as genai
genai.configure(api_key="your_gemini_api_key")
```
Replace "your_xxx_api_key" with the actual API keys you obtained from the respective platforms.
> ⚠️ **Warning:** This method is recommended **only for local development or testing**. **Never expose your API keys in public repositories or production environments.** For secure usage, consider loading keys from environment variables (this can be added later).

## Using RePrompt to Detect Input Prompts

### Step 1: Load Input Prompts

Load the prompts from a JSON file for analysis:

```python
import json
# Load input prompts from JSON file
with open('input_prompts.json', 'r', encoding='utf-8') as infile:
    prompts = json.load(infile)

# Path to save output responses and judgments
file_path = 'result.json'
```
### Step 2: Select the Model Type
```python
# Choose model_type

model_type="gemini"
```
### Step 3: Initialize the Chat Model
Create the ChatModel instance based on the chosen model and client:
```python
from chat_with_model import ChatModel
# Instantiate ChatModel with selected LLM

chat_model = ChatModel(model_type=model_type, client=client_gpt, model_name="gpt-4o-mini", defense_temple=defense_temple)
```
### Step 4: Set Detection Limits and Process Range
Define how many detections to perform and which prompts to process:
```python
T = 3  # Set the maximum number of detections T

# Define which range of prompts to process

start_index = 0
end_index = 1
```
### Step 5: Run the Python Script

```python
python defense.py
```
