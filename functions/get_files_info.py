import os

# working_directory = the directory the AI is allowed to access
# directory = the specific directory the AI wants to inspect
# "." means the current working directory by default
# -> means the function should return a string
def get_files_info(working_directory: str, directory: str = ".") -> str:

    # Start a try block to ensure any unexpected error from os.path function happens is handled.
    try:
        # Convert a working directory into an absolute path.
        # example: "calculator" becomes "/Users/azzzz/aiagent/calculator"
        working_dir_abs = os.path.abspath(working_directory)

        # Combine a working directory with the directory that user or AI requested
        # For example:
        # working_dir_abs = "/Users/azzzz/aiagent/calculator"
        # directory = "pkg"
        #
        # Result:
        # "/Users/azzzz/aiagent/calculator/pkg"
        #
        # normpath() cleans up things like ".." and ".".
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Find the common path shared by the allowed working directory and the requested target directory.
        #
        # If the target is INSIDE the working directory, the common
        # path should be exactly the working directory.
        #
        # Example:
        # working directory:
        # /Users/azzzz/aiagent/calculator
        #
        # target:
        # /Users/azzzz/aiagent/calculator/pkg
        #
        # common path:
        # /Users/azzzz/aiagent/calculator
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir])
            == working_dir_abs
        )

        # if the target directory is outside the allowed working directory, reject the request.
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'

        # Check whether the requested path actually exists and is a directory.
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory.'

        # Get the names of everything inside the target directory.
        items = os.listdir(target_dir)

        # Storage to store each formatted file or directory description here.
        result = []

        # Go through every items in the directory
        for item in items:
            item_path = os.path.join(target_dir, item) # Build a complete path to this item.
            file_size = os.path.getsize(item_path) # Get the item's size in bytes
            is_dir = os.path.isdir(item_path) # Check whether the item is a directory or not

            # Create the required output format.
            result.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(result) # Turn a list of strings into one string with each item on its own line.

    # Catch any unexpected errors raised by the code above
    except Exception as e:
        return f"Error: {e}" # Convert the error into a string


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}