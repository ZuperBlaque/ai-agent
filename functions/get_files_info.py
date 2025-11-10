import os
from google.genai import types

# Define the function schema for get_files_info
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        },
        required =[]
    )
)

def get_files_info(working_directory, directory="."):
    """
    Return a single formatted string describing the contents of the target directory.
    Each line looks like:
    - NAME: file_size=SIZE bytes, is_dir=BOOL
    On error, returns a string starting with "Error:".
    """
    
    # Combine base directory with the relative path
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(abs_working, directory))

    # Ensure the target directory exists
    if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
        
    try:
        lines = []
        for name in os.listdir(abs_target):
            full = os.path.join(abs_target, name)
            is_dir = os.path.isdir(full)
            size = os.path.getsize(full)
            line = f'- {name}: file_size={size} bytes, is_dir={is_dir}'
            lines.append(line)
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"

