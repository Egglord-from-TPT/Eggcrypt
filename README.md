# eggcrypt

A pretty secure (yet inneficient) encryption program.

This is my fifth python library :D

Commands:

eggcrypt.encrypt("text", "key") # Returns an encrypted string.

eggcrypt.decrypt("ciphertext", "key") # Returns a non-encrypted string.

eggcrypt.key("") # Returns a random key/seed if no arguments, uses the string/intiger input if given to generate a deterministic output.

eggcrypt.hash("") # Uses a custom method to hash a string. Input: str or int.

# !NB!

Use: pip install eggcrypt

But, to import it: import eggcrypt
