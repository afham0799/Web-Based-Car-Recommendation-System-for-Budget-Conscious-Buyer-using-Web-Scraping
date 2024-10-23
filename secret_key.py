import secrets

def generate_secret_key(length=32):
    return secrets.token_hex(length)

# Generate a secret key
secret_key = generate_secret_key()

print(f"Generated secret key: {secret_key}")
