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
- Set up the Claude desktop config to point to the MCP server

### Starting the server
- Open Claude Desktop, and the MCP server should start automatically

### Authenticating with Google
- When the first request is made to the MCP server requiring Gmail API access, you will be prompted to authenticate with Google. Once this is complete, you should be good to go! 🚀
