# Troubleshooting Guide

## MongoDB with Github Actions

### Cannot connect to MongoDB Atlas
When working with MongoDB and Github Actions, you may encounter connectivity issues. Here are common problems and their solutions:

#### Database Connection Errors
If you receive an error like `cannot find 'testdb.table'` or `MongoNetworkError: connection failed`, check the following:

1. **Environment Variables**
   - Ensure `MONGO_URI` is properly set in your Github Secrets
   - Verify the connection string format: 
     ```
     mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority
     ```
   - Check if special characters in password are properly URL encoded
   - Confirm the database name is correct (case-sensitive)

2. **Network Access**
   - Verify IP address is whitelisted in MongoDB Atlas
   - For Github Actions, allow access from `0.0.0.0/0` temporarily during CI/CD
   - Check if the cluster is active and running

3. **Authentication Issues**
   - Confirm user credentials are correct
   - Verify user has appropriate database access roles
   - Check if the user is associated with the correct database

4. **Database/Collection Case Sensitivity**
   - MongoDB is case-sensitive for database and collection names
   - Example: `testDb.Users` is different from `testdb.users`
   - Use consistent naming conventions throughout your codebase

## React Application Issues

### Development Server Problems

#### Node.js and npm Version Incompatibility
If you encounter React build or start errors:

1. **Version Verification**
   ```bash
   node --version  # Should be >= 14.0.0
   npm --version   # Should be >= 6.14.0
   ```

2. **Dependency Issues**
   - Clear npm cache:
     ```bash
     npm cache clean --force
     ```
   - Delete node_modules and reinstall:
     ```bash
     rm -rf node_modules
     rm package-lock.json
     npm install
     ```
   - Check for peer dependency conflicts:
     ```bash
     npm ls
     ```

3. **Build Errors**
   - Check for missing dependencies in package.json
   - Ensure all required dev dependencies are installed
   - Verify babel and webpack configurations

### Common React Error Messages

1. **Module Not Found**
   ```
   Module not found: Can't resolve 'package-name'
   ```
   - Solution: Install missing package
   ```bash
   npm install package-name
   ```

2. **Invalid Hook Call**
   - Ensure React version is consistent across all dependencies
   - Check for multiple React installations:
   ```bash
   npm ls react
   ```

## Application Access Issues

### Cannot Access Website

#### Port Configuration Problems
If you're unable to access the application, check the following:

1. **React Development Server**
   - Default port: 3000
   - Check if port is already in use:
     ```bash
     # Windows
     netstat -ano | findstr :3000
     
     # Linux/Mac
     lsof -i :3000
     ```
   - Configure different port:
     ```bash
     # In package.json
     "scripts": {
       "start": "PORT=3001 react-scripts start"
     }
     ```

2. **Flask Backend Server**
   - Default port: 5000
   - Verify Flask configuration:
     ```python
     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=5000)
     ```
   - Check port availability:
     ```bash
     # Windows
     netstat -ano | findstr :5000
     
     # Linux/Mac
     lsof -i :5000
     ```

3. **CORS Configuration**
   - Ensure CORS is properly configured in Flask:
     ```python
     from flask_cors import CORS
     
     app = Flask(__name__)
     CORS(app, resources={r"/*": {"origins": "*"}})
     ```
   - Check React API calls use correct backend URL

4. **Proxy Settings**
   - Verify proxy configuration in package.json:
     ```json
     {
       "proxy": "http://localhost:5000"
     }
     ```
   - Ensure environment variables are set correctly:
     ```
     REACT_APP_API_URL=http://localhost:5000
     ```

### Network Issues
1. **Firewall Settings**
   - Check if ports are blocked by firewall
   - Allow incoming/outgoing connections for required ports

## Environment Setup

### Development Environment Checklist
- [ ] Node.js and npm installed and updated
- [ ] Python and pip installed
- [ ] MongoDB Atlas account configured
- [ ] Environment variables set
- [ ] Required ports available
- [ ] Git configuration complete
- [ ] IDE/editor setup properly

Always check the application logs for specific error messages and stack traces when troubleshooting. Most issues can be resolved by ensuring proper configuration and environment setup.