"""
Notion Agent CLI Application

This module implements a command-line interface for interacting with Notion through
natural language commands. It uses the Swarm framework to manage a multi-agent system
that can create and modify Notion pages and content.

Features:
- Interactive CLI with colored output for better user experience
- Natural language command processing
- Graceful exit handling with 'exit' or 'quit' commands
- Support for message history tracking
- Optional debug mode for development

Usage:
    python app.py

Commands:
    - Any natural language command to interact with Notion
    - 'exit' or 'quit' to terminate the application

Note:
    The application requires valid API keys for both OpenAI and Notion,
    which should be configured in the environment variables.
"""

import sys
from swarm import Swarm
from swarm.repl import run_demo_loop
from openai import OpenAI
from agents import notion_delegate_agent
from tools import OPENAI_API_KEY

if __name__ == "__main__":
    client = Swarm(OpenAI(api_key=OPENAI_API_KEY))
    print("\033[94mNotion Agent is live")

    while True:
        prompt = input("\033[92mUser\033[0m: ")
        if prompt.lower() == "exit" or prompt.lower() == "quit":
            sys.exit("Bye bye")

        messages = [
            {
                "role": "user",
                "content": f"""
                    {prompt}
                """,
            }
        ]

        response = client.run(notion_delegate_agent, messages=messages, debug=False)

        print("\033[95mNotion \033[95mAgent\033[0m:", response.messages[-1]["content"])
        print()

    # if you don't care about the keeping track of the message history, which also count
    # towards your input token, use run_demo_loop instead.
    # response = run_demo_loop(
    #     notion_delegate_agent,
    #     debug=True
    # )
