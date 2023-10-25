

import re



original_string = "cd053!@#$%&*()6c2b57c4ae3e!@#$%&*()9c02d002583a134-us21"
word_to_remove = "!@#$%&*()"

# Create a regular expression pattern to match the word
pattern = r'\b' + re.escape(word_to_remove) + r'\b'

# Remove the word from the string
new_string = re.sub(pattern, '', original_string)

print(new_string)
