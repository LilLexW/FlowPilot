import os
import json
import requests
from dotenv import load_dotenv


load_dotenv(".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")

def summarize_meeting(notes):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemma-4-26b-a4b-it:free",
        "max_tokens": 800,

        "messages": [
            {
                "role": "system",

                "content": """
You are an AI project manager.

Analyze the meeting notes and extract structured project information.

Return ONLY valid JSON.

Use exactly this structure:

{
  "summary": "",
  "action_items": [
    {
      "task": "",
      "owner": "",
      "priority": "",
      "deadline": ""
    }
  ],
  "risks": [
    {
      "risk": "",
      "impact": "",
      "mitigation": ""
    }
  ],
  "next_steps": []
}

For every action item:

- "task" should contain only the actual task.
- "owner" should contain the person responsible for the task.
- "priority" should be High, Medium, or Low.
- "deadline" should contain the deadline if mentioned.
- If the owner is not mentioned, use "N/A".
- If the deadline is not mentioned, use "N/A".

For every risk:

- "risk" should describe the risk.
- "impact" should be High, Medium, or Low.
- "mitigation" should describe how to reduce the risk.

Do not return markdown.
Do not explain anything.
Return valid JSON only.
"""
            },

            {
                "role": "user",
                "content": notes
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

    except requests.RequestException as e:

        return {
            "error": f"API request failed: {str(e)}"
        }

    if response.status_code != 200:

        return {
            "error": (
                f"API Error {response.status_code}: "
                f"{response.text}"
            )
        }

    result = response.json()

    if "choices" not in result:
        return str(result)

    content = result["choices"][0]["message"]["content"]

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:

        return json.loads(content)

    except json.JSONDecodeError:

        return {
            "error": "AI returned invalid JSON.",
            "raw_output": content
        }
