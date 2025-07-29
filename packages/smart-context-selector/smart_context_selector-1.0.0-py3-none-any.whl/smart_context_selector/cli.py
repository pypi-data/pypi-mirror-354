#!/usr/bin/env python3
"""
Smart Context Selector - Command Line Interface
"""

import argparse
import sys
from .core import SmartContextSelector

def main():
    parser = argparse.ArgumentParser(
        description="Smart Context Selector - Create optimized documentation bundles for AI assistants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "build a slack bot with n8n"
  %(prog)s --prompt "create an AI agent" --config n8n --name my_agent
  %(prog)s --prompt "API integration" --config-file custom.json
  %(prog)s --list-configs
        """
    )
    
    # Main arguments
    parser.add_argument(
        "--prompt", "-p", 
        help="Prompt describing what you want to build"
    )
    
    parser.add_argument(
        "--name", "-n", 
        help="Custom bundle name"
    )
    
    parser.add_argument(
        "--config", "-c", 
        default="n8n",
        help="Built-in configuration to use (default: n8n)"
    )
    
    parser.add_argument(
        "--config-file", 
        help="Path to custom configuration JSON file"
    )
    
    parser.add_argument(
        "--docs-dir", 
        help="Override documentation directory from config"
    )
    
    parser.add_argument(
        "--max-files", 
        type=int, 
        default=120,
        help="Maximum number of files to include (default: 120)"
    )
    
    parser.add_argument(
        "--push", 
        action="store_true", 
        help="Push bundle to GitHub after creation"
    )
    
    # Utility arguments
    parser.add_argument(
        "--list-configs", 
        action="store_true",
        help="List available built-in configurations"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="Smart Context Selector 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Handle list configs
    if args.list_configs:
        try:
            selector = SmartContextSelector()
            configs = selector.list_available_configs()
            print("📋 Available built-in configurations:")
            for config in configs:
                print(f"  • {config}")
            print(f"\nUsage: --config {configs[0] if configs else 'CONFIG_NAME'}")
        except Exception as e:
            print(f"❌ Error listing configs: {e}")
        return
    
    # Validate required arguments
    if not args.prompt:
        parser.error("--prompt is required (or use --list-configs)")
    
    print("🎯 Smart Context Selector")
    print("=" * 50)
    
    try:
        # Initialize selector
        selector = SmartContextSelector(
            config_name=args.config,
            config_file=args.config_file,
            docs_dir=args.docs_dir
        )
        
        # Create the bundle
        bundle_dir = selector.create_context_bundle(
            prompt=args.prompt, 
            bundle_name=args.name
        )
        
        # Push to GitHub if requested
        if args.push:
            selector.push_to_github(bundle_dir)
        
        print(f"\n🎉 Done! Your smart context bundle is ready:")
        print(f"📁 {bundle_dir}")
        print(f"\n💡 Next steps:")
        print(f"1. Upload this folder to your AI assistant")
        print(f"2. Use your original prompt with the AI")
        print(f"3. The AI will have optimal context for helping you!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()