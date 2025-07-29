#!/usr/bin/env python
"""Jujutsu CLI implementation."""

import argparse
import sys
import os
from pathlib import Path

__version__ = "0.0.1"

def get_command_name():
    """現在実行されているコマンド名を取得"""
    script_name = Path(sys.argv[0]).name
    # エイリアスの検出
    if script_name in ["jujutsu", "jutsu", "jjz", "jj2"]:
        return script_name
    return "jujutsu"

def print_banner(command_name):
    """コマンドに応じたバナーを表示"""
    banners = {
        "jujutsu": "🥋 Jujutsu - Mastering CLI with Style",
        "jutsu": "⚡ Jutsu - Quick CLI Techniques",
        "jjz": "🔥 JJZ - Lightning Fast Commands",
        "jj2": "🚀 JJ2 - Advanced CLI Operations"
    }
    print(banners.get(command_name, banners["jujutsu"]))
    print(f"Version: {__version__}")
    print("-" * 40)

def cmd_init():
    """Initialize a new project"""
    print("📁 Initializing new jujutsu project...")
    print("✅ Project initialized successfully!")

def cmd_status():
    """Show project status"""
    print("📊 Project Status:")
    print("• Status: Active")
    print("• Files: Ready")
    print("• Last update: Just now")

def cmd_help():
    """Show help information"""
    print("📚 Available Commands:")
    print("  init     - Initialize a new project")
    print("  status   - Show project status")
    print("  version  - Show version information")
    print("  help     - Show this help message")
    print("\n🔧 Available Aliases:")
    print("  jujutsu, jutsu, jjz, jj2 - All work the same way!")

def main():
    """メインエントリーポイント"""
    parser = argparse.ArgumentParser(
        description="Jujutsu CLI - Powerful development tool with multiple aliases",
        prog=get_command_name()
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["init", "status", "help"],
        default="help",
        help="Command to execute"
    )
    
    args = parser.parse_args()
    command_name = get_command_name()
    
    # バナー表示
    print_banner(command_name)
    print()
    
    # コマンド実行
    if args.command == "init":
        cmd_init()
    elif args.command == "status":
        cmd_status()
    elif args.command == "help":
        cmd_help()
    else:
        cmd_help()

if __name__ == "__main__":
    main() 