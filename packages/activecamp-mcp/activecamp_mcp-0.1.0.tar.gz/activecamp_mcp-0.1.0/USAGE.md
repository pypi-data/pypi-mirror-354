# Using the ActiveCampaign MCP Server

This document provides details on the available tools and resources, with a focus on the custom simplifications made to enhance interaction with Large Language Models (LLMs).

## Authentication

The server handles authentication automatically using the credentials provided in your `.env` file. You do not need to provide the API token when calling tools; it is injected into every API request by the server.

## Simplified Custom Tools

To provide a more intuitive and token-efficient experience for LLMs, several complex API endpoints have been wrapped in simpler custom tools.

### `smart_contact_search`

This tool simplifies searching for contacts by abstracting away the 20+ filter and sort parameters of the native API endpoint.

* **Purpose**: To find contacts using simple, common search criteria.
* **Parameters**:
    * `email` (str, optional): Search by a specific email address.
    * `name` (str, optional): Search for a contact by their full name.
    * `tag` (str, optional): Find contacts associated with a specific tag.
* **Example LLM Prompt**: `"Find the contact with the email 'jane.doe@example.com'"` or `"Search for contacts tagged as 'New Lead'"`

### `upsert_contact`

This single tool handles both creating a new contact and updating an existing one, making it more reliable than using separate tools. It is a more intuitive wrapper around the API's `contact/sync` endpoint.

* **Purpose**: To create a new contact or update an existing one based on their email address.
* **Parameters**:
    * `email` (str): The unique email address of the contact.
    * `firstName` (str, optional): The contact's first name.
    * `lastName` (str, optional): The contact's last name.
    * `phone` (str, optional): The contact's phone number.
* **Example LLM Prompt**: `"Create a contact for John Smith at 'john.smith@email.com'"` or `"Update the last name of the contact 'john.smith@email.com' to 'Smithers'"`

### `manage_contact_list_subscription`

This tool provides a clear, boolean-based method for managing a contact's subscription status to a list, avoiding the need for the LLM to know about the API's internal integer codes (`1` for active, `2` for unsubscribed).

* **Purpose**: To easily subscribe or unsubscribe a contact from a mailing list.
* **Parameters**:
    * `contact_id` (int): The ID of the contact.
    * `list_id` (int): The ID of the list.
    * `subscribe` (bool): Set to `True` to subscribe the contact, `False` to unsubscribe.
* **Example LLM Prompt**: `"Subscribe contact 12345 to list 10"` or `"Unsubscribe contact 12345 from list 10"`

## Directly Mapped Tools & Resources

Most other endpoints in the ActiveCampaign API are available as tools and resources, named directly after their `operationId` in the OpenAPI specification. You can interact with them as you would with any standard MCP tool.

**Examples:**
* `create_account`
* `delete_account`
* `get_campaigns`
* `add_tag_to_contact`
* `Notes`

## Excluded Endpoints

For simplicity and to reduce the complexity for the LLM, the following endpoints have been excluded from this MCP server:

* **Granular Contact Details**: All sub-endpoints for a contact (e.g., `/contacts/{id}/bounceLogs`, `/contacts/{id}/contactGoals`) have been removed. The primary `get_contact` tool provides this information in its response.
* **Bulk Delete**: The `/api/3/accounts/bulk_delete` endpoint has been excluded to prevent accidental mass-deletions by the LLM.