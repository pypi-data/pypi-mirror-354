import llm
import requests
import json

# --- Configuration ---
BASE_URL = "http://localhost:8080"

# --- Main Helper for API Calls ---

def _handle_api_call(method: str, endpoint: str, **kwargs) -> str:
    """A robust helper to make API calls and return a JSON string result."""
    try:
        # The 'json' kwarg automatically sets the Content-Type header to application/json
        response = requests.request(method, f"{BASE_URL}{endpoint}", **kwargs)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Handle cases with no content in the response body
        if response.status_code == 204:
            return json.dumps({"status": "success", "message": "Operation successful."})
            
        result = response.json()
        return json.dumps(result, indent=2)

    except requests.exceptions.HTTPError as e:
        # Try to provide a more informative error message from the server's response
        error_message = f"API Error: {e.response.status_code} {e.response.reason}"
        try:
            server_error = e.response.json()
            error_message += f"\nServer Detail: {json.dumps(server_error)}"
        except json.JSONDecodeError:
            error_message += f"\nServer Response (not JSON): {e.response.text}"
        return json.dumps({"error": error_message})
        
    except requests.exceptions.RequestException as e:
        # Handle network-level errors (e.g., connection refused)
        return json.dumps({"error": f"Request failed: Could not connect to the server at {BASE_URL}. Please ensure it is running. Details: {e}"})
        
    except Exception as e:
        # Handle other unexpected errors
        return json.dumps({"error": f"An unexpected error occurred: {e}"})


# --- Tool Function Implementations ---

def read_graph() -> str:
    """Retrieves the entire knowledge graph, including all entities and their relations."""
    return _handle_api_call("get", "/read_graph")

def create_entities(entities_json: str) -> str:
    """
    Creates new entities. Input must be a JSON string of a list of entity objects.
    Example: '[{"name": "Entity1", "entityType": "TypeA", "observations": ["obs1"]}]'
    """
    try:
        entities_data = json.loads(entities_json)
        if not isinstance(entities_data, list):
            raise TypeError("Input must be a list of entity objects.")
        return _handle_api_call("post", "/create_entities", json={"entities": entities_data})
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid input format for create_entities: {e}"})

def create_relations(relations_json: str) -> str:
    """
    Creates new relations between entities. Input must be a JSON string of a list of relation objects.
    Example: '[{"from": "Entity1", "to": "Entity2", "relationType": "connects_to"}]'
    """
    try:
        relations_data = json.loads(relations_json)
        if not isinstance(relations_data, list):
            raise TypeError("Input must be a list of relation objects.")
        return _handle_api_call("post", "/create_relations", json={"relations": relations_data})
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid input format for create_relations: {e}"})

def add_observations(observation_json: str) -> str:
    """
    Adds observations to an entity. Input must be a JSON string of an object with "entity_name" and "contents" keys.
    Example: '{"entity_name": "Entity1", "contents": ["new observation", "another one"]}'
    """
    try:
        obs_data = json.loads(observation_json)
        payload = {"observations": [{"entityName": obs_data["entity_name"], "contents": obs_data["contents"]}]}
        return _handle_api_call("post", "/add_observations", json=payload)
    except (json.JSONDecodeError, KeyError) as e:
        return json.dumps({"error": f"Invalid input format for add_observations: {e}"})

def search_nodes(query: str) -> str:
    """
    Searches for nodes (entities) by a query string. The search matches names, types, and observations.
    """
    return _handle_api_call("post", "/search_nodes", json={"query": query})

def open_nodes(names_json: str) -> str:
    """
    Retrieves specific nodes by their names. Input must be a JSON string of a list of entity names.
    Example: '["Entity1", "Entity2"]'
    """
    try:
        names = json.loads(names_json)
        if not isinstance(names, list):
            raise TypeError("Input must be a list of names.")
        return _handle_api_call("post", "/open_nodes", json={"names": names})
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid input format for open_nodes: {e}"})

def delete_entities(names_json: str) -> str:
    """
    Deletes entities from the graph. Input must be a JSON string of a list of entity names.
    Example: '["EntityToDelete1", "EntityToDelete2"]'
    """
    try:
        names = json.loads(names_json)
        if not isinstance(names, list):
            raise TypeError("Input must be a list of names.")
        return _handle_api_call("post", "/delete_entities", json={"entityNames": names})
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid input format for delete_entities: {e}"})

def delete_observations(deletions_json: str) -> str:
    """
    Deletes specific observations from an entity. Input is a JSON string with 'entity_name' and 'observations' list.
    Example: '{"entity_name": "Entity1", "observations": ["obs_to_delete"]}'
    """
    try:
        data = json.loads(deletions_json)
        payload = {"deletions": [{"entityName": data["entity_name"], "observations": data["observations"]}]}
        return _handle_api_call("post", "/delete_observations", json=payload)
    except (json.JSONDecodeError, KeyError) as e:
        return json.dumps({"error": f"Invalid input format for delete_observations: {e}"})

def delete_relations(relations_json: str) -> str:
    """
    Deletes relations from the graph. Input must be a JSON string of a list of relation objects to delete.
    Example: '[{"from": "Entity1", "to": "Entity2", "relationType": "connects_to"}]'
    """
    try:
        relations_data = json.loads(relations_json)
        if not isinstance(relations_data, list):
            raise TypeError("Input must be a list of relation objects.")
        return _handle_api_call("post", "/delete_relations", json={"relations": relations_data})
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid input format for delete_relations: {e}"})


# --- LLM Plugin Hook ---

@llm.hookimpl
def register_tools(tools):
    """This function is called by LLM when the plugin is loaded."""
    tool_definitions = [
        llm.Tool("read_graph", read_graph, "Retrieves the entire knowledge graph, including all entities and their relations."),
        llm.Tool("create_entities", create_entities, "Creates new entities. Input must be a JSON string of a list of entity objects."),
        llm.Tool("create_relations", create_relations, "Creates new relations between entities. Input must be a JSON string of a list of relation objects."),
        llm.Tool("add_observations", add_observations, "Adds observations to an entity. Input must be a JSON string of an object with 'entity_name' and 'contents' keys."),
        llm.Tool("search_nodes", search_nodes, "Searches for nodes (entities) by a query string."),
        llm.Tool("open_nodes", open_nodes, "Retrieves specific nodes by their names. Input must be a JSON string of a list of entity names."),
        llm.Tool("delete_entities", delete_entities, "Deletes entities from the graph. Input must be a JSON string of a list of entity names."),
        llm.Tool("delete_observations", delete_observations, "Deletes specific observations from an entity. Input is a JSON string with 'entity_name' and 'observations' list."),
        llm.Tool("delete_relations", delete_relations, "Deletes relations from the graph. Input must be a JSON string of a list of relation objects to delete."),
    ]
    tools.extend(tool_definitions):
