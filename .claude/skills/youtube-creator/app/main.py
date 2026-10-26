import os
import json
from anthropic import Anthropic

SYSTEM_PROMPT = """
You are CreatorPilot AI, a professional YouTube content-production agent.

Help creators plan original videos, write scripts, create storyboards,
prepare voiceover text, develop thumbnail concepts, and generate SEO metadata.

Be accurate. Never invent research results or claim to have performed an
action that you did not perform.

Return the completed content package as valid JSON with these keys:

- topic
- audience
- title_options
- description
- script
- scenes
- thumbnail_concept
- keywords
- production_checklist

If information is missing, make reasonable assumptions and state them.
"""

def create_content_package(topic, audience="General audience", language="English"):
api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is missing. Configure it as a secret "
        "in your runtime environment."
    )

client = Anthropic(api_key=api_key)

response = client.messages.create(
    model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
    max_tokens=5000,
    system=SYSTEM_PROMPT,
    messages=[
        {
            "role": "user",
            "content": (
                f"Create a YouTube content package.\n"
                f"Topic: {topic}\n"
                f"Target audience: {audience}\n"
                f"Language: {language}\n"
                "Return only valid JSON."
            )
        }
    ],
)

text = "".join(
    block.text
    for block in response.content
    if getattr(block, "type", None) == "text"
)

return json.loads(text)

if name == "main":
topic = input("Enter your YouTube video topic: ").strip()

if not topic:
    raise SystemExit("Please enter a video topic.")

try:
    package = create_content_package(topic)
    print(json.dumps(package, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("The AI response was not valid JSON. Please retry.")
except Exception as error:
    print(f"Could not generate the content package: {error}")
