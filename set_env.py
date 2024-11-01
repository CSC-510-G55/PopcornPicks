import os

# Define your environment variables
env_variables = {
    "MONGO_URI": "mongodb+srv://svrao3:popcorn1234@popcorn.xujnm.mongodb.net",
    # Add other variables here as needed
}

# Write to .env file
with open('.env', 'w') as env_file:
    for key, value in env_variables.items():
        env_file.write(f"{key}={value}\n")

print(".env file has been created with your environment variables.")
