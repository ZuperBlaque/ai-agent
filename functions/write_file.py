import os

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
