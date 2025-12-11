# draft-email-mcp

An MCP server for creating draft replies to unread emails via Gmail API

## Overview

This MCP server was designed to be run locally with Claude Desktop. It extends the LLM's capabilities by providing the following additional abilities:
- Retrieving the latest `n` unread emails from the authenticated Gmail inbox
- Creating draft replies for an email in Gmail given the relevant `email_id`

## Setup

###  Prerequisites

- Credentials for a Google Cloud project with Gmail API access
- Claude Desktop installed locally

### Environment Variables
- Clone the `.env.example` into a fresh `.env` file
- Download the `credentials.json` file for your Google Cloud project and place it in a convenient location
- Set the `GOOGLE_CREDENTIALS_PATH` in the `.env` to point to your `credentials.json` file
- Set the `GOOGLE_TOKEN_PATH` to desired location for the `token.json`. This needs to be a writable directory, as the token file will be created when the server authenticates with Google Auth.

### Setting up `claude_desktop_config.json`
- Locate the `claude_desktop_config.json`:
  - **Mac:** `/Users/{user}/Library/Application Support/Claude/claude_desktop_config.json`
  - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- Extend your existing `claude_desktop_config.json` with the following configuration:
  ```json
  {
    "mcpServers": {
      "email": {
        "command": "{path-to-your-draft-email-mcp-directory}/env/bin/python",
        "args": ["{path-to-your-draft-email-mcp-directory}/draft_email_server.py"],
        "env": {}
      }
    }
  }
  ```

### Starting the server
- Open Claude Desktop, and the MCP server should start automatically

### Authenticating with Google
- When the first request is made to the MCP server requiring Gmail API access, you will be prompted to authenticate with Google. Once this is complete, you should be good to go! 🚀

## Available tools
This MCP server provides the following tools:

### `get_unread_emails`
This accepts a `limit` argument that defaults to `5` to ensure the tool is resilient to use on inboxes with a large number of unread emails. It retrieves the `id`, `sender`, `subject`, `thread_id`, `timestamp` and `snippet` of each email from the Gmail inbox and returns the result in JSON format. Though it might be better to retrieve the body of the email in some cases, the `1MB` size limit imposed by Claude Desktop means that many marketing emails containing numerous images are too large, resulting in an error.

### `create_draft_reply`

This accepts the `email_id` of the original email and the `reply_body` as strings and creates this draft in the relevant thread in Gmail. It returns the `draft_id` and `draft_message` of the created draft in JSON format.

## Demo

### Example prompts

- `Summarise my last unread email`
- `Create draft replies for my latest 3 unread emails`

### Screenshots

#### Before
<img width="1147" height="221" alt="Screenshot 2025-12-11 at 22 23 32" src="https://github.com/user-attachments/assets/89bd80d6-01ef-4704-868a-18705e380100" />

#### During
<img width="996" height="795" alt="Screenshot 2025-12-11 at 22 26 56" src="https://github.com/user-attachments/assets/dc1ab20b-cca2-4a40-9839-a3b286ce140b" />
<img width="750" alt="Screenshot 2025-12-11 at 22 28 56" src="https://github.com/user-attachments/assets/fed204f9-f691-49fb-aa86-5c277d303edb" />


#### After
<img width="1162" height="227" alt="Screenshot 2025-12-11 at 22 30 13" src="https://github.com/user-attachments/assets/fca14dde-2f04-4d3d-9225-b0f9a2654ed5" />
<img width="1404" height="696" alt="Screenshot 2025-12-11 at 22 30 42" src="https://github.com/user-attachments/assets/2128425e-9dab-4aa6-9d03-02cf4c51badf" />


