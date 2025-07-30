import json
import os
from pydantic import BaseModel

from anthropic.types import TextBlock
import anthropic


class PageElement(BaseModel):
    id: str
    iframe_path: str | None


def locate_element_prompt(prompt: str, accessibility_tree: dict) -> str:
    return f"""
Given the following HTML structure, find the element that matches user's instruction. 
 
User's instruction: {prompt}
 
HTML structure: {json.dumps(accessibility_tree)}
 
Only return the element ID without any other content without any quote. If the element cannot be found, return empty string.
    """


class WebAgent:
    """
    Base agent class for general browser automation.

    Takes a browser instance and uses Claude to perform dynamic actions based on goals.

    Base class sets up the anthropic client, and provides basic functionality like taking screenshots
    """

    def __init__(self):
        """
        Create a new GenericAgent instance.

        Args:
            browser: Browser instance for interaction
            api_key: Claude API key (optional, defaults to ANTHROPIC_API_KEY env var)
        """
        self.model = "claude-3-7-sonnet-20250219"
        self.max_iterations = 100  # Maximum number of actions to prevent infinite loops

        # Use API key from environment variable if not provided
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not anthropic_api_key:
            raise ValueError(
                "Claude API key not provided. Please provide it via the api_key parameter "
                "or set the ANTHROPIC_API_KEY environment variable."
            )

        self.client = anthropic.Anthropic(api_key=anthropic_api_key)

    def query_element(
        self, prompt: str, accessibility_tree: dict
    ) -> PageElement | None:
        text_prompt = locate_element_prompt(prompt, accessibility_tree)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system="""Find an element that best matches user's instruction""",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text_prompt,
                        }
                    ],
                }
            ],
        )
        for block in response.content:
            if block.type == "text":
                if isinstance(block, TextBlock):
                    content = block.text
                    continue
        element_id = content if content else None
        return PageElement(id=element_id, iframe_path=None)
