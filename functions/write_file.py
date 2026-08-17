import os

def write_file(working_directory: str, file_path: str, content: str)-> str:
    try:
        working_dir_abs = os.path.abspath(working_directory) # Get the absolute part of directory that AI is allowed to work on.

        # Combine the allowed directory with the requested file path
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Checked whether the requested file is inside the permitted working directory
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        # Not allowing the AI agent to escape the working directory
        if not valid_target_file:
            return (
                f'Error: Cannot write to "{file_path}"' "as it is outside the permitted working directory"
            )

        # After the requested path is in directory, the directory cannot be overwriting as normal file
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{target_file}" as it is a directory'

        # Get the directory containing the file
        parent_dir = os.path.dirname(target_file)

        # Create any missing parent directories.
        os.makedirs(parent_dir, exist_ok=True)

        # Open the file in write mode
        # "w" means to create a file if it doesn't exist; overwrite it if it already exist
        with open(target_file, "w") as f:
            f.write(content)

        # Tell the caller that the operation succeeded
        return (
            f'Successfully wrote to "{file_path}"'
            f"({len(content)} characters written)"
        )

    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites a file with the provided content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}