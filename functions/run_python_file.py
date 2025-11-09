import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
         
        # Convert to absolute paths for safety
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(abs_working, file_path))

        # Check that file is within the permitted directory
        if not abs_target.startswith(abs_working + os.sep):    
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Ensure parent directory exists, if not, return an error.
        if not os.path.exists(abs_target):
            return f'Error: File "{file_path}" not found.'
        
        # Ensure file is a Python file        
        if not abs_target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Construct the command to run:
        # "python <script> <extra args>"
        command = [os.sys.executable, abs_target] + list(args)

        # Execute script
        completed = subprocess.run(
            command,
            cwd=abs_working,       # Run inside the working directory
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,             # Decode output as strings instead of bytes
            timeout=30             # Prevent infinite loops
        )

        # Format output
        output_parts = []

        if completed.stdout.strip():
            output_parts.append(f"STDOUT:\n{completed.stdout.strip()}")

        if completed.stderr.strip():
            output_parts.append(f"STDERR:\n{completed.stderr.strip()}")

        # Always check return code
        if completed.returncode != 0:
            output_parts.append(f"Process exited with code {completed.returncode}")

        # If absolutely nothing to report
        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
        