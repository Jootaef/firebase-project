# 🔥 Firebase To-Do List App

A Python-based To-Do List application built with Firebase Firestore and Firebase Authentication. This project demonstrates how to create a cloud-based task management system using Google's Firebase platform.

## 📋 Features

- ✅ **User Authentication**: Sign up and sign in with email/password
- 📝 **Task Management**: Create, read, update, and delete tasks
- 👤 **User-specific Tasks**: Each user can only see and manage their own tasks
- 🎯 **Task Status**: Mark tasks as done or pending
- 📅 **Timestamps**: Automatic creation timestamps for tasks
- 🖥️ **Interactive CLI**: User-friendly command-line interface
- 🎮 **Demo Mode**: Quick demonstration of all features

## 🛠️ Prerequisites

Before running this application, you need to:

1. **Create a Firebase Project**:

   - Go to [Firebase Console](https://console.firebase.google.com)
   - Click "Create a project" or select an existing project
   - Follow the setup wizard

2. **Enable Firestore Database**:

   - In your Firebase project, go to "Firestore Database"
   - Click "Create database"
   - Choose "Start in test mode" (for development)
   - Select a location for your database

3. **Enable Authentication**:

   - Go to "Authentication" in your Firebase project
   - Click "Get started"
   - Go to "Sign-in method" tab
   - Enable "Email/Password" provider

4. **Download Service Account Key**:
   - Go to Project Settings (gear icon)
   - Go to "Service accounts" tab
   - Click "Generate new private key"
   - Save the JSON file as `serviceAccountKey.json` in your project root

## 🚀 Installation

1. **Clone or download this project**:

   ```bash
   git clone <your-repo-url>
   cd Firebase
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Firebase credentials**:
   - Place your `serviceAccountKey.json` file in the project root directory

## 📁 Project Structure

```
Firebase/
├── todo_app.py              # Main application file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── serviceAccountKey.json  # Firebase service account key (you need to add this)
└── .gitignore             # Git ignore file
```

## 🎯 Usage

### Interactive Mode (Recommended)

Run the application in interactive mode for a full user experience:

```bash
python todo_app.py
```

This will start an interactive menu where you can:

- Sign up with a new account
- Sign in with existing account
- Add, view, update, and delete tasks
- Mark tasks as done/undone

### Demo Mode

Run a quick demonstration of all features:

```bash
python todo_app.py --demo
```

This will:

- Create a demo user
- Add sample tasks
- Display all tasks
- Show the basic functionality

### Programmatic Usage

You can also use the functions directly in your own code:

```python
from todo_app import *

# Initialize Firebase
initialize_firebase()

# Create a user
user_id = sign_up("user@example.com", "password123")

# Add a task
task_id = add_task(user_id, "Complete CSE 310 assignment", "Finish the cloud databases module")

# Get all tasks
tasks = get_tasks(user_id)

# Update a task
update_task(task_id, new_title="Updated task title")

# Mark task as done
mark_task_done(task_id, done=True)

# Delete a task
delete_task(task_id)
```

## 🔧 API Reference

### Authentication Functions

- `sign_up(email, password)`: Create a new user account
- `sign_in(email, password)`: Sign in existing user (returns user ID)

### Task Management Functions

- `add_task(user_id, title, description="")`: Add a new task
- `get_tasks(user_id)`: Get all tasks for a user
- `update_task(task_id, new_title=None, new_description=None, done=None)`: Update task fields
- `delete_task(task_id)`: Delete a task
- `mark_task_done(task_id, done=True)`: Mark task as done/undone

## 🗄️ Database Schema

The application uses Firestore with the following structure:

```
tasks (collection)
├── document_id
    ├── user_id: string
    ├── title: string
    ├── description: string
    ├── done: boolean
    └── created_at: timestamp
```

## 🔒 Security Rules

For production use, you should set up proper Firestore security rules. Here's a basic example:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.user_id;
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"serviceAccountKey.json not found"**

   - Make sure you've downloaded the service account key from Firebase Console
   - Ensure the file is named exactly `serviceAccountKey.json`
   - Place it in the same directory as `todo_app.py`

2. **"Permission denied" errors**

   - Check that your Firebase project has Firestore enabled
   - Verify that your service account has the necessary permissions
   - Ensure you're using the correct service account key

3. **Authentication errors**
   - Make sure Email/Password authentication is enabled in Firebase Console
   - Check that your service account has the "Firebase Admin" role

### Getting Help

If you encounter issues:

1. Check the Firebase Console for any error messages
2. Verify your service account key is valid
3. Ensure all dependencies are installed correctly
4. Check that Firestore and Authentication are properly configured

## 📝 License

This project is created for educational purposes as part of the CSE 310 Cloud Databases module.

## 👨‍💻 Author

Created by Jaydan for BYU CSE 310 Cloud Databases Module.

## 🎓 Learning Objectives

This project demonstrates:

- Cloud database integration with Firebase Firestore
- User authentication with Firebase Auth
- CRUD operations on cloud data
- Real-time data synchronization
- Security best practices for cloud applications
- Python integration with cloud services

---

**Happy coding! 🚀**
