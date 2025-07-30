Of course. Based on the approved design specification, I have decomposed the project into a series of discrete, actionable tasks.

Each task is designed to be self-contained enough to be handled by an individual AI agent, with clear goals, requirements, and context. The tasks are ordered logically to build the final `server.py` file step-by-step.

Here is the task decomposition:

---

### **Task 1: Project Scaffolding and Initial Setup**

* **Goal:** Create the basic file structure and configuration files for the project. This task establishes the foundation for all subsequent coding tasks.
* **Requirements:**
    * Use `pyproject.toml` and `uv.lock` for Python dependency management (instead of `requirements.txt`).
    * (Optional) Export a `requirements.txt` later if needed for deployment or documentation.
    * Create a file named `.env.example` to serve as a template for environment variables.
    * Create an empty Python file named `server.py` which will contain the core application logic.
    * Create a `README.md` file explaining the project setup and execution using `uv`.
    * Create a `USAGE.md` file explaining the custom tools and server features.

* **File Content:**
    * **`pyproject.toml` and `uv.lock`:**
        * Use these files to manage dependencies. Example dependencies:
            - fastmcp
            - httpx
            - pyyaml
            - pydantic
            - pydantic-settings
        * (No `requirements.txt` is needed, but it can be exported later if required.)

    * **`.env.example`:**
        ```
        # The base URL for your ActiveCampaign API account (e.g., https://your-account.api-us1.com)
        AC_API_URL=
        # Your ActiveCampaign API Token
        AC_API_TOKEN=
        ```
    * **`README.md` and `USAGE.md`:**
        * The content for these files should be the complete markdown text generated in our previous step.

---

### **Task 2: Implement Server Initialization and Authentication**

* **Goal:** Write the initial block of `server.py` to handle environment variable loading and the creation of an authenticated `httpx` client.
* **Requirements:**
    * In `server.py`, import the necessary libraries: `httpx`, `yaml`, `FastMCP`, and `pydantic-settings` (`BaseSettings`).
    * Define a `Config` class inheriting from `pydantic_settings.BaseSettings` to load `AC_API_URL` and `AC_API_TOKEN` from environment variables.
    * Instantiate the `Config` class to load environment variables.
    * Raise a `ValueError` if either of the required environment variables is not set (handled by Pydantic validation).
    * Instantiate an `httpx.AsyncClient` with the `base_url` and `headers` (`Api-Token`) configured correctly for the ActiveCampaign API.

* **Code Context:**
    ```python
    # server.py
    from pydantic_settings import BaseSettings
    import httpx
    import yaml
    from fastmcp import FastMCP

    class Config(BaseSettings):
        AC_API_URL: str
        AC_API_TOKEN: str

    config = Config()  # Loads from environment

    # 1. Get API_URL and API_TOKEN from config
    # 2. Create an authenticated httpx.AsyncClient instance
    client = httpx.AsyncClient(
        base_url=config.AC_API_URL,
        headers={"Api-Token": config.AC_API_TOKEN}
    )
    ```

---

### **Task 3: Implement OpenAPI to MCP Conversion with Route Exclusions**

* **Goal:** Generate the base `FastMCP` server from the `activev3.yml` specification, applying the custom route maps to exclude specific endpoints.
* **Requirements:**
    * Assume a file named `activev3.yml` exists in the same directory.
    * Import `RouteMap` and `MCPType` from `fastmcp.server.openapi`.
    * Define a list of `RouteMap` objects that specify which API routes to exclude, as per the design spec (`/contacts/{contactId}/*`, `/contacts` (POST), and `/accounts/bulk_delete/{ids}`).
    * Load and parse the YAML from `activev3.yml`.
    * [cite_start]Call `FastMCP.from_openapi`, providing the parsed spec, the authenticated `httpx` client from Task 2, and the custom `route_maps`. [cite: 799]

