import os
from config import MAX_FILE_LENGTH

def get_file_content(working_directory, file_path):
    """
    Return the content of the target file as a string.
    On error, returns a string starting with "Error:".
    """
    try:
        # Combine base directory with the relative path
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(abs_working, file_path))

        # Ensure the target directory exists
        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):    
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure the target is a file
        if not os.path.isfile(abs_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read and return the file content
        with open(abs_target, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > MAX_FILE_LENGTH:
            content = (
                content[:MAX_FILE_LENGTH] + 
                f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]'
            )
        
        return content
    
    except Exception as e:
        # Catch all exceptions and return as error message
        return f"Error: {str(e)}"