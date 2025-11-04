"""GPT-5 service for image analysis and search."""
import os
import base64
from typing import Dict, Any, List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path: str) -> str:
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_image(image_path: str) -> Dict[str, Any]:
    """Analyze an image using GPT-5 vision API and return structured metadata."""
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o",  # Using gpt-4o as fallback until gpt-5 is available in your account
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analyze this screenshot and extract the following information in JSON format:
{
  "description": "A detailed description of what's shown in the image",
  "text_content": "Any visible text (OCR), transcribe all readable text",
  "visual_elements": ["list", "of", "key", "visual", "elements"],
  "colors": ["dominant", "colors"],
  "context": "What type of screenshot is this (e.g., code, email, graph, document)",
  "keywords": ["searchable", "keywords"],
  "summary": "Brief one-line summary"
}

Please be thorough with text extraction as this will be used for search."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
        response_format={"type": "json_object"}
    )
    
    import json
    metadata = json.loads(response.choices[0].message.content)
    return metadata


def search_screenshots(query: str, screenshots_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Search screenshots using GPT-5 agent to find relevant matches."""
    
    # Prepare screenshots context for the agent
    screenshots_context = []
    for screenshot in screenshots_data:
        screenshots_context.append({
            "id": screenshot["id"],
            "filename": screenshot["filename"],
            "metadata": screenshot["metadata"]
        })
    
    system_prompt = """You are a screenshot search assistant. Your job is to analyze a user's query and find the most relevant screenshots from the indexed database.

Given a user query and a list of screenshots with their metadata, you need to:
1. Understand what the user is looking for
2. Analyze each screenshot's metadata to determine relevance
3. Rank screenshots by relevance (0.0 to 1.0 confidence score)
4. Return the top 5 most relevant results

Return your response in this JSON format:
{
  "results": [
    {
      "id": screenshot_id,
      "filename": "filename.png",
      "confidence": 0.95,
      "reason": "Brief explanation why this matches"
    }
  ]
}

Only include screenshots with confidence > 0.3. If no screenshots match well, return an empty results array."""

    user_message = f"""User Query: "{query}"

Available Screenshots:
{json.dumps(screenshots_context, indent=2)}

Find the top 5 most relevant screenshots for this query."""

    response = client.chat.completions.create(
        model="gpt-4o",  # Using gpt-4o as fallback until gpt-5 is available in your account
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        response_format={"type": "json_object"}
    )
    
    import json
    result = json.loads(response.choices[0].message.content)
    return result.get("results", [])

