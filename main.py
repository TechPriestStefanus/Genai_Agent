import os
import json
import argparse
import sys
import time
from dotenv import load_dotenv
from google.genai import types
from google import genai
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python
from functions.write_file import schema_write_file
from functions.call_function import call_function
from prompts import system_prompt

available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python, schema_write_file])

# CONFIG
loop_range = 10

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

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]   

    for _ in range(loop_range):
        #updated response to messages
        #response = client.models.generate_content(model= "gemini-2.5-flash", contents= args+"In one paragraph.")
        
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature = 0), )
                                                
        user_prompt = (args.user_prompt)
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        called_functions = response.function_calls #list of types.FunctionCall objects
        results_list = []
        
        if response.candidates:  
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)


        def function_loop():
            for f_object in called_functions:
                    function_call_result = call_function(f_object, args.verbose) #takes functioncallobject and verbose bool 
                    if not isinstance(function_call_result.parts, list) or not function_call_result.parts:
                        raise Exception("Problem with function result return object")
                    
                    elif not function_call_result.parts[0].function_response:
                        raise Exception("Function Response Error 1")
                    
                    elif not function_call_result.parts[0].function_response.response:
                        raise Exception("Function Response Error 2")
                    
                    else:
                        
                        results_list.append(function_call_result.parts[0])
                        if args.verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")

        if response.usage_metadata is None:
            raise RuntimeError("API request failed")
        elif args.verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            if called_functions:
                function_loop()
                if results_list:
                    messages.append(types.Content(role="user", parts=results_list))
                
                    


            else:   
                print(response.text)
        else:
            if called_functions:
                function_loop()
                if results_list:
                    messages.append(types.Content(role="user", parts=results_list))
                
            else:
                print(response.text)
        
        
        if not called_functions:
            break
        if _ == (loop_range-1):
            sys.exit(_ExitCode = 1)

        time.sleep(30)

        

if __name__ == "__main__":
    main()

#uv run main.py ""
