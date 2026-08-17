import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        # Combine the allowed directory with the requested file path
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Checked whether the requested file is inside the permitted working directory
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        # Not allowing AI to execute files outside its permitted directory.
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Checking whether the file exists and is actually a file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Making sure the AI only executing Python files
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command that will be executed.
        command = ["Python", target_file]

        # If the caller provide additional argument, add them to the command.
        if args:
            command.extend(args)

        # Run the Python program
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Start building an output
        output = ""

        # A return code other than 0 means the program failed.
        if result.returncode != 0:
            output += f"Process existed with code {result.returncode}\n"

        # Add stdout if the program printed anything
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"

        # Add stderr if the program printed anything there.
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"

        # if neither stdout nor stderr contain anything, tell the caller that the program produced no output
        if not result.stdout and not result.stderr:
            output += "No output produced"

        return output

    # Catch any error and turn them into an error string.
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}