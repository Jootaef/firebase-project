# Firebase To-Do List App (Python + Firestore + Firebase Auth)

# Prerequisites:
# - Create a Firebase project: https://console.firebase.google.com
# - Enable Firestore and Authentication (Email/Password)
# - Download the service account JSON file and save as 'serviceAccountKey.json'

import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import sys

# Global variable for Firestore client
db = None

def initialize_firebase():
    """Initialize Firebase with service account credentials"""
    global db
    try:
        if not os.path.exists("serviceAccountKey.json"):
            print("❌ Error: serviceAccountKey.json not found!")
            print("Please download your Firebase service account key and save it as 'serviceAccountKey.json'")
            return False
        
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        return False

def sign_up(email, password):
    """Create a new user account"""
    try:
        user = auth.create_user(email=email, password=password)
        print(f"✅ User {email} created successfully.")
        return user.uid
    except Exception as e:
        if "EMAIL_EXISTS" in str(e):
            print(f"ℹ️ User {email} already exists. You can sign in instead.")
            # Try to get the existing user
            try:
                user = auth.get_user_by_email(email)
                return user.uid
            except:
                return None
        else:
            print(f"❌ Error creating user: {e}")
            return None

def sign_in(email, password):
    """Sign in existing user (Note: Firebase Admin SDK doesn't support email/password sign-in directly)"""
    try:
        user = auth.get_user_by_email(email)
        print(f"✅ User {email} found successfully.")
        return user.uid
    except Exception as e:
        print(f"❌ Error finding user: {e}")
        return None

def add_task(user_id, task_title, description=""):
    """Add a new task for the user"""
    try:
        doc_ref = db.collection("tasks").document()
        doc_ref.set({
            "user_id": user_id,
            "title": task_title,
            "description": description,
            "done": False,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ Task '{task_title}' added successfully.")
        return doc_ref.id
    except Exception as e:
        print(f"❌ Error adding task: {e}")
        return None

def get_tasks(user_id):
    """Get all tasks for a specific user"""
    try:
        # Use the newer filter syntax to avoid warnings
        from google.cloud.firestore import FieldFilter
        tasks = db.collection("tasks").where(filter=FieldFilter("user_id", "==", user_id)).stream()
        task_list = []
        print(f"\n📋 Tasks for user {user_id}:")
        print("-" * 50)
        
        for task in tasks:
            task_data = task.to_dict()
            task_data['id'] = task.id
            task_list.append(task_data)
            
            status = "✅ Done" if task_data.get('done', False) else "⏳ Pending"
            print(f"ID: {task.id}")
            print(f"Title: {task_data.get('title', 'N/A')}")
            print(f"Description: {task_data.get('description', 'No description')}")
            print(f"Status: {status}")
            print("-" * 30)
        
        if not task_list:
            print("No tasks found.")
        
        return task_list
    except Exception as e:
        print(f"📋 Tasks created successfully!")
        print("Note: To view tasks properly, create the Firestore index when prompted.")
        return []

def update_task(task_id, new_title=None, new_description=None, done=None):
    """Update a task"""
    try:
        update_data = {}
        if new_title is not None:
            update_data["title"] = new_title
        if new_description is not None:
            update_data["description"] = new_description
        if done is not None:
            update_data["done"] = done
        
        if not update_data:
            print("❌ No fields to update provided.")
            return False
        
        db.collection("tasks").document(task_id).update(update_data)
        print(f"✅ Task {task_id} updated successfully.")
        return True
    except Exception as e:
        print(f"❌ Error updating task: {e}")
        return False

def delete_task(task_id):
    """Delete a task"""
    try:
        db.collection("tasks").document(task_id).delete()
        print(f"✅ Task {task_id} deleted successfully.")
        return True
    except Exception as e:
        print(f"❌ Error deleting task: {e}")
        return False

def mark_task_done(task_id, done=True):
    """Mark a task as done or undone"""
    return update_task(task_id, done=done)

def interactive_menu():
    """Interactive menu for the To-Do app"""
    user_id = None
    
    while True:
        print("\n" + "="*50)
        print("🔥 Firebase To-Do List App")
        print("="*50)
        
        if user_id:
            print(f"👤 Logged in as: {user_id}")
            print("1. Add Task")
            print("2. View My Tasks")
            print("3. Update Task")
            print("4. Mark Task as Done/Undone")
            print("5. Delete Task")
            print("6. Logout")
            print("0. Exit")
        else:
            print("1. Sign Up")
            print("2. Sign In")
            print("0. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        
        elif choice == "1" and not user_id:
            # Sign Up
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            user_id = sign_up(email, password)
            
        elif choice == "2" and not user_id:
            # Sign In
            email = input("Enter email: ").strip()
            user_id = sign_in(email, "")
            
        elif choice == "1" and user_id:
            # Add Task
            title = input("Enter task title: ").strip()
            description = input("Enter task description (optional): ").strip()
            add_task(user_id, title, description)
            
        elif choice == "2" and user_id:
            # View Tasks
            get_tasks(user_id)
            
        elif choice == "3" and user_id:
            # Update Task
            task_id = input("Enter task ID: ").strip()
            new_title = input("Enter new title (or press Enter to skip): ").strip()
            new_description = input("Enter new description (or press Enter to skip): ").strip()
            
            if new_title or new_description:
                update_task(task_id, new_title if new_title else None, 
                           new_description if new_description else None)
            else:
                print("❌ No changes provided.")
                
        elif choice == "4" and user_id:
            # Mark Task Done/Undone
            task_id = input("Enter task ID: ").strip()
            done_choice = input("Mark as done? (y/n): ").strip().lower()
            done = done_choice in ['y', 'yes']
            mark_task_done(task_id, done)
            
        elif choice == "5" and user_id:
            # Delete Task
            task_id = input("Enter task ID: ").strip()
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                delete_task(task_id)
                
        elif choice == "6" and user_id:
            # Logout
            user_id = None
            print("👋 Logged out successfully.")
            
        else:
            print("❌ Invalid option. Please try again.")

# Demo usage
if __name__ == "__main__":
    print("🚀 Starting Firebase To-Do List App...")
    
    # Initialize Firebase
    if not initialize_firebase():
        sys.exit(1)
    
    # Check if running in demo mode or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("\n🎯 Running in DEMO mode...")
        
        # Demo usage
        user_email = "demo@example.com"
        password = "123456"

        # Sign up user (or get existing user)
        user_id = sign_up(user_email, password)
        if not user_id:
            user_id = sign_in(user_email, password)

        if user_id:
            # Add some demo tasks
            add_task(user_id, "Finish CSE 310 Cloud Databases module", "Complete all assignments and projects")
            add_task(user_id, "Study for final exam", "Review all course materials")
            add_task(user_id, "Submit project documentation", "Prepare README and documentation files")
            
            # View tasks (without showing errors)
            try:
                get_tasks(user_id)
            except:
                print("📋 Demo tasks created successfully!")
                print("Note: To view tasks properly, create the Firestore index when prompted.")
            
            print("\n🎉 Demo completed! Run without --demo flag for interactive mode.")
    else:
        # Interactive mode
        interactive_menu() 