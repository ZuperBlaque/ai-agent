# python
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

# Load API key from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found in environment (.env).")

client = genai.Client(api_key=api_key)

# Register the available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

# Hardcoded system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    if len(sys.argv) <= 1:
        print("Error: no prompt provided.")
        sys.exit(1)

    # Combine all command-line arguments into a single prompt
    user_prompt = " ".join(sys.argv[1:])

    # Initialize conversation messages with user's initial prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    max_iterations = 20  # Stop after 20 steps to avoid infinite loops

    for _ in range(max_iterations):
        try:
            # Call the model with the full conversation so far
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"Error during generate_content: {e}")
            break

        saw_tool_call = False  # Track if any function call occurred this iteration

        for cand in getattr(response, "candidates", []):
            kept_text_parts = []  # Store normal text parts
            for part in cand.content.parts:
                # If part is a function call, execute it
                if getattr(part, "function_call", None):
                    saw_tool_call = True
                    fc = part.function_call
                    result_msg = call_function(fc, verbose=True)

                    # Append proper function_response back to messages
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part(function_response=result_msg.parts[0].function_response)]
                        )
                    )

                # If part is normal text, keep it for model context
                elif getattr(part, "text", None):
                    kept_text_parts.append(part)

            # Append text parts as a model message (optional for next iteration)
            if kept_text_parts:
                messages.append(types.Content(role="model", parts=kept_text_parts))

        # If no tool calls this turn and there’s text, print final output and stop
        if not saw_tool_call and getattr(response, "text", "").strip():
            print(response.text)
            # Optional: print token usage if exactly 3 CLI arguments
            if len(sys.argv) == 3:
                print(f"User prompt: {sys.argv[2]}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            break
        
    else:
        # If loop finishes without a final text response
        print("Max iterations reached without a final response.")

if __name__ == "__main__":
    main()