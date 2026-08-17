import json
from collections.abc import Callable

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

# Tell the LLM which functions are available
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


# Map the function name from the LLM to the actual Python function
function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    # Get the name of the function the LLM wants to call
    function_name = tool_call.function.name

    # Convert the JSON arguments from a string into a Python dictionary
    function_args = json.loads(tool_call.function.arguments or "{}")

    # Print information about the function call
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check whether the requested function actually exists
    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    # Give every function the working directory automatically
    function_args["working_directory"] = "./calculator"

    # Get the actual Python function
    function = function_map[function_name]

    # Actually run the function
    result = function(**function_args)

    # Return the result as a tool message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }