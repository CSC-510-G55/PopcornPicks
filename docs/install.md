# Steps for setting up the repository and running the web app

## Step 1: Git Clone the Repository
```bash
git clone https://github.com/se24ncsu/PopcornPicks.git
```
(OR) Download the .zip file on your local machine from the following link
https://github.com/se24ncsu/PopcornPicks/

## Step 2: Install the required packages
Run the following command in the terminal:
```bash
pip install -r requirements.txt
```

## Step 3: MongoDB Atlas Setup
1. Create a free account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (free tier is sufficient)
3. In the Security tab, create a database user with read/write privileges
4. In Network Access, add your IP address or allow access from anywhere (0.0.0.0/0)
5. Click "Connect" and choose "Connect your application"
6. Copy the connection string
7. Replace `<password>` with your database user password
8. Add this connection string to either:
   - Your GitHub repository secrets as `MONGO_URI`
   - In `set_env.py` file:
     ```python
     MONGO_URI = "your_connection_string_here"
     ```

## Step 4: Node.js and npm Setup
1. Download and install [Node.js](https://nodejs.org/) (includes npm)
2. Verify installation:
```bash
node --version
npm --version
```

## Step 5: Frontend Setup
Navigate to the React frontend directory and install dependencies:
```bash
cd react-frontend
npm install
```

## Step 6: Start the Backend Server
From the main directory, run:
```bash
python -m src.recommenderapp.app
```

## Step 7: Start the Frontend Server
In a new terminal, navigate to the React frontend directory:
```bash
cd react-frontend
npm start
```

## Step 8: Open the URL in your browser
```
http://localhost:3000
```

**NOTE: For the email notifier feature - create a new gmail account, replace the sender_email variable with the new email and sender_password variable with its password (2 factor authentication) in the utils.py file (function: send_email_to_user(recipient_email, categorized_data)).**