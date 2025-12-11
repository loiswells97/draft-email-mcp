# draft-email-mcp

An MCP server for retrieving unread emails and creating draft replies via Gmail API

## Overview

This MCP server was designed to be run locally with Claude Desktop. It extends the LLM's capabilities by providing the following additional abilities:
- Retrieving the latest `n` unread emails from the authenticated Gmail inbox
- Creating draft replies for an email in Gmail given the relevant `email_id`
- Retrieving a local email style guide file

## Setup

###  Prerequisites

- Credentials for a Google Cloud project with Gmail API access
- Claude Desktop installed locally

### Environment Variables
- Clone the `.env.example` into a fresh `.env` file
- Download the `credentials.json` file for your Google Cloud project and place it in a convenient location
- Set the `GOOGLE_CREDENTIALS_PATH` in the `.env` to point to your `credentials.json` file
- Set the `GOOGLE_TOKEN_PATH` to desired location for the `token.json`. This needs to be a writable directory, as the token file will be created when the server authenticates with Google Auth.
- If providing a local email style guide, set the `EMAIL_STYLE_GUIDE_PATH` variable to the location of the style guide. See [`example_email_style_guide.md`](https://github.com/loiswells97/draft-email-mcp/blob/main/example_email_style_guide.md) for an example style guide.

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

### get_style_guide

This retrieves the content of the style guide at `EMAIL_STYLE_GUIDE_PATH` to enable Claude to write better emails.

## Demo

This demo was run using [`example_email_style_guide.md`](https://github.com/loiswells97/draft-email-mcp/blob/main/example_email_style_guide.md) as the style guide.

### Example prompts

- `Summarise my last unread email`
- `Create draft replies for my latest 3 unread emails`
- `Get my email style guide`

### Screenshots

#### Before
<img width="1156" height="231" alt="Screenshot 2025-12-11 at 23 15 22" src="https://github.com/user-attachments/assets/d9c3cd14-e515-4127-81e8-f993f59ebbf2" />


#### During
<img width="524" height="376" alt="Screenshot 2025-12-11 at 23 20 00" src="https://github.com/user-attachments/assets/942ef1a2-6175-465e-9945-e1f3b5b093a3" />
<img width="523" height="681" alt="Screenshot 2025-12-11 at 23 19 02" src="https://github.com/user-attachments/assets/c6fdf9b8-3ab7-4062-a083-9f99cafdf721" />


#### After
<img width="1414" height="379" alt="Screenshot 2025-12-11 at 23 18 15" src="https://github.com/user-attachments/assets/e4187034-11a5-4fd3-9e94-94f2cb8c1459" />
<img width="1161" height="673" alt="Screenshot 2025-12-11 at 23 18 49" src="https://github.com/user-attachments/assets/5a39281c-7d98-4f83-81eb-d8da174ac089" />


