import base64
from Crypto.Cipher import AES
import os
import string

# Read the file to obtain the encoded/encrypted text.
f = open("bother_encoded.py", "r")
encoded_cipher_text = f.read()
f.close()

# The original program was 1) encrypted with AES and 2) encoded with base64.
# Let's begin by decoding the text.
all_characters = string.letters + string.digits
decoded_cipher_text = base64.b64decode(encoded_cipher_text)

# Now let's brute force it; for each two-character string, generate a SHA1 key, define a cipher on it
# and decrypt the text. If the decryption is correct, it will almost certainly have
# an 'import' (the assumption is that the author is using a library to make calls and send messages).
def decrypt_cipher():
	for i in all_characters:
		for j in all_characters:
			two_char_string = i + j

			f = os.popen("echo '" + two_char_string + "' | shasum")
			cipher = AES.new(f.readlines()[0][:16], AES.MODE_ECB)

			# Since import statements go on top, we will only decrypt the first 30 characters of the text.
			plain_text = cipher.decrypt(decoded_cipher_text[:32])

			if plain_text.find("import") != -1:
				return cipher.decrypt(decoded_cipher_text)
	return ""

decrypted_text = decrypt_cipher()
print decrypted_text

