import os
import json
import requests

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


def summarize_meeting(notes):

    if not API_KEY:

        return {
            "error": "OPENROUTER_API_KEY is not configured."
        }


    url = (
        "https://openrouter.ai/api/v1/"
        "chat/completions"
    )


    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


    data = {

        "model":
            "google/gemma-4-26b-a4b-it:free",

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

- task = actual task only
- owner = responsible person
- priority = High, Medium, or Low
- deadline = deadline if mentioned
- owner = "N/A" if unknown
- deadline = "N/A" if unknown

For every risk:

- risk = description of risk
- impact = High, Medium, or Low
- mitigation = how to reduce the risk

Do not return markdown.
Do not explain.
Return JSON only.
"""
            },

            {
                "role": "user",
                "content": notes
            }

        ]
    }


    # =========================
    # API Request
    # =========================

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

    except requests.RequestException as e:

        return {
            "error":
                f"API request failed: {str(e)}"
        }


    # =========================
    # API Error
    # =========================

    if response.status_code != 200:

        try:

            error_data = response.json()

            message = (
                error_data
                .get("error", {})
                .get("message", response.text)
            )

        except Exception:

            message = response.text


        return {
            "error":
                f"API Error {response.status_code}: {message}"
        }


    # =========================
    # Parse API Response
    # =========================

    try:

        result = response.json()

    except ValueError:

        return {
            "error":
                "The API returned an invalid response."
        }


    if "choices" not in result:

        return {
            "error":
                "The AI response did not contain choices."
        }


    try:

        content = (
            result["choices"][0]
            ["message"]["content"]
        )

    except (KeyError, IndexError, TypeError):

        return {
            "error":
                "Unable to read AI response."
        }


    if not content:

        return {
            "error":
                "The AI returned an empty response."
        }


    # =========================
    # Clean JSON
    # =========================

    content = content.strip()

    if content.startswith("```json"):

        content = content[
            len("```json"):
        ]

    elif content.startswith("```"):

        content = content[
            len("```"):
        ]


    if content.endswith("```"):

        content = content[
            :-3
        ]


    content = content.strip()


    # =========================
    # Parse JSON
    # =========================

    try:

        parsed = json.loads(
            content
        )

    except json.JSONDecodeError:

        # Try extracting JSON object
        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1:

            try:

                parsed = json.loads(
                    content[start:end + 1]
                )

            except json.JSONDecodeError:

                return {
                    "error":
                        "AI returned invalid JSON."
                }

        else:

            return {
                "error":
                    "AI returned invalid JSON."
            }


    # =========================
    # Validate Structure
    # =========================

    if not isinstance(parsed, dict):

        return {
            "error":
                "AI response is not a JSON object."
        }


    parsed.setdefault(
        "summary",
        ""
    )

    parsed.setdefault(
        "action_items",
        []
    )

    parsed.setdefault(
        "risks",
        []
    )

    parsed.setdefault(
        "next_steps",
        []
    )


    return parsed