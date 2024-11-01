"""
This script will create a .env file with environment variables.
"""

env_variables = {
    "MONGO_URI": "mongodb+srv://svrao3:popcorn1234@popcorn.xujnm.mongodb.net",
}

with open(".env", "w",encoding="utf-8") as env_file:
    for key, value in env_variables.items():
        env_file.write(f"{key}={value}\n")

print(".env file has been created with your environment variables.")
