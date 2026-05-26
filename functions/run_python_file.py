
import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
        name="run_python_file",
        description="executes a python file in a specified directory relative to the working directory, with or without additional arguments",
        parameters = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to the python file to be executed, relative to the working directory (default is the working directory itself)",
                    ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="additional arguments in the form of a list of strings of numbers (this is an optional property)",
                    items=types.Schema(type=types.Type.STRING)
                    )
                }
            )
        )

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
        abs_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_path, file_path))

        is_valid_path = os.path.commonpath([target_file_path, abs_path]) == abs_path

        if not is_valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)

        new_stuff = subprocess.run(command, cwd=abs_path, capture_output = True , text = True, timeout = 30)

        output_string = ""

        if new_stuff.returncode != 0:
            output_string += f"Process exited with code {new_stuff.returncode}"

        if (new_stuff.stdout == "") and (new_stuff.stderr == ""):
            output_string += "No output produced"
        elif new_stuff.stderr != "":
            output_string += f"STDERR: {new_stuff.stderr}"
        elif new_stuff.stdout != "":
            output_string += f"STDOUT: {new_stuff.stdout}"
        return output_string
    
    except Exception as e:
        return f"Error: executeing Python File: {e}"
            
        
        
