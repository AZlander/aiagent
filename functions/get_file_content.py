import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # Get the absolute path of the directory
        # that the AI is allowed to access.
        working_dir_abs = os.path.abspath(working_directory)

        # Combine the allowed directory with the requested file.
        #
        # Example:
        # working_directory = "calculator"
        # file_path = "main.py"
        #
        # target_file becomes:
        # "/Users/azzzz/aiagent/calculator/main.py"
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Check whether the requested file is inside
        # the permitted working directory.
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        # If the file is outside our allowed directory,
        # don't allow the agent to access it.
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check whether the path actually points to a regular file.
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Open the file in read mode.
        with open(target_file, "r") as f:

            # Read at most 10,000 characters.
            content = f.read(MAX_CHARS)

            # Try to read ONE additional character.
            #
            # If we get a character, the file is larger than
            # our 10,000 character limit.
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        # Return the file's contents.
        return content

    # Catch unexpected errors and return them as strings.
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}