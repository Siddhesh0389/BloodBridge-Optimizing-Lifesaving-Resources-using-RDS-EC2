import pymysql

# Try different password combinations
passwords_to_try = [
    '',           # Empty password (XAMPP/WAMP default)
    'root',       # Common password
    'Abcd@1234',   # Another common password
    'mysql',      # Another common password
    '123456',     # Simple password
]

print("Testing MySQL connections...")
print("-" * 40)

for password in passwords_to_try:
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            charset='utf8mb4'
        )
        print(f"✓ SUCCESS! Password is: '{password}'")
        connection.close()
        break
    except pymysql.Error as e:
        print(f"✗ Failed with password: '{password}' - Error: {e.args[0]}")

print("-" * 40)