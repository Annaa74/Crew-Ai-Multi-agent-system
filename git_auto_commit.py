#!/usr/bin/env python3
"""
Continuous Git Commit Helper
Automatically commits and pushes changes to GitHub
Run: python git_auto_commit.py [--message "commit message"] [--push]
"""

import subprocess
import sys
import argparse
from datetime import datetime
import os


def run_command(cmd, capture=False):
    """Execute a shell command and return output"""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.returncode
        else:
            result = subprocess.run(cmd, shell=True)
            return "", result.returncode
    except Exception as e:
        print(f"❌ Error executing command: {str(e)}")
        return "", 1


def get_git_status():
    """Check if there are any changes to commit"""
    output, code = run_command("git status --short", capture=True)
    return output, code == 0


def get_commit_message(args):
    """Generate or use provided commit message"""
    if args.message:
        return args.message
    
    # Generate based on changes
    status, _ = get_git_status()
    
    if not status:
        print("✅ No changes to commit")
        return None
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    changes = len(status.split('\n'))
    
    return f"chore: Auto-commit {changes} file(s) - {timestamp}"


def main():
    parser = argparse.ArgumentParser(description="Auto-commit and push to GitHub")
    parser.add_argument("--message", "-m", help="Custom commit message")
    parser.add_argument("--push", "-p", action="store_true", help="Push to remote after commit")
    parser.add_argument("--branch", "-b", default="main", help="Branch to push to (default: main)")
    
    args = parser.parse_args()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("📊 Checking git status...")
    status, success = get_git_status()
    
    if not status:
        print("✅ No changes detected")
        return 0
    
    print("\n📝 Changes detected:")
    print(status)
    
    # Stage changes
    print("\n📦 Staging changes...")
    _, code = run_command("git add -A")
    if code != 0:
        print("❌ Failed to stage changes")
        return 1
    
    # Get commit message
    message = get_commit_message(args)
    if not message:
        return 0
    
    # Commit
    print(f"\n💾 Creating commit: '{message}'")
    _, code = run_command(f'git commit -m "{message}"')
    if code != 0:
        print("❌ Failed to create commit")
        return 1
    
    print("✅ Commit successful!")
    
    # Push if requested
    if args.push:
        print(f"\n🚀 Pushing to origin/{args.branch}...")
        _, code = run_command(f"git push -u origin {args.branch}")
        if code != 0:
            print("❌ Failed to push")
            return 1
        print("✅ Push successful!")
    else:
        print(f"\n💡 Run with --push to push changes to remote")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
