import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir=os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        contents = ""

        for n in os.listdir(target_dir):
            name=n
            n_path = os.path.join(target_dir, n)
            file_size=os.path.getsize(n_path)
            is_dir=os.path.isdir(n_path)
            contents += f"\n- {name}: file_size={file_size} bytes, is_dir={is_dir}"
        
        return contents
    except:
        return "Error: cant access file"
