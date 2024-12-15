"""
Notion API Integration Tools

This module provides a comprehensive set of tools for interacting with the Notion API,
enabling the creation and manipulation of various Notion blocks and pages. It handles
all direct communication with the Notion API, providing a clean interface for creating
and modifying content.

Features:
- Page creation and management
- Rich text block creation (headings, paragraphs)
- Media block creation (images, videos, embeds)
- List management (numbered, bulleted, to-do)
- Code block creation with syntax highlighting
- Bookmark and external link integration

Environment Variables Required:
    NOTION_API_KEY: Your Notion integration token
    OPENAI_API_KEY_: Your OpenAI API key
    NOTION_ENDPOINT: Notion API endpoint (usually https://api.notion.com/v1)
    NOTION_PAGE_ID: ID of the parent page for new content

API Version: 2022-06-28
"""

import os
from typing import List
import httpx
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_")
NOTION_ENDPOINT = os.getenv("NOTION_ENDPOINT")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")


def create_notion_page(page_title):
    """
    Create a new page in Notion with the specified title and content.

    args:
        page_title: The title of the new page.
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/pages"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    properties = {"title": {"title": [{"text": {"content": page_title}}]}}

    try:
        response = httpx.post(
            url,
            headers=headers,
            json={"parent": {"page_id": page_id}, "properties": properties},
        )
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_heading_block(
    heading_type: str = "heading_1",
    content: str = "New Heading",
    is_hyperlink: bool = False,
    hyperlink_url: str = "",
    color: str = "default",
):
    """
    Add a heading block to a Notion page with the specified content.

    args:
        context_variables: The context variables containing the API key and page ID.
        heading_type: The type of heading block to add (e.g., 'heading_1', 'heading_2').
        content: The content of the heading block.
        is_hyperlink: A boolean value indicating whether the heading should be a hyperlink.
        hyperlink_url: The URL of the hyperlink.
        color: The color of the heading block.

    example usage:
        add_notion_heading_block(heading_type='heading_1', content='Lacinato Kale', is_hyperlink=False)
        add_notion_heading_block(heading_type='heading_1', content='Lacinato Kale', is_hyperlink=True, hyperlink_url='https://en.wikipedia.org/wiki/Lacinato_kale')
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    text_obj = {"type": "text", "text": {"content": content}}

    data = {
        "children": [
            {
                "object": "block",
                "type": heading_type,
                heading_type: {
                    "rich_text": [text_obj],
                    "color": color,  # Move color inside the heading block
                },
            }
        ]
    }

    if is_hyperlink:
        text_obj["text"]["link"] = {"url": hyperlink_url}

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_paragraph_block(
    content: str,
    is_hyperlink: bool = False,
    hyperlink_url: str = "",
    color: str = "default",
):
    """
    Add a paragraph block to a Notion page with the specified content.

    args:
        context_variables: The context variables containing the API key and page ID.
        content: The content of the paragraph block.
        is_hyperlink: A boolean value indicating whether the paragraph should be a hyperlink.
        hyperlink_url: The URL of the hyperlink.
        color: The color of the paragraph block.

    example usage:
        add_notion_paragraph_block(content='San Francisco is a beautiful city', is_hyperlink=False)
        add_notion_paragraph_block(content='San Francisco is a beautiful city', is_hyperlink=True, hyperlink_url='https://en.wikipedia.org/wiki/San-Francisco')
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    text_obj = {"type": "text", "text": {"content": content}}

    data = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [text_obj], "color": color},
            }
        ]
    }

    if is_hyperlink:
        text_obj["text"]["link"] = {"url": hyperlink_url}

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_code_block(code: str, language: str = "python", caption: List[str] = []):
    """
    Add a code block to a Notion page with the specified code content.

    args:
        code: The code content of the code block.
        language: The programming language of the code block.
        caption: A list of strings for the caption of the code block.
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "code",
                "code": {
                    "caption": [{"text": {"content": c}} for c in caption],
                    "rich_text": [{"type": "text", "text": {"content": code}}],
                    "language": language,
                },
            }
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_embed_block(url: str):
    """
    Add an embed block to a Notion page with the specified embed URL.

    args:
        url: The URL of the content to embed in the embed block.
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {"children": [{"object": "block", "type": "embed", "embed": {"url": url}}]}

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_youtube_url_block(video_url: str):
    """
    Add a video block to a Notion page with the specified video URL.

    args:
        video_url: The URL of the video to embed in the video block.
    """
    if "youtube.com" not in video_url:
        return {"error": "Invalid YouTube video URL"}
    elif "watch?v=" not in video_url:
        return {"error": "Invalid YouTube video URL"}

    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "video",
                "video": {"type": "external", "external": {"url": video_url}},
            }
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_image_block(image_url: str):
    """
    Add an image block to a Notion page with the specified image URL.

    args:
        image_url: The URL of the image to embed in the image block.
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {"type": "external", "external": {"url": image_url}},
            }
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_bookmark_block(link: str, caption: str):
    """
    Add a bookmark block to a Notion page with the specified link and caption.

    args:
        link: The URL of the bookmarked link.
        caption: The caption for the bookmark block.
    """
    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "bookmark",
                "bookmark": {"url": link, "caption": [{"text": {"content": caption}}]},
            }
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_number_list_block(items: List[str]):
    """
    Add a number list block to a Notion page with the specified items.

    args:
        items: A list of strings representing the items in the number list.
    """
    if isinstance(items, str):
        items = [item.strip() for item in items.split(",")]

    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                },
            }
            for item in items
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_bulleted_list_block(items: List[str]):
    """
    Add a bulleted list block to a Notion page with the specified items.

    args:
        items: A list of strings representing the items in the bulleted list.
    """
    if isinstance(items, str):
        items = [item.strip() for item in items.split(",")]

    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                },
            }
            for item in items
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}


def add_notion_to_do_block(items: List[str], checked: bool = False):
    """
    Add a to-do block to a Notion page with the specified content.

    args:
        items: The content of the to-do block. Must be a list.
        checked: A boolean value indicating whether the to-do block is checked.
    """
    if isinstance(items, str):
        items = [item.strip() for item in items.split(",")]

    api_key = NOTION_API_KEY
    page_id = NOTION_PAGE_ID

    url = f"{NOTION_ENDPOINT}/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": item}}],
                    "checked": checked,
                },
            }
            for item in items
        ]
    }

    try:
        response = httpx.patch(url, headers=headers, json=data)
        return response.json()
    except httpx.ReadTimeout:
        return {"error": "Request timed out"}
