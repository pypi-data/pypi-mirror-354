import llm
import requests
import json

# --- Configuration ---
BASE_URL = "http://localhost:8080"

# --- Main Helper for API Calls ---

def _handle_api_call(method: str, endpoint: str, **kwargs) -> str:
    """A robust helper to make API calls and return a JSON string result."""
    try:
        response = requests.request(method, f"{BASE_URL}{endpoint}", **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return json.dumps({"status": "success", "message": "Operation successful."})
        result = response.json()
        return json.dumps(result, indent=2)
    except requests.exceptions.HTTPError as e:
        error_message = f"API Error: {e.response.status_code} {e.response.reason}"
        try:
            server_error = e.response.json()
            error_message += f"\nServer Detail: {json.dumps(server_error)}"
        except json.JSONDecodeError:
            error_message += f"\nServer Response (not JSON): {e.response.text}"
        return json.dumps({"error": error_message})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Request failed: Could not connect to the server at {BASE_URL}. Please ensure it is running. Details: {e}"})
    except Exception as e:
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
def register_tools(register): 
    """This function is called by LLM to register our tools."""
    # We call the 'register' function for each tool we want to add.
    register(read_graph)
    register(create_entities)
    register(create_relations)
    register(add_observations)
    register(search_nodes)
    register(open_nodes)
    register(delete_entities)
    register(delete_observations)
    register(delete_relations)
