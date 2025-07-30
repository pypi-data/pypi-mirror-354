import inspect
import json


def generate_json_spec(func):
    # Get function name and docstring
    func_name = func.__name__
    func_doc = inspect.getdoc(func) or "No description provided"

    # Get function signature
    sig = inspect.signature(func)
    parameters = sig.parameters
    required_params = [name for name, param in parameters.items() if param.default == param.empty]
    optional_params = [name for name, param in parameters.items() if param.default != param.empty]

    # Define JSON schema
    json_spec = {
        "name": func_name,
        "description": func_doc,
        "parameters": {
            "type": "object",
            "required": required_params,
            "properties": {}
        }
    }
    
    # Add parameters to JSON schema
    for name, param in parameters.items():
        param_spec = {
            "type": "string",
            "description": "",
        }
        if param.annotation != param.empty:
            param_spec["type"] = param.annotation.__name__
        if param.default != param.empty:
            param_spec["default"] = param.default
            param_spec["description"] += f", default is {param.default}"

        json_spec["parameters"]["properties"][name] = param_spec

    return json.dumps(json_spec, indent=4)


