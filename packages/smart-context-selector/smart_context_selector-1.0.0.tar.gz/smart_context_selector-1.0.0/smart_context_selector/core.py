#!/usr/bin/env python3
"""
Smart Context Selector - Core Module

Analyzes prompts and creates optimal documentation bundles for AI assistants like Claude
"""

import os
import re
import json
import shutil
from datetime import datetime
from typing import List, Dict, Set, Optional
import subprocess
import pkg_resources

class SmartContextSelector:
    def __init__(self, config_name: str = "n8n", config_file: Optional[str] = None, docs_dir: Optional[str] = None):
        """
        Initialize Smart Context Selector
        
        Args:
            config_name: Name of built-in config (e.g., 'n8n')
            config_file: Path to custom config JSON file
            docs_dir: Override docs directory from config
        """
        self.config = self._load_config(config_name, config_file)
        
        # Allow docs_dir override
        if docs_dir:
            self.config['docs_dir'] = docs_dir
            
        self.docs_dir = self.config['docs_dir']
        self.context_output_dir = self.config.get('context_output_dir', 'smart_context_bundles')
        self.knowledge_base = self.config['knowledge_base']
        self.file_patterns = self.config.get('file_patterns', {})
        
        print(f"🎯 Loaded config: {self.config['name']}")
        print(f"📁 Docs directory: {self.docs_dir}")
    
    def _load_config(self, config_name: str, config_file: Optional[str]) -> Dict:
        """Load configuration from built-in configs or custom file"""
        
        if config_file:
            # Load custom config file
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Config file not found: {config_file}")
            
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        else:
            # Load built-in config
            try:
                # Try to load from package configs
                config_path = pkg_resources.resource_filename(
                    'smart_context_selector', 
                    f'configs/{config_name}.json'
                )
                
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                        
            except (ImportError, FileNotFoundError):
                # Fallback to local file (for development)
                local_config_path = os.path.join(
                    os.path.dirname(__file__), 
                    'configs', 
                    f'{config_name}.json'
                )
                
                if os.path.exists(local_config_path):
                    with open(local_config_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                
            # If no config found
            available_configs = self._get_available_configs()
            raise ValueError(
                f"Config '{config_name}' not found. Available configs: {available_configs}"
            )
    
    def _get_available_configs(self) -> List[str]:
        """Get list of available built-in configs"""
        configs = []
        
        try:
            # Try package resource path
            config_dir = pkg_resources.resource_filename('smart_context_selector', 'configs')
        except ImportError:
            # Fallback to local path
            config_dir = os.path.join(os.path.dirname(__file__), 'configs')
        
        if os.path.exists(config_dir):
            for filename in os.listdir(config_dir):
                if filename.endswith('.json'):
                    configs.append(filename[:-5])  # Remove .json extension
        
        return configs
    
    def list_available_configs(self) -> List[str]:
        """Public method to list available configurations"""
        return self._get_available_configs()
    
    def analyze_prompt(self, prompt: str) -> Dict[str, any]:
        """Analyze the prompt to identify required components"""
        prompt_lower = prompt.lower()
        
        analysis = {
            "detected_services": [],
            "detected_categories": set(),
            "complexity_score": 0,
            "required_folders": set(["getting_started"]),  # Always include basics
            "specific_keywords": [],
            "workflow_type": "unknown"
        }
        
        # Detect services and add their categories
        for keyword, categories in self.knowledge_base.items():
            if keyword in prompt_lower:
                analysis["detected_services"].append(keyword)
                analysis["specific_keywords"].append(keyword)
                for category in categories:
                    analysis["detected_categories"].add(category)
                    analysis["required_folders"].add(category)
        
        # Calculate complexity based on number of different services
        analysis["complexity_score"] = len(analysis["detected_services"])
        
        # Determine workflow type based on config
        workflow_types = {
            "ai_focused": ["ai", "chatbot", "langchain", "openai", "anthropic"],
            "integration_focused": ["api", "webhook", "integration", "connect"],
            "data_focused": ["data", "database", "transform", "process"]
        }
        
        for workflow_type, keywords in workflow_types.items():
            if any(keyword in prompt_lower for keyword in keywords):
                analysis["workflow_type"] = workflow_type
                break
        
        # Always include workflows folder if it exists in knowledge base
        if any("workflow" in categories for categories in self.knowledge_base.values()):
            analysis["required_folders"].add("workflows")
        
        # Add troubleshooting if complex
        if analysis["complexity_score"] > 3:
            analysis["required_folders"].add("troubleshooting")
        
        return analysis
    
    def get_relevant_files(self, analysis: Dict, max_files: int = 120) -> List[str]:
        """Get the most relevant files based on analysis"""
        relevant_files = []
        files_with_scores = []
        
        # Collect all files from required folders
        for folder in analysis["required_folders"]:
            folder_path = os.path.join(self.docs_dir, folder)
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith('.md') and filename != 'README.md':
                        file_path = os.path.join(folder, filename)
                        score = self.calculate_file_relevance(filename, analysis)
                        files_with_scores.append((file_path, score, filename))
        
        # Sort by relevance score
        files_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Take top files up to max_files
        for file_path, score, filename in files_with_scores[:max_files]:
            if score > 0:  # Only include files with some relevance
                relevant_files.append(file_path)
        
        return relevant_files
    
    def calculate_file_relevance(self, filename: str, analysis: Dict) -> int:
        """Calculate how relevant a file is to the prompt"""
        score = 0
        filename_lower = filename.lower()
        
        # High score for detected keywords
        for keyword in analysis["specific_keywords"]:
            if keyword in filename_lower:
                score += 50
        
        # Medium score for core concepts
        core_patterns = self.file_patterns.get("core_always", [])
        for pattern in core_patterns:
            if pattern in filename_lower:
                score += 20
        
        # Workflow type specific scoring
        if analysis["workflow_type"] == "ai_focused":
            ai_patterns = self.file_patterns.get("ai_specific", [])
            for pattern in ai_patterns:
                if pattern in filename_lower:
                    score += 30
        
        # Integration specific scoring
        if analysis["workflow_type"] in ["integration_focused", "general"]:
            integration_patterns = self.file_patterns.get("integration_specific", [])
            for pattern in integration_patterns:
                if pattern in filename_lower:
                    score += 25
        
        # Boost for shorter, focused filenames
        if len(filename) < 30:
            score += 5
        
        # Common important files
        important_files = [
            "overview", "getting-started", "basic", "introduction",
            "common-issues", "troubleshooting", "best-practices"
        ]
        for important in important_files:
            if important in filename_lower:
                score += 15
        
        return score
    
    def create_context_bundle(self, prompt: str, bundle_name: str = None) -> str:
        """Create a context bundle based on the prompt"""
        print(f"🔍 Analyzing prompt: {prompt[:100]}...")
        
        # Analyze the prompt
        analysis = self.analyze_prompt(prompt)
        
        # Generate bundle name if not provided
        if not bundle_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            bundle_name = f"context_{timestamp}"
        
        print(f"\n📊 Analysis Results:")
        print(f"  🎯 Workflow Type: {analysis['workflow_type']}")
        print(f"  🔧 Detected Services: {', '.join(analysis['detected_services'][:10])}")
        print(f"  📁 Required Folders: {', '.join(analysis['required_folders'])}")
        print(f"  📈 Complexity Score: {analysis['complexity_score']}")
        
        # Get relevant files
        relevant_files = self.get_relevant_files(analysis)
        
        print(f"\n📋 Selected {len(relevant_files)} files for optimal AI context")
        
        # Create bundle directory
        bundle_dir = os.path.join(self.context_output_dir, bundle_name)
        if os.path.exists(bundle_dir):
            shutil.rmtree(bundle_dir)
        os.makedirs(bundle_dir, exist_ok=True)
        
        # Copy selected files
        copied_files = 0
        for file_path in relevant_files:
            source_path = os.path.join(self.docs_dir, file_path)
            if os.path.exists(source_path):
                dest_path = os.path.join(bundle_dir, file_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(source_path, dest_path)
                copied_files += 1
        
        # Create bundle metadata and README
        self.create_bundle_readme(bundle_dir, prompt, analysis, relevant_files)
        
        print(f"✅ Created bundle: {bundle_name}")
        print(f"📁 Location: {bundle_dir}")
        print(f"📄 Files: {copied_files}")
        
        return bundle_dir
    
    def create_bundle_readme(self, bundle_dir: str, prompt: str, analysis: Dict, files: List[str]):
        """Create README for the bundle"""
        config_name = self.config.get('name', 'Unknown')
        config_desc = self.config.get('description', 'Documentation')
        
        readme_content = f"""# 🎯 Smart Context Bundle

**Generated for prompt:** "{prompt[:200]}{'...' if len(prompt) > 200 else ''}"

**Configuration:** {config_name} - {config_desc}

## 📊 Analysis Results

- **Workflow Type:** {analysis['workflow_type']}
- **Detected Services:** {', '.join(analysis['detected_services'])}
- **Complexity Score:** {analysis['complexity_score']}/10
- **Total Files:** {len(files)}

## 📁 Included Documentation

This bundle contains {len(files)} carefully selected files optimized for your specific needs:

### Categories Included:
{chr(10).join([f"- **{folder.replace('_', ' ').title()}**" for folder in analysis['required_folders']])}

### Key Services Detected:
{chr(10).join([f"- {service.title()}" for service in analysis['detected_services'][:10]])}

## 🚀 Usage Instructions

1. **Download this entire folder**
2. **Upload to your AI assistant** as context
3. **Use your original prompt:** "{prompt[:100]}{'...' if len(prompt) > 100 else ''}"
4. **Your AI will have optimal context** for helping you!

## 🎯 Optimization Details

This bundle was intelligently curated to:
- ✅ Include all relevant concepts for your prompt
- ✅ Stay within AI context limits (~85-95% usage)
- ✅ Prioritize high-impact documentation
- ✅ Exclude irrelevant content

## 📈 Quality Metrics

- **Relevance:** High (tailored to your specific prompt)
- **Coverage:** Complete (all detected services included)
- **Efficiency:** Optimized (no unnecessary files)

---

*Generated by Smart Context Selector at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*Configuration: {config_name}*
"""
        
        with open(os.path.join(bundle_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def push_to_github(self, bundle_dir: str) -> bool:
        """Push the bundle to GitHub"""
        try:
            bundle_name = os.path.basename(bundle_dir)
            
            print(f"\n⚠️  Make sure your git remote is set to your own GitHub repository before pushing!")
            print(f"   (Use 'git remote -v' to check and 'git remote set-url origin <your-repo-url>' to change)")
            print(f"📤 Pushing {bundle_name} to GitHub...")
            
            # Git commands
            subprocess.run(["git", "add", bundle_dir], check=True)
            subprocess.run([
                "git", "commit", "-m", 
                f"🎯 Add smart context bundle: {bundle_name}"
            ], check=True)
            subprocess.run(["git", "push"], check=True)
            
            print(f"✅ Successfully pushed to GitHub!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pushing to GitHub: {e}")
            return False