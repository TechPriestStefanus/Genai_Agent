from functions.get_file_content import get_file_content

lorem = get_file_content ("calculator", "lorem.txt")
if len(lorem) <= 11000:
    print("lorem.txt truncated: True")
print(get_file_content("calculator", "main.py"), 
    get_file_content("calculator", "pkg/calculator.py"), 
    get_file_content("calculator", "/bin/cat"), 
    get_file_content("calculator", "pkg/does_not_exist.py"))