#!/usr/bin/env python3
"""
Test script to verify Firebase setup and basic functionality
"""

import os
import sys
from todo_app import initialize_firebase, sign_up, add_task, get_tasks

def test_firebase_connection():
    """Test if Firebase can be initialized and connected"""
    print("🧪 Testing Firebase connection...")
    
    if not os.path.exists("serviceAccountKey.json"):
        print("❌ serviceAccountKey.json not found!")
        print("Please download your Firebase service account key and save it as 'serviceAccountKey.json'")
        return False
    
    try:
        if initialize_firebase():
            print("✅ Firebase connection successful!")
            return True
        else:
            print("❌ Firebase connection failed!")
            return False
    except Exception as e:
        print(f"❌ Error testing Firebase connection: {e}")
        return False

def test_basic_operations():
    """Test basic CRUD operations"""
    print("\n🧪 Testing basic operations...")
    
    try:
        # Test user creation
        test_email = "test@example.com"
        test_password = "test123456"
        
        print("Creating test user...")
        user_id = sign_up(test_email, test_password)
        
        if not user_id:
            print("❌ User creation failed!")
            return False
        
        print(f"✅ Test user created with ID: {user_id}")
        
        # Test task creation
        print("Creating test task...")
        task_id = add_task(user_id, "Test task", "This is a test task")
        
        if not task_id:
            print("❌ Task creation failed!")
            return False
        
        print(f"✅ Test task created with ID: {task_id}")
        
        # Test task retrieval
        print("Retrieving tasks...")
        tasks = get_tasks(user_id)
        
        if len(tasks) > 0:
            print("✅ Task retrieval successful!")
        else:
            print("❌ No tasks found!")
            return False
        
        print("✅ All basic operations test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during basic operations test: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Firebase To-Do App Setup Test")
    print("=" * 40)
    
    # Test Firebase connection
    if not test_firebase_connection():
        print("\n❌ Setup test failed! Please check your Firebase configuration.")
        sys.exit(1)
    
    # Test basic operations
    if not test_basic_operations():
        print("\n❌ Basic operations test failed!")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Your Firebase To-Do app is ready to use.")
    print("\nYou can now run:")
    print("  python todo_app.py          # Interactive mode")
    print("  python todo_app.py --demo   # Demo mode")

if __name__ == "__main__":
    main() 