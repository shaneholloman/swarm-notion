"""
Multi-agent system for Notion integration using the Swarm framework.

This module implements a hierarchical agent system for managing Notion content:
- Delegate Agent: Routes tasks to specialized agents
- Page Agent: Handles page-level operations
- Block Agent: Manages block-level content

Each agent is configured with specific capabilities and can transfer control to other
agents as needed based on the task requirements.
"""

from swarm import Agent
from swarm.types import Result
from prompts import delegate_agent_prompt, page_agent_prompt, block_agent_prompt
from tools import (
    NOTION_API_KEY,
    NOTION_PAGE_ID,
    create_notion_page,
    add_notion_heading_block,
    add_notion_paragraph_block,
    add_notion_code_block,
    add_notion_embed_block,
    add_notion_youtube_url_block,
    add_notion_image_block,
    add_notion_bookmark_block,
    add_notion_number_list_block,
    add_notion_bulleted_list_block,
    add_notion_to_do_block,
)

MODEL = "gpt-4o-mini"


def transfer_to_notion_delegate_agent():
    """
    Transfer control to the Notion Delegate Agent.

    This function creates a Result object containing the delegate agent and necessary
    context variables for Notion API authentication and page identification.

    Returns:
        Result: Object containing the delegate agent and context variables
    """
    return Result(
        agent=notion_delegate_agent,
        context_variables={"api_key": NOTION_API_KEY, "page_id": NOTION_PAGE_ID},
    )


def transfer_to_notion_page_agent():
    """
    Transfer control to the Notion Page Agent.

    This function creates a Result object containing the page agent and necessary
    context variables for Notion API authentication and page identification.

    Returns:
        Result: Object containing the page agent and context variables
    """
    return Result(
        agent=notion_page_agent,
        context_variables={"api_key": NOTION_API_KEY, "page_id": NOTION_PAGE_ID},
    )


def transfer_to_notion_block_agent():
    """
    Transfer control to the Notion Block Agent.

    This function creates a Result object containing the block agent and necessary
    context variables for Notion API authentication and page identification.

    Returns:
        Result: Object containing the block agent and context variables
    """
    return Result(
        agent=notion_block_agent,
        context_variables={"api_key": NOTION_API_KEY, "page_id": NOTION_PAGE_ID},
    )


# Initialize Delegate Agent with capabilities to transfer to Page and Block agents
notion_delegate_agent = Agent(
    name="Notion Delegate Agent",
    model=MODEL,
    instructions=delegate_agent_prompt,
    functions=[transfer_to_notion_page_agent, transfer_to_notion_block_agent],
)

# Initialize Page Agent with capability to transfer back to Delegate agent
notion_page_agent = Agent(
    name="Notion Page Agent",
    model=MODEL,
    instructions=page_agent_prompt,
    functions=[transfer_to_notion_delegate_agent],
)

# Initialize Block Agent with capability to transfer back to Delegate agent
notion_block_agent = Agent(
    name="Notion Block Agent",
    model=MODEL,
    instructions=block_agent_prompt,
    functions=[transfer_to_notion_delegate_agent],
)

# Extend Page Agent with page creation capability
notion_page_agent.functions.extend([create_notion_page])

# Extend Block Agent with all block manipulation capabilities
notion_block_agent.functions.extend(
    [
        add_notion_heading_block,
        add_notion_paragraph_block,
        add_notion_code_block,
        add_notion_embed_block,
        add_notion_youtube_url_block,
        add_notion_image_block,
        add_notion_bookmark_block,
        add_notion_number_list_block,
        add_notion_bulleted_list_block,
        add_notion_to_do_block,
    ]
)
