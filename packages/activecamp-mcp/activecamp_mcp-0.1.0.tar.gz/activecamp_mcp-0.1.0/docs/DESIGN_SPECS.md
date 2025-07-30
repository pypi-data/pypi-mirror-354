## **Design Spec: ActiveCampaign v3 MCP Server (Revised for uv)**

This document outlines the design for a Python-based MCP server for the ActiveCampaign v3 API, built using the FastMCP framework and managed with `uv`.

### 1. High-Level Approach

[cite_start]The server will be generated using FastMCP's `FastMCP.from_openapi` class method[cite: 777]. [cite_start]This will automatically convert the ActiveCampaign REST API endpoints into MCP `Tools`, `Resources`, and `Resource Templates` based on their HTTP methods and path structures[cite: 782, 791].

We will then apply customizations to achieve the desired "compression" and removal of certain functions. This will be done using a combination of:
* [cite_start]**Custom Route Maps**: To selectively exclude or change the MCP component type for specific API routes[cite: 799, 805].
* **Custom Wrapper Tools**: For endpoints that are overly complex, we will create simpler, more LLM-friendly Python functions that call the underlying auto-generated tools.
* [cite_start]**Component Naming**: We will use the `mcp_names` parameter to give verbose or non-intuitive endpoints friendlier names for the LLM[cite: 818].

### 2. Core Components & Setup

The project will be scaffolded with the following core files:

* `server.py`: The main file containing the FastMCP server definition, OpenAPI loading, and all custom logic.
* `requirements.txt`: A file listing all necessary Python dependencies (`fastmcp`, `httpx`, `python-dotenv`).
* `.env`: A file to securely store the ActiveCampaign API token and URL.
* `README.md`: A file with setup and execution instructions using the `uv` package manager.

### 3. Authentication

The ActiveCampaign API uses a token in the `Api-Token` header for authentication. [cite_start]This will be handled by configuring the `httpx.AsyncClient` that FastMCP uses to make API calls[cite: 830]. The API token and account-specific URL will be loaded securely from an environment variable (`AC_API_TOKEN`, `AC_API_URL`) rather than being hard-coded.

**Example `server.py` snippet:**
```python
import os
import httpx
from fastmcp import FastMCP

# Load token from environment variables
api_url = os.getenv("AC_API_URL")
api_token = os.getenv("AC_API_TOKEN")

if not all([api_url, api_token]):
    raise ValueError("AC_API_URL and AC_API_TOKEN environment variables must be set.")

# Create an authenticated HTTP client
api_client = httpx.AsyncClient(
    base_url=api_url,
    headers={"Api-Token": api_token}
)

# ... further server generation logic
```

### 4. Endpoint Mapping Strategy

This is the core of the customization, addressing your request to compress and prune the API surface.

#### 4.1. Direct Mapping

[cite_start]The majority of the standard CRUD (Create, Read, Update, Delete) operations will be mapped directly to MCP tools and resources using FastMCP's default rules[cite: 782].

* [cite_start]`POST`, `PUT`, `DELETE` routes will become **Tools**[cite: 790].
* [cite_start]`GET` routes with path parameters (e.g., `GET /api/3/accounts/{id}`) will become **Resource Templates**[cite: 786, 787].
* [cite_start]`GET` routes without path parameters (e.g., `GET /api/3/accounts`) will become **Resources**[cite: 788].

**Examples of Directly Mapped Tools:**
* `create_account`
* `delete_account`
* `update_account`
* `add_tag_to_contact`
* `remove_tag_from_contact`

#### 4.2. Exclusions

To simplify the server, we will explicitly exclude redundant or overly specific endpoints. [cite_start]This will be done using a `RouteMap` with `MCPType.EXCLUDE`[cite: 805].

**Proposed Exclusions:**

* **Specific Contact Data Endpoints**: The main `GET /api/3/contacts/{contactId}` endpoint returns a comprehensive `contact` object with a `links` section. We will rely on this primary endpoint and exclude the separate, granular endpoints for a contact's goals, bounce logs, etc.
    * **Rule**: Exclude `^/api/3/contacts/{contactId}/.+`
* **Bulk Delete**: Bulk delete operations are potentially dangerous for an LLM to invoke without very careful supervision. We will exclude `/api/3/accounts/bulk_delete/{ids}`.

#### 4.3. Custom Tools & Simplifications (Compression)

This is where we add the most value by creating a more intuitive interface for the LLM.

1.  **Unified Contact Creation/Update**:
    * **Problem**: The API has `POST /api/3/contacts` (Create) and `POST /api/3/contact/sync` (Create or Update). The `sync` endpoint is more versatile.
    * **Solution**:
        * [cite_start]Exclude the simple `POST /api/3/contacts` endpoint using a `RouteMap`[cite: 805].
        * [cite_start]Rename the `POST /api/3/contact/sync` tool from its default `create_or_update_contact` to a more intuitive `upsert_contact` using the `mcp_names` dictionary[cite: 818].

2.  **Simplified Contact Search**:
    * **Problem**: The `GET /api/3/contacts` endpoint has over 20 different query parameters for filtering and sorting, which is overwhelming and inefficient for an LLM.
    * **Solution**: We will define a custom Python tool called `smart_contact_search`. This tool will:
        * [cite_start]Be created by decorating a standard Python function with `@mcp.tool`[cite: 996].
        * Expose only the most essential search parameters: `email`, `name`, `tag`, and `list_name`.
        * Internally, it will call the more complex, auto-generated `get_contacts` tool, mapping the simple inputs to the correct API parameters.

3.  **Simplified List Subscription Management**:
    * **Problem**: The `POST /api/3/contactLists` endpoint uses a `status` field (`1` for subscribe, `2` for unsubscribe) which is not intuitive for an LLM.
    * **Solution**: We will create a custom wrapper tool named `manage_contact_list_subscription`.
        * It will accept a `contact_id`, a `list_id`, and a boolean `subscribe` parameter.
        * The tool's logic will translate the `subscribe` boolean into the required `status` integer (`1` or `2`) before calling the underlying auto-generated tool.

### 5. Project Scaffolding Plan

Once this design is approved, I will generate the following files:

* **`server.py`**:
    * Will contain the logic for loading the OpenAPI spec.
    * Will define the authenticated `httpx.AsyncClient`.
    * [cite_start]Will include the custom `RouteMap` definitions for exclusions[cite: 799].
    * Will define the custom wrapper tools (`smart_contact_search`, `manage_contact_list_subscription`).
    * [cite_start]Will instantiate the final MCP server using `FastMCP.from_openapi`, passing in all the custom configurations[cite: 777].
    * [cite_start]Will include the `if __name__ == "__main__":` block to run the server[cite: 202, 292].

* **`requirements.txt`**:
    ```
    fastmcp
    httpx
    python-dotenv
    ```

* **`.env.example`**:
    ```
    # The base URL for your ActiveCampaign API account (e.g., https://your-account.api-us1.com)
    AC_API_URL=
    # Your ActiveCampaign API Token
    AC_API_TOKEN=
    ```

* **`README.md`**: Will contain setup instructions tailored for `uv`.
    * Instructions on how to create the `.env` file from the example.
    * How to create and activate a virtual environment: `uv venv` and `source .venv/bin/activate`.
    * How to install dependencies: `uv pip install -r requirements.txt`.
    * How to run the server: `python server.py`.

