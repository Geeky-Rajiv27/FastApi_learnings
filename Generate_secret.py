import secrets

SECRET_KEY = secrets.token_hex(32)
print(f"The code is : {SECRET_KEY}")