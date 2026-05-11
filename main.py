import os
import json
import argparse
from dotenv import load_dotenv
from google.genai import types
from google import genai





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
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(system_instruction="In one paragraph"))
                                              
    user_prompt = (args.user_prompt)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.usage_metadata is None:
        raise RuntimeError("API request failed")
    elif args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(response.text)
    else:
        print(response.text)

if __name__ == "__main__":
    main()
