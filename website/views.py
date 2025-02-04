from werkzeug.security import generate_password_hash


#passwords = ["admin123", "student123", "fixer123"]

#for password in passwords:
 #   print(f"Password: {password} -> Hashed: {generate_password_hash(password)}")

from werkzeug.security import generate_password_hash
print(generate_password_hash("admin123", method="scrypt"))
