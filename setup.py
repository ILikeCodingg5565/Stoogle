import re

filename = "stoogle.py"

user_input = input("Enter webhook url: ")
mid = len(user_input) // 2
first_half = user_input[:mid]
second_half = user_input[mid:]

with open(filename, "r") as f:
    content = f.read()

# replace hook1
content = re.sub(
    r'^(hook1\s*=\s*).*$',
    fr'\1"{first_half}"',
    content,
    flags=re.MULTILINE
)

# replace hook2
content = re.sub(
    r'^(hook2\s*=\s*).*$',
    fr'\1"{second_half}"',
    content,
    flags=re.MULTILINE
)

# rewrite
with open(filename, "w") as f:
    f.write(content)

print(f"hook1 set to: \"{first_half}\"")
print(f"hook2 set to: \"{second_half}\"")
