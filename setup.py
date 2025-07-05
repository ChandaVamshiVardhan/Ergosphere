#!/usr/bin/env python
"""
Setup script for Smart Todo application.
This script helps users quickly set up the application.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_node_version():
    """Check if Node.js version is compatible"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✓ Node.js version {version} found")
        return True
    except FileNotFoundError:
        print("✗ Node.js is not installed or not in PATH")
        print("Please install Node.js 18 or higher from https://nodejs.org/")
        return False

def setup_backend():
    """Setup the Django backend"""
    print("\n" + "="*50)
    print("SETTING UP BACKEND")
    print("="*50)
    
    # Check if virtual environment exists
    venv_path = "venv" if platform.system() != "Windows" else "venv"
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file...")
        env_content = """SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite:///db.sqlite3
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Created .env file")
    
    # Run Django migrations
    if not run_command(f"{activate_cmd} && python manage.py makemigrations", "Creating Django migrations"):
        return False
    
    if not run_command(f"{activate_cmd} && python manage.py migrate", "Running Django migrations"):
        return False
    
    # Create sample data
    if not run_command(f"{activate_cmd} && python sample_data.py", "Creating sample data"):
        return False
    
    print("✓ Backend setup completed!")
    return True

def setup_frontend():
    """Setup the Next.js frontend"""
    print("\n" + "="*50)
    print("SETTING UP FRONTEND")
    print("="*50)
    
    # Navigate to frontend directory
    if not os.path.exists('frontend'):
        print("✗ Frontend directory not found")
        return False
    
    os.chdir('frontend')
    
    # Install dependencies
    if not run_command("npm install", "Installing Node.js dependencies"):
        return False
    
    # Create .env.local file if it doesn't exist
    if not os.path.exists('.env.local'):
        print("Creating .env.local file...")
        env_content = "NEXT_PUBLIC_API_URL=http://localhost:8000/api\n"
        with open('.env.local', 'w') as f:
            f.write(env_content)
        print("✓ Created .env.local file")
    
    os.chdir('..')
    print("✓ Frontend setup completed!")
    return True

def main():
    """Main setup function"""
    print("🚀 Smart Todo Setup Script")
    print("="*50)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_node_version():
        return
    
    # Setup backend
    if not setup_backend():
        print("\n✗ Backend setup failed. Please check the errors above.")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("\n✗ Frontend setup failed. Please check the errors above.")
        return
    
    print("\n" + "="*50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nNext steps:")
    print("1. Update the .env file with your OpenAI API key (optional)")
    print("2. Start the backend server:")
    print("   python manage.py runserver")
    print("3. Start the frontend server (in a new terminal):")
    print("   cd frontend && npm run dev")
    print("\nThe application will be available at:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000/api")
    print("   Admin Panel: http://localhost:8000/admin")
    print("\nHappy coding! 🎯")

if __name__ == '__main__':
    main() 