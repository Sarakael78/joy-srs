#!/usr/bin/env python3
"""
Script to create users and generate the USERS environment variable for Vercel.
"""

import json
import hashlib
import os

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, hash_value = hashed_password.split('$')
        computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return computed_hash == hash_value
    except:
        return False

def create_users():
    """Create users interactively."""
    users = {}
    
    print("🔐 Legal Strategy Infographics - User Setup")
    print("=" * 50)
    print("This script will help you create users for the platform.")
    print("Enter 'done' when finished adding users.\n")
    
    while True:
        username = input("Enter username (or 'done' to finish): ").strip()
        
        if username.lower() == 'done':
            break
            
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
            
        if username in users:
            print(f"User '{username}' already exists. Please choose a different username.")
            continue
            
        password = input(f"Enter password for '{username}': ").strip()
        
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
            
        # Hash the password
        hashed_password = hash_password(password)
        users[username] = hashed_password
        
        print(f"✅ User '{username}' created successfully!\n")
    
    if not users:
        print("No users were created. Exiting.")
        return
    
    # Generate the JSON string for environment variable
    users_json = json.dumps(users)
    
    print("\n🎉 User setup complete!")
    print("=" * 50)
    print(f"Created {len(users)} user(s):")
    for username in users:
        print(f"  - {username}")
    
    print("\n📋 Add this environment variable to Vercel:")
    print("=" * 50)
    print("USERS=" + users_json)
    print("=" * 50)
    
    print("\n📝 Instructions:")
    print("1. Go to your Vercel project dashboard")
    print("2. Navigate to Settings > Environment Variables")
    print("3. Add a new variable:")
    print("   - Name: USERS")
    print("   - Value: " + users_json)
    print("4. Save and redeploy your project")
    
    # Save to file for reference
    with open("users_config.json", "w") as f:
        json.dump(users, f, indent=2)
    
    print("\n💾 User configuration saved to: users_config.json")

if __name__ == "__main__":
    create_users()
