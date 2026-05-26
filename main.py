import os
import json
import argparse
from dotenv import load_dotenv
from google.genai import types
from google import genai
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python
from functions.write_file import schema_write_file
from prompts import system_prompt

available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python, schema_write_file])

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("api key not found!")
    


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()



    client = genai.Client(api_key=api_key)

    #updated response to messages
    #response = client.models.generate_content(model= "gemini-2.5-flash", contents= args+"In one paragraph.")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]   
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature = 0), )
                                              
    user_prompt = (args.user_prompt)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    called_functions = response.function_calls

    if response.usage_metadata is None:
        raise RuntimeError("API request failed")
    elif args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        if called_functions:
            for f_object in called_functions:
                print(f"Calling function: {f_object.name}({f_object.args})")
        else:    
            print(response.text)
    else:
        if called_functions:
            for f_object in called_functions:
                print(f"Calling function: {f_object.name}({f_object.args})")
        else:
            print(response.text)

    

if __name__ == "__main__":
    main()

#uv run main.py ""
