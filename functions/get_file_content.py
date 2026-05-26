import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Lists the files content in a specified directory relative to the working directory",
        parameters = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to get content from, relative to the working directory (default is the working directory itself)",
                    )
                }
            )
        )

def get_file_content(working_directory, file_path):

    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_working_directory, file_path))

        is_valid_path = os.path.commonpath([abs_working_directory, target_directory]) == abs_working_directory

        if not is_valid_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        #return file contents as string
        file = open(target_directory, "r")
        contents = file.read(10000)
        if file.read(1):
            contents += f'[...File "{target_directory}" truncated at 10000 characters]'
        file.close()
        return contents
    
    except:
        Exception("Error: Failed to get content from file")