import os
from google.genai import types

# Define the function schema for get_files_info
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file located within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),

            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            )
        },
        required=["file_path", "content"]
    )
)

def write_file(working_directory, file_path, content):
    try:
         
        # Convert to absolute paths for safety
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(abs_working, file_path))

        # Check that file is within the permitted directory
        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):    
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
         # Ensure parent directory exists (create it if needed)
        parent_directory = os.path.dirname(abs_target)
        os.makedirs(parent_directory, exist_ok=True)

        # Ensure file path exists
        # Write the file (overwrites existing or creates new)
        with open(abs_target, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                    
    except Exception as e:
        return f"Error: {str(e)}"
