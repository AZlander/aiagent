import os
import argparse
import json

from dotenv import load_dotenv          #importing dotenv library
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()           #Load an .env file from dotenv library
    api_key = os.environ.get("OPENROUTER_API_KEY")          #Getting an OpenRouter key from .env document

    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY is not set")         #Prompting an output when agent didn't receive an api_key

    client = OpenAI(            #Creating an instance of OpenAI client class and assign it to the variable client
        base_url="https://openrouter.ai/api/v1",            #Overriding an API endpoint to OpenRouter server instead of OpenAI server. /api/v1 is the versioned API path OpenRouter exposes
        api_key=api_key         #Passes an authentication key
    )

    #
    parser = argparse.ArgumentParser(description="Chatbox")         #Create an argument parser object
    parser.add_argument("user_prompt", type=str, help="User prompt")            #Define one expected argument called user_prompt
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args()          #Reads the terminal input and stored it in parsed value


    # List of message objects, with the system prompt first and user's input second
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},

    ]

    # Let the agent have up to 20 turns.
    for _ in range(20):

        # Ask the LLM what to do next.
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        # Get the assistant's response.
        message = response.choices[0].message

        # IMPORTANT:
        # Add the assistant's response to the conversation history.
        messages.append(message)

        # If the LLM doesn't want to call a function,
        # then it has produced its final answer.
        if not message.tool_calls:
            if message.content:
                print(f"Final response:\n{message.content}")
                break
            else:
                print("Error: Model returned an empty response.")
                break

        # The LLM requested one or more functions.
        for tool_call in message.tool_calls:

            # Actually execute the function.
            result_message = call_function(
                tool_call,
                verbose=args.verbose
            )

            # Make sure the function returned something.
            if not result_message.get("content"):
                raise RuntimeError("Function call returned no content")

            # Add the tool's result to the conversation history.
            messages.append(result_message)

            # Show the result if verbose mode is enabled.
            if args.verbose:
                print(f"-> {result_message['content']}")

    else:
        # This runs if the loop reaches 20 iterations
        # without getting a final response.
        print("Maximum iterations reached without a final response.")


if __name__ == "__main__":
    main()