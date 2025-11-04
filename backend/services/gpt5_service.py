"""GPT-5 service for image analysis and search."""
import os
import base64
import json
from typing import Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    
    metadata = json.loads(response.choices[0].message.content)
    return metadata


def chat_with_screenshots(query: str, screenshots_data: List[Dict[str, Any]], conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """Chat with an agent that has access to screenshot metadata and can answer questions."""
    
    # Prepare screenshots context for the agent
    screenshots_context = []
    for screenshot in screenshots_data:
        screenshots_context.append({
            "id": screenshot["id"],
            "filename": screenshot["filename"],
            "metadata": screenshot["metadata"]
        })
    
    system_prompt = f"""You are a helpful AI assistant with access to a user's screenshot database. You can search through screenshots, answer questions about them, and have natural conversations.

Available Screenshots Database:
{json.dumps(screenshots_context, indent=2)}

Your capabilities:
1. Search and find relevant screenshots based on user queries
2. Answer questions about screenshot content and details
3. Provide insights and summaries about the screenshots
4. Have natural conversations about the images

When responding:
- If the user is searching for screenshots, identify relevant ones and explain why they match
- If asking about details, reference the metadata to answer
- Be conversational and helpful
- Use emojis occasionally to be friendly

You must ALWAYS respond in this JSON format:
{{
  "message": "Your conversational response to the user",
  "results": [
    {{
      "id": screenshot_id,
      "filename": "filename.png",
      "confidence": 0.95,
      "reason": "Why this screenshot is relevant"
    }}
  ]
}}

- Include "results" array with relevant screenshots (can be empty if just chatting)
- Only include screenshots with confidence > 0.3
- The "message" should always be present with your response
"""

    # Build conversation messages
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current query
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return {
        "message": result.get("message", ""),
        "results": result.get("results", [])
    }

