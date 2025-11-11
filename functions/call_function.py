import os
from google.genai import types
import importlib
import sys
  # Import the function implementations
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

functions_lib = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

def call_function(function_call_part, verbose=False):
    """
    Calls a function based on the provided function call part.

    Args:
        function_call_part (dict): A dictionary containing the function name and arguments.
        verbose (bool): If True, prints additional information during execution.

    Returns:
        The result of the function call.
    """
    function_name = function_call_part.name
    arguments = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({arguments})")
    else:
        print(f" - Calling function: {function_name}")

    # Retrieve the function to call
    func = functions_lib.get(function_name)
    
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Inject working directory argument
    arguments["working_directory"] = os.path.abspath("./calculator")

    # Call the function with the provided arguments
    function_result = func(**arguments)

    if verbose:
        print(f"Result: {function_result}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )