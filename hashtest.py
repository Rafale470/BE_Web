import hashlib
password = "Test"

password = hashlib.sha256(password.encode())
passwordC = password.hexdigest()

print(passwordC)