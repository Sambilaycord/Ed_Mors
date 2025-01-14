import hashlib

def hash_password(password):
    # Generate a salted hash using SHA-256
    salt = "Edmore"  # You should use a unique and random salt for each user
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password, salt

def verify_password(hashed_password, salt, password_to_check):
    # Verify the password during login
    salted_password = password_to_check + salt
    return hashed_password == hashlib.sha256(salted_password.encode()).hexdigest()

# Example of registering a new user
new_password = "deliverydept123"
hashed_password, salt = hash_password(new_password)
print(hash_password(new_password))

# Store the hashed_password and salt in the database along with other user details

# Example of checking the password during login
input_password = "hello"

if verify_password(hashed_password, salt, input_password):
    print("Password is correct!")
else:
    print("Incorrect password!")
