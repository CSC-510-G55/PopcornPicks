"""
This script will create a .env file with environment variables.
"""

env_variables = {
    "MONGO_URI": "mongodb+srv://svrao3:popcorn1234@popcorn.xujnm.mongodb.net",
    "APP_PASSWORD": "tnjydyefhlpsmdao",
    "REACT_APP_API_URL": "http://127.0.0.1:5000"

}

with open(".env", "w", encoding="utf-8") as env_file:
    for key, value in env_variables.items():
        env_file.write(f"{key}={value}\n")

print(".env file has been created with your environment variables.")

with open("./react-frontend/.env", "w", encoding="utf-8") as env_file:
    for key, value in env_variables.items():
        env_file.write(f"{key}={value}\n")

print(".env file has been created with your environment variables.")
