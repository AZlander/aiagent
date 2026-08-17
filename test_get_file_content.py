from functions.get_file_content import get_file_content


# Large file
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")


# Normal file
print("\n--- main.py ---")
print(get_file_content("calculator", "main.py"))


# File inside pkg
print("\n--- calculator.py ---")
print(get_file_content("calculator", "pkg/calculator.py"))


# Outside permitted directory
print("\n--- /bin/cat ---")
print(get_file_content("calculator", "/bin/cat"))


# File that doesn't exist
print("\n--- does_not_exist.py ---")
print(get_file_content("calculator", "pkg/does_not_exist.py"))