import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
# from pydantic_ai import Agent # Removed to use raw client
# from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

class BlogPost(BaseModel):
    title: str = Field(description="Catchy title for the blog post")
    content: str = Field(
        description=(
            "The main story/article in well-formatted markdown. "
            "Use headers, bullet points, and emphasis where appropriate."
        )
    )
    tags: List[str] = Field(description="List of 3-5 relevant tags")
    summary: str = Field(description="A 2-3 sentence summary for social media or SEO")

class GeneratorService:
    def __init__(self):
        # 1. Credentials Binding
        # The user has OPENROUTER_API_KEY. We must map it to OPENAI_API_KEY
        # for PydanticAI to detect it natively without constructor args.
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
             # Fallback if they happen to use the standard one
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("Missing API Key: OPENROUTER_API_KEY not found in environment.")

        # Set the environment variables that PydanticAI/OpenAI read automatically
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

import re
import json

class GeneratorService:
    def __init__(self):
        self.primary_model_name = os.getenv("MODEL_PRIMARY", "xiaomi/mimo-v2-flash:free")

        # 2. Canonical Initialization
        # Use AsyncOpenAI directly to bypass any tool-forcing logic in PydanticAI
        self.client = AsyncOpenAI(
            base_url=os.environ["OPENAI_BASE_URL"],
            api_key=os.environ["OPENAI_API_KEY"]
        )
        
        # We manually construct the system prompt
        self.system_prompt = (
            "You are a 'TL;DR' Efficiency Expert. "
            "Your task: Compress the input text into a concise, high-density summary accessible to both noobs and pros. "
            "Constraint: Maximum efficiency. No fluff. No long paragraphs. "
            "You MUST return a valid JSON object matching this EXACT schema:\n"
            "{\n"
            '  "title": "A Catchy Title",\n'
            '  "content": "## 🚀 The Gist\\n(One powerful sentence)\\n\\n## 🧠 Key Details\\n- (Bullet point)\\n- (Bullet point)\\n\\n## 💡 Why It Matters\\n(Strategic insight)",\n'
            '  "tags": ["tag1", "tag2", "tag3"],\n'
            '  "summary": "A 2-sentence summary for SEO."\n'
            "}\n\n"
            "IMPORTANT: The 'content' field must contain the Markdown formatted text. "
            "Do NOT output just the content. You must wrap it in the JSON structure above. "
            "Do NOT use tools. Output strictly raw JSON."
        )

    async def generate_blog(self, crawled_content: str) -> BlogPost:
        """
        Generates a blog post from the crawled content using raw OpenAI client.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.primary_model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": crawled_content}
                ],
                # Explicitly disable tools for free models to avoid 404
                tool_choice="none",
                # Low temperature for strict adherence to instructions
                temperature=0.2,
                max_tokens=1000
            )
            
            # Clean and parse the output
            raw_text = response.choices[0].message.content
            print(f"[DEBUG] Raw output: {raw_text[:100]}...")
            
            # Robust JSON extraction using regex
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                clean_text = match.group(0)
            else:
                # Fallback to cleanup if regex fails
                clean_text = raw_text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text[7:]
                if clean_text.startswith("```"):
                    clean_text = clean_text[3:]
                if clean_text.endswith("```"):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()
            
            # Validate against schema
            # If plain json load fails, let pydantic try
            return BlogPost.model_validate_json(clean_text)
            
        except Exception as e:
            print(f"Generation Error: {e}")
            raise e
