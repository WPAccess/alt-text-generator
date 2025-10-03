#!/usr/bin/env python3
"""
Deployment Helper Script
Helps you deploy to GitHub and cloud platforms
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_status():
    """Check if git is initialized and has changes"""
    print("🔍 Checking git status...")
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("📦 Initializing git repository...")
        if not run_command("git init", "Git initialization"):
            return False
    
    # Check for changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Changes detected, ready to commit")
        return True
    else:
        print("✅ No changes to commit")
        return False

def setup_git_repo():
    """Setup git repository for deployment"""
    print("🚀 Setting up git repository for deployment...")
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Check if this is first commit
    result = subprocess.run("git log --oneline", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        commit_message = "Initial commit: Simple Alt Text Generator"
    else:
        commit_message = "Update: Alt text generator improvements"
    
    # Commit changes
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return False
    
    return True

def setup_remote_repo():
    """Setup remote GitHub repository"""
    print("🔗 Setting up remote GitHub repository...")
    
    # Check if remote already exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("✅ Remote repository already configured")
        return True
    
    # Get repository URL from user
    print("\n📋 GitHub Repository Setup:")
    print("1. Go to: https://github.com/new")
    print("2. Create a new repository (e.g., 'alt-text-generator')")
    print("3. Copy the repository URL")
    
    repo_url = input("\nEnter your GitHub repository URL: ").strip()
    if not repo_url:
        print("❌ Repository URL is required")
        return False
    
    # Add remote origin
    if not run_command(f"git remote add origin {repo_url}", "Adding remote origin"):
        return False
    
    return True

def push_to_github():
    """Push code to GitHub"""
    print("📤 Pushing to GitHub...")
    
    # Push to main branch
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        return False
    
    return True

def show_deployment_options():
    """Show deployment platform options"""
    print("\n🚀 Deployment Platform Options:")
    print("=" * 50)
    
    print("\n1. 🚄 Railway (Recommended):")
    print("   • Go to: https://railway.app/")
    print("   • Sign up with GitHub")
    print("   • Click 'Deploy from GitHub repo'")
    print("   • Select your repository")
    print("   • Add environment variables")
    print("   • Deploy automatically!")
    
    print("\n2. 🎨 Render:")
    print("   • Go to: https://render.com/")
    print("   • Sign up with GitHub")
    print("   • Create 'Background Worker'")
    print("   • Connect your repository")
    print("   • Set build command: pip install -r requirements.txt")
    print("   • Set start command: python simple_alt_generator.py")
    print("   • Add environment variables")
    print("   • Deploy!")
    
    print("\n3. 🟣 Heroku:")
    print("   • Go to: https://heroku.com/")
    print("   • Create new app")
    print("   • Connect GitHub repository")
    print("   • Enable automatic deployments")
    print("   • Add environment variables")
    print("   • Deploy!")
    
    print("\n📋 Environment Variables to Add:")
    print("   • GEMINI_API_KEY")
    print("   • GOOGLE_SHEETS_CREDENTIALS")
    print("   • ZOHO_CLIENT_ID")
    print("   • ZOHO_CLIENT_SECRET")
    print("   • ZOHO_REFRESH_TOKEN")
    print("   • SCHEDULE_TIME (optional)")

def main():
    """Main deployment function"""
    print("🚀 GitHub Deployment Helper")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('simple_alt_generator.py'):
        print("❌ Please run this script from the project directory")
        return
    
    # Check git status
    if not check_git_status():
        print("⚠️ No changes to deploy")
        return
    
    # Setup git repository
    if not setup_git_repo():
        print("❌ Git setup failed")
        return
    
    # Setup remote repository
    if not setup_remote_repo():
        print("❌ Remote repository setup failed")
        return
    
    # Push to GitHub
    if not push_to_github():
        print("❌ Push to GitHub failed")
        return
    
    print("\n🎉 Successfully pushed to GitHub!")
    print("=" * 40)
    
    # Show deployment options
    show_deployment_options()
    
    print("\n✅ Next Steps:")
    print("1. Choose a deployment platform (Railway recommended)")
    print("2. Connect your GitHub repository")
    print("3. Add environment variables")
    print("4. Deploy and start daily automation!")

if __name__ == "__main__":
    main()