* **Code Context:**
    ```python
    # server.py (continuing from previous task)
    from fastmcp.server.openapi import RouteMap, MCPType

    # --- AGENT: Implement code below ---

    # 1. Define the list of RouteMap objects for exclusions.
    #    - Exclude granular contact data: pattern=r"^/api/3/contacts/.+/.+"
    #    - Exclude simple contact creation: pattern=r"^/api/3/contacts$", methods=["POST"]
    # 2. Open and load the 'data/activev3.yml' file.
    # 3. Call FastMCP.from_openapi and assign the result to a variable `mcp`.
    #    Pass the spec, the client, and the route_maps.
    ```

---

### **Task 4: Implement Custom Wrapper Tool `manage_contact_list_subscription`**

* **Goal:** Create and register the simplified tool for managing contact list subscriptions.
* **Requirements:**
    * Define an `async` function named `manage_contact_list_subscription` that accepts `contact_id: int`, `list_id: int`, and `subscribe: bool`.
    * The function's logic must convert the `subscribe` boolean into an integer `status` (`1` for `True`, `2` for `False`).
    * The function must then call the underlying auto-generated tool for subscribing/unsubscribing contacts. The agent should assume this tool is available on the `mcp` object created in the previous task. The original tool's name is `"Subscribe or Unsubscribe contact from list"`.
    * The function should return the result of the underlying tool call.
    * [cite_start]Register this function as a tool on the `mcp` object using the `@mcp.tool()` decorator. [cite: 996]

* **Code Context:**
    ```python
    # server.py (continuing from previous task)

    # The `mcp` object is assumed to be created from the OpenAPI spec.
    # The original tool is available as:
    # mcp.get_tool("Subscribe or Unsubscribe contact from list")

    # --- AGENT: Implement code below ---

    # 1. Define the async wrapper function `manage_contact_list_subscription`.
    # 2. Add logic to convert the boolean to a status integer.
    # 3. Call the original tool with the correct parameters: `contact`, `list`, and `status`.
    # 4. Register the function with `@mcp.tool(name="manage_contact_list_subscription")`.
    ```

---

### **Task 5: Implement Custom Wrapper Tool `smart_contact_search`**

* **Goal:** Create and register the simplified tool for searching for contacts.
* **Requirements:**
    * Define an `async` function named `smart_contact_search` that accepts optional string parameters: `email`, `name`, and `tag_id`.
    * The function's logic must construct a `params` dictionary to pass to the underlying `Get Contacts` tool.
        * If `email` is provided, add it to `params` with the key `"email"`.
        * If `name` is provided, add it to `params` with the key `"search"`.
        * If `tag_id` is provided, add it to `params` with the key `"tagid"`.
    * The function must call the underlying auto-generated tool named `"Get Contacts"`, passing the `params` dictionary.
    * The function should return the result of the tool call.
    * [cite_start]Register this function on the `mcp` object using the `@mcp.tool()` decorator. [cite: 996]

* **Code Context:**
    ```python
    # server.py (continuing from previous task)

    # The `mcp` object is assumed to be created.
    # The original tool is available as: mcp.get_tool("Get Contacts")

    # --- AGENT: Implement code below ---

    # 1. Define the async wrapper function `smart_contact_search`.
    # 2. Add logic to build the params dictionary based on provided arguments.
    # 3. Call the original "Get Contacts" tool with the constructed params.
    # 4. Register the function with `@mcp.tool(name="smart_contact_search")`.
    ```

---

### **Task 6: Finalize the Server Script**

* **Goal:** Assemble all previous components in `server.py` into a final, runnable script.
* **Requirements:**
    * Ensure all code from tasks 2-5 is present and correctly ordered.
    * [cite_start]Add the `if __name__ == "__main__":` block at the end of the script. [cite: 202]
    * [cite_start]Inside the block, call `mcp.run()` to start the server. [cite: 204]

* **Final Structure:**
    ```python
    # server.py
    # 1. Imports

    # 2. Config class and instantiation (pydantic-settings)

    # 3. Auth client setup

    # 4. Route map definitions

    # 5. OpenAPI spec loading and FastMCP.from_openapi call

    # 6. Definition and registration of manage_contact_list_subscription

    # 7. Definition and registration of smart_contact_search

    # 8. if __name__ == "__main__": block with mcp.run()
    ```