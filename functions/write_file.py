import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write or overwrite files in file path relative to working directory",
        parameters = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to be written into the file"

                    )
                }
            )
        )

def write_file(working_directory, file_path, content):
    
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        is_valid_path = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir

        if not is_valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return "Error: writing failed"
