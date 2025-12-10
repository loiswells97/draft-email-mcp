#!/usr/bin/env python3

import asyncio
import os
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from email.message import EmailMessage
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.compose"]
TOKEN_PATH = os.environ.get("GOOGLE_TOKEN_PATH", "token.json")
CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials.json")

server = Server("draft-email-server")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    
async def get_email(email_id: str):
    try:
        gmail_service = get_gmail_service()
        msg = (
            gmail_service.users()
            .messages()
            .get(userId="me", id=email_id)
            .execute()
        )
        headers = msg["payload"]["headers"]
        subject = next(header["value"] for header in headers if header["name"] == "Subject")
        sender = next(header["value"] for header in headers if header["name"] == "From")

        return {
            "id": email_id,
            "sender": sender,
            "subject": subject,
            "thread_id": msg["threadId"],
            "timestamp": msg["internalDate"],
            "snippet": msg["snippet"],
        }
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def hello_world():
    return "Hello, World!"

async def get_unread_emails(limit: int = 5):
    try:
        gmail_service = get_gmail_service()
        results = (
            gmail_service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=limit)
            .execute()
        )
        messages = results.get("messages", [])
        emails = []
        for message in messages:
            email = await get_email(message["id"])
            if email:
                emails.append(email)
        return emails
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

async def create_draft_reply(email_id: str, reply_body: str):
    try:
    # create gmail api client
        gmail_service = get_gmail_service()
        original_email = await get_email(email_id)

        message = EmailMessage()
        message.set_content(reply_body)

        message["To"] = original_email["sender"]
        message["From"] = "me"
        message["Subject"] = "Re: " + original_email["subject"]
        message["In-Reply-To"] = email_id

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message, "threadId": original_email["thread_id"]}}
        draft = (
            gmail_service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        return f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}'

    except HttpError as error:
        print(f"An error occurred: {error}")
        draft = None

    return draft


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="hello_world",
            description="Say hello to the world",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_unread_emails",
            description="Get a list of unread emails",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of unread emails to retrieve",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="create_draft_reply",
            description="Create a draft reply to an email",
            inputSchema={
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The ID of the email to create a draft reply to",
                    },
                    "reply_body": {
                        "type": "string",
                        "description": "The body of the draft reply email",
                    },
                },
                "required": ["email_id", "reply_body"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "hello_world":
        greeting = hello_world()
        return [types.TextContent(type="text", text=greeting)]
    elif name == "get_unread_emails":
        limit = arguments["limit"]
        emails = await get_unread_emails(limit)
        if not emails:
            return [types.TextContent(type="text", text="✓ No unread emails found")]
        email_texts = json.dumps(emails)
        return [types.TextContent(type="text", text=f"✓ Here are your unread emails:\n\n{email_texts}")]
    elif name == "create_draft_reply":
        email_id = arguments["email_id"]
        reply_body = arguments["reply_body"]
        draft = await create_draft_reply(email_id, reply_body)
        return [types.TextContent(type="text", text=f"✓ Draft reply created:\n{draft}")]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="draft-email-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
