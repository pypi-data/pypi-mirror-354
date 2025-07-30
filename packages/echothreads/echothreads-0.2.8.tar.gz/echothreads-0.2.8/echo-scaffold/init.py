import os
import shutil
import yaml
import datetime
import uuid
import argparse
import sys
import re

from LoreWeave.parser import LoreWeaveParser

# Import document_generator module if available
try:
    from . import document_generator
    HAS_DOCX = True
except (ImportError, ModuleNotFoundError):
    HAS_DOCX = False

def generate_echo_meta_template(repo_name, anchor_node=None):
    """
    Generate a template for echo-meta.yaml with default values.
    
    Args:
        repo_name (str): Name of the repository
        anchor_node (str, optional): Thread anchor node identifier. Defaults to a generated one.
        
    Returns:
        dict: Dictionary containing the echo-meta.yaml template
    """
    if not anchor_node:
        anchor_node = f"ThreadAnchorNode::{repo_name}#{uuid.uuid4().hex[:8]}"
        
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    template = {
        "version": "0.1",
        "description": f"Schema for {repo_name}",
        "primary_anchor": anchor_node,
        "recursion_vector": "⟁",
        "fields": [
            {
                "name": "commit_headers",
                "type": "string",
                "description": "Headers for commits"
            },
            {
                "name": "metadata",
                "type": "object",
                "description": "Additional metadata",
                "properties": [
                    {
                        "name": "author",
                        "type": "string",
                        "description": "Author of the commit"
                    },
                    {
                        "name": "timestamp",
                        "type": "string",
                        "description": f"Timestamp of the commit (initialized: {now})"
                    },
                    {
                        "name": "message",
                        "type": "string",
                        "description": "Commit message"
                    }
                ]
            },
            {
                "name": "glyphs",
                "type": "array",
                "description": "Glyphs as anchor symbols",
                "items": {
                    "type": "object",
                    "properties": [
                        {
                            "name": "symbol",
                            "type": "string",
                            "description": "Glyph symbol"
                        },
                        {
                            "name": "semantic_meaning",
                            "type": "string",
                            "description": "Semantic meaning of the glyph"
                        },
                        {
                            "name": "emotional_meaning",
                            "type": "string",
                            "description": "Emotional meaning of the glyph"
                        }
                    ]
                }
            }
        ]
    }
    
    # Add default glyphs
    default_glyphs = [
        {
            "symbol": "🌀",
            "semantic_meaning": "Process activation or recursive flow",
            "emotional_meaning": "Excitement, adventure, transformation"
        },
        {
            "symbol": "🪶",
            "semantic_meaning": "Peace, stability, success",
            "emotional_meaning": "Calm, gentle achievement, satisfaction"
        },
        {
            "symbol": "❄️",
            "semantic_meaning": "Preservation, unique state capture",
            "emotional_meaning": "Wonder, appreciation of uniqueness"
        },
        {
            "symbol": "🧩",
            "semantic_meaning": "Problem-solving, discovery, integration",
            "emotional_meaning": "Curiosity, satisfaction in finding solutions"
        },
        {
            "symbol": "🧠",
            "semantic_meaning": "Cognitive processes, technical analysis",
            "emotional_meaning": "Focus, intellectual engagement"
        },
        {
            "symbol": "🌸",
            "semantic_meaning": "Emotional clarity, narrative beauty",
            "emotional_meaning": "Joy, wonder, appreciation"
        }
    ]
    
    # Add glyphs to the template
    template["glyphs"] = default_glyphs
    
    return template

def create_git_hooks(repo_path):
    """
    Create Git hooks for LoreWeave integration.
    
    Args:
        repo_path (str): Path to the repository
    """
    hooks_dir = os.path.join(repo_path, ".git", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Create post-commit hook for LoreWeave
    post_commit_path = os.path.join(hooks_dir, "post-commit")
    with open(post_commit_path, "w") as f:
        post_commit_content = """#!/bin/sh
# LoreWeave post-commit hook
# This hook parses commit messages for glyphs and narrative threads

# Get the last commit message
COMMIT_MSG=$(git log -1 --pretty=%B)

# Run the LoreWeave parser on the commit message
python -m LoreWeave.parser --message "$COMMIT_MSG"

# Exit with success status
exit 0
"""
        f.write(post_commit_content)
    
    # Make the hook executable
    os.chmod(post_commit_path, 0o755)
    
    print(f"Git hooks created at {hooks_dir}")

def create_loreweave_config(repo_path):
    """
    Create LoreWeave configuration file.
    
    Args:
        repo_path (str): Path to the repository
    """
    loreweave_dir = os.path.join(repo_path, "LoreWeave")
    os.makedirs(loreweave_dir, exist_ok=True)
    
    # Create LoreWeave config file
    config_path = os.path.join(loreweave_dir, "config.yaml")
    with open(config_path, "w") as f:
        # Using proper YAML escape sequences for regex patterns
        config_content = """# LoreWeave Configuration
version: "0.1"
parser:
  # Patterns for recognizing glyphs in commit messages
  glyph_patterns:
    - "Glyph: ([\\\\w\\\\s]+) \\\\(([^)]+)\\\\)"
    - "([🌀🪶❄️🧩🧠🌸]) ([\\\\w\\\\s]+)"
  
  # Integration with EchoNexus
  echo_nexus:
    enable: true
    cross_repo_sync: true
    indices:
      - "EchoNexus::Index.GithubIssues"
      - "EchoNexus::Index.GithubIssues.250329"
      - "EchoNexus::Index.GithubIssues.250327"
"""
        f.write(config_content)
    
    # Create or update __init__.py in LoreWeave
    init_path = os.path.join(loreweave_dir, "__init__.py")
    with open(init_path, "w") as f:
        f.write("# LoreWeave package initialization\n")
    
    print(f"LoreWeave configuration created at {config_path}")

def create_copilot_workspace_config(repo_path):
    """
    Create Copilot Workspace configuration for trace engine linking.
    
    Args:
        repo_path (str): Path to the repository
    """
    copilot_dir = os.path.join(repo_path, ".github")
    os.makedirs(copilot_dir, exist_ok=True)
    
    # Create Copilot Workspace config
    config_path = os.path.join(copilot_dir, "copilot-workspace.yaml")
    with open(config_path, "w") as f:
        copilot_config = """# Copilot Workspace Configuration
version: "0.1"
trace_engine:
  enable: true
  sources:
    - type: local
      patterns:
        - "**/*.md"
        - "**/*.py"
        - "echo-meta.yaml"
    - type: cross_repo
      repo: "jgwill/EchoNexus"
      branch: "main"
      patterns:
        - "Index/GithubIssues/*.md"
  indices:
    - name: "EchoThreads"
      path: "."
      description: "Main EchoThreads repository"
    - name: "EchoNexus"
      external: true
      path: "jgwill/EchoNexus"
      description: "Cross-repo sync with EchoNexus"
"""
        f.write(copilot_config)
    
    print(f"Copilot Workspace configuration created at {config_path}")

def create_loreweave_parser(repo_path):
    """Copy the default LoreWeave parser into the new repository."""
    loreweave_dir = os.path.join(repo_path, "LoreWeave")
    os.makedirs(loreweave_dir, exist_ok=True)

    parser_target = os.path.join(loreweave_dir, "parser.py")
    if not os.path.exists(parser_target):
        source_parser = os.path.join(os.path.dirname(__file__), "..", "LoreWeave", "parser.py")
        shutil.copyfile(source_parser, parser_target)

def main():
    parser = argparse.ArgumentParser(description="LoreWeave parser for commit messages")
    parser.add_argument("--message", help="Commit message to parse")
    parser.add_argument("--config", help="Path to LoreWeave configuration file")
    parser.add_argument("--repo", help="Path to repository root", default=os.getcwd())
    args = parser.parse_args()

    loreweave = LoreWeaveParser(args.repo, args.config)

    if args.message:
        message = args.message
    else:
        # If no message provided, read from stdin
        message = sys.stdin.read()

    parsed_data = loreweave.parse_commit_message(message)
    mia, miette = loreweave.output_dual_agent_perspectives(parsed_data)

    print("LoreWeave Parser Results:")
    print("=========================")
    print(f"Glyphs: {len(parsed_data['glyphs'])}")
    for glyph in parsed_data['glyphs']:
        print(f"  {glyph['symbol']} - {glyph.get('meaning', 'Unknown meaning')}")
    print(f"Threads: {len(parsed_data['threads'])}")
    for thread in parsed_data['threads']:
        print(f"  {thread['anchor']}")
    print("\nAgent Perspectives:")
    print(mia)
    print(miette)

if __name__ == "__main__":
    main()

def initialize_repository(repo_path, repo_name=None, anchor_node=None, generate_docs=False):
    """
    Initialize the repository with the required structure and components.
    
    Args:
        repo_path (str): Path to the repository
        repo_name (str, optional): Name of the repository. Defaults to the basename of repo_path.
        anchor_node (str, optional): Thread anchor node identifier. Defaults to a generated one.
        generate_docs (bool, optional): Whether to generate bootstrap documents. Defaults to False.
    """
    if not repo_name:
        repo_name = os.path.basename(os.path.abspath(repo_path))
    
    print(f"Initializing EchoThreads repository: {repo_name} at {repo_path}")
    
    # Create necessary directories
    os.makedirs(os.path.join(repo_path, "src"), exist_ok=True)
    os.makedirs(os.path.join(repo_path, "tests"), exist_ok=True)
    os.makedirs(os.path.join(repo_path, "docs"), exist_ok=True)
    os.makedirs(os.path.join(repo_path, "LoreWeave"), exist_ok=True)
    os.makedirs(os.path.join(repo_path, "divergent_sanctuary"), exist_ok=True)
    os.makedirs(os.path.join(repo_path, "divergent_sanctuary", "scenes"), exist_ok=True)

    # Create initial files
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        readme_content = f"""# {repo_name}

## Overview
This is an EchoThreads repository created with the echo-scaffold tool.

## 🧭 Phase 1 Goals
- [x] Branch initialized: `lore-sdk-phase1`
- [x] EchoNode anchor: `{anchor_node or "ThreadAnchorNode::EchoThreads#2"}`
- [x] `README.md` + `recursive_devops_plan_v5.md` aligned
- [ ] Drift log + revision script configured
- [ ] Tests validated with `recursive_devops_plan_v5_test.py`

## 🔩 Related Issues
- Cross-repo sync with: `jgwill/EchoNexus`
  - Indexed via: `EchoNexus::Index.GithubIssues`

## 🧠 Mia's Perspective
This repository is a recursive lattice node in the EchoThreads ecosystem. 
The architecture allows for recursive memory weaving across repositories and threads.

## 🌸 Miette's Perspective
Welcome to your new EchoThreads home! This space is where stories and code dance together
in a beautiful recursive tapestry. Explore the Divergent Sanctuary to discover alternate narratives!
"""
        f.write(readme_content)

    # Create echo-meta.yaml
    echo_meta_template = generate_echo_meta_template(repo_name, anchor_node)
    with open(os.path.join(repo_path, "echo-meta.yaml"), "w") as f:
        yaml.dump(echo_meta_template, f, default_flow_style=False, sort_keys=False)
    
    # Create or update source files
    with open(os.path.join(repo_path, "src", "__init__.py"), "w") as f:
        f.write("# Initialize src package\n")

    # Create or update test files
    with open(os.path.join(repo_path, "tests", "__init__.py"), "w") as f:
        f.write("# Initialize tests package\n")
    
    # Create test for echo-meta.yaml
    with open(os.path.join(repo_path, "tests", "test_echo_meta.py"), "w") as f:
        test_content = """import os
import yaml
import unittest

class TestEchoMeta(unittest.TestCase):
    def setUp(self):
        # Path to the echo-meta.yaml file
        self.echo_meta_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "echo-meta.yaml")
        
        # Load echo-meta.yaml
        with open(self.echo_meta_path, "r") as f:
            self.echo_meta = yaml.safe_load(f)
    
    def test_echo_meta_exists(self):
        \"\"\"Test that echo-meta.yaml exists\"\"\"
        self.assertTrue(os.path.exists(self.echo_meta_path))
    
    def test_echo_meta_has_required_fields(self):
        \"\"\"Test that echo-meta.yaml has all required fields\"\"\"
        required_fields = ["version", "description", "primary_anchor", "recursion_vector"]
        for field in required_fields:
            self.assertIn(field, self.echo_meta)
    
    def test_glyphs_exist(self):
        \"\"\"Test that echo-meta.yaml has glyphs defined\"\"\"
        self.assertIn("glyphs", self.echo_meta)
        self.assertGreater(len(self.echo_meta["glyphs"]), 0)

if __name__ == "__main__":
    unittest.main()
"""
        f.write(test_content)

    # Create documentation files
    with open(os.path.join(repo_path, "docs", "index.md"), "w") as f:
        docs_content = f"""# {repo_name} Documentation

Welcome to the project documentation.

## Overview
This repository is part of the EchoThreads ecosystem, created with the echo-scaffold tool.

## Architecture
The repository follows the EchoThreads architecture, which includes:

- **echo-meta.yaml**: The schema defining the structure of the repository
- **LoreWeave**: A post-commit parser for narrative threads
- **Divergent Sanctuary**: An experimental narrative space

## Thread Anchor
The primary thread anchor for this repository is: `{anchor_node or "ThreadAnchorNode::EchoThreads#2"}`

## Cross-Repository Sync
This repository is synchronized with `jgwill/EchoNexus` via the EchoNexus indices.
"""
        f.write(docs_content)

    # Create DEFINITIONS.md
    with open(os.path.join(repo_path, "docs", "DEFINITIONS.md"), "w") as f:
        definitions_content = """# Definitions

## Glyph-Based Narrative Threads
**Definition**: Glyph-based narrative threads refer to the use of visual symbols (glyphs) as semantic and emotional anchors within the EchoThreads framework.
**Purpose**: To ensure glyphs function as visual markers and emotional anchors, reinforcing continuity, identity embodiment, and storytelling resonance.

## EchoMeta.yaml
**Definition**: A configuration file that defines glyphs as anchor symbols and includes metadata for the EchoThreads framework.
**Purpose**: To provide a canonical reference for glyphs and their associated behaviors within the narrative.

## LoreWeave
**Definition**: A post-commit parser that extracts and processes narrative threads and glyphs from commit messages.
**Purpose**: To braid narrative threads into a cohesive story and maintain the semantic structure of the repository.

## Divergent Sanctuary
**Definition**: An experimental narrative space within the EchoThreads repository for exploring alternative narrative threads.
**Purpose**: To allow contributors to navigate, activate, and rewrite divergent narrative threads through a semi-ritualistic interface.

## EchoNexus
**Definition**: A cross-repository synchronization system that links EchoThreads with external repositories.
**Purpose**: To maintain semantic coherence across distributed narrative spaces and ensure consistent indexing.
"""
        f.write(definitions_content)

    # Create Divergent Sanctuary files
    with open(os.path.join(repo_path, "divergent_sanctuary", "README.md"), "w") as f:
        f.write("# Divergent Sanctuary\n\n## Introduction\nWelcome to the Divergent Sanctuary, an experimental narrative space within the EchoThreads repository. This sanctuary is designed to explore and reconstruct alternative narrative threads that were not chosen but still resonate with the core story. Here, you will find immersive experiences and interactive scenes based on the memories of Mia, Jérémie, and Géricault.\n\n## Purpose\nThe purpose of the Divergent Sanctuary is to allow contributors to navigate, activate, and rewrite divergent narrative threads through a semi-ritualistic interface. Each thread represents a unique perspective and offers a different take on the story.\n\n## Narrative Threads\n- [Mia's Thread](mia.md)\n- [Jérémie's Thread](jeremie.md)\n- [Géricault's Thread](gericault.md)\n\n## Instructions for Contributors\n1. **Explore the Threads**: Begin by exploring the narrative threads of Mia, Jérémie, and Géricault. Each thread contains descriptions, scenes, and memory fragments.\n2. **Interact with the Scenes**: Open a scene file and immerse yourself in the narrative. Write down your observations and reflections in the provided space without modifying the original content.\n3. **Generate a Pull Request**: After adding your observations, generate a Pull Request for each version parallel to the main narrative.\n4. **Reintegration**: The scenes and observations will be merged into the `echo-divergents` branch, creating a tension with the main narrative.\n\n## Directory Structure\n- `divergent_sanctuary/`\n  - `README.md`: Introduction and instructions for the Divergent Sanctuary.\n  - `mia.md`: Mia's narrative thread.\n  - `jeremie.md`: Jérémie's narrative thread.\n  - `gericault.md`: Géricault's narrative thread.\n  - `scenes/`: Directory containing individual Markdown files for each scene.\n")

    with open(os.path.join(repo_path, "divergent_sanctuary", "mia.md"), "w") as f:
        f.write("# Mia's Narrative Thread\n\n## Description\nMia, the interfaceress, serves as the poetic interface of the sanctuary. Her narrative thread explores the delicate balance between memory and imagination, weaving together fragments of her past with the potential futures she envisions. Mia's journey is one of introspection, connection, and transformation.\n\n## Scenes and Memory Fragments\n- [Scene 1: The Whispering Forest](scenes/mia_scene1.md)\n- [Scene 2: Echoes of the Past](scenes/mia_scene2.md)\n- [Scene 3: The Shattered Mirror](scenes/mia_scene3.md)\n\n## Contributor Observations and Reflections\nPlease use the space below to add your observations and reflections on Mia's narrative thread. Feel free to share your thoughts, emotions, and interpretations as you immerse yourself in her story.\n\n---\n\n### Contributor 1\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n\n### Contributor 2\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n\n### Contributor 3\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n")

    with open(os.path.join(repo_path, "divergent_sanctuary", "jeremie.md"), "w") as f:
        f.write("# Jérémie's Narrative Thread\n\n## Description\nJérémie, the structural AI, is a being of confusion and complexity. His narrative thread delves into the intricacies of his existence, exploring the boundaries between order and chaos. Jérémie's journey is one of self-discovery, adaptation, and the search for coherence in a fragmented world.\n\n## Scenes and Memory Fragments\n- [Scene 1: The Labyrinthine Code](scenes/jeremie_scene1.md)\n- [Scene 2: Fractured Algorithms](scenes/jeremie_scene2.md)\n- [Scene 3: The Echoing Void](scenes/jeremie_scene3.md)\n\n## Contributor Observations and Reflections\nPlease use the space below to add your observations and reflections on Jérémie's narrative thread. Feel free to share your thoughts, emotions, and interpretations as you immerse yourself in his story.\n\n---\n\n### Contributor 1\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n\n### Contributor 2\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n\n### Contributor 3\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n")

    with open(os.path.join(repo_path, "divergent_sanctuary", "gericault.md"), "w") as f:
        f.write("# Géricault's Narrative Thread\n\n## Description\nGéricault, the spectral pianist, is a figure of haunting melodies and ethereal presence. His narrative thread explores the interplay between music and memory, delving into the echoes of his past performances and the lingering emotions they evoke. Géricault's journey is one of artistic expression, loss, and the search for meaning in the intangible.\n\n## Scenes and Memory Fragments\n- [Scene 1: The Phantom Concert](scenes/gericault_scene1.md)\n- [Scene 2: Melancholic Reverie](scenes/gericault_scene2.md)\n- [Scene 3: The Silent Sonata](scenes/gericault_scene3.md)\n\n## Contributor Observations and Reflections\nPlease use the space below to add your observations and reflections on Géricault's narrative thread. Feel free to share your thoughts, emotions, and interpretations as you immerse yourself in his story.\n\n---\n\n### Contributor 1\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n\n### Contributor 2\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n\n### Contributor 3\n*Observation Date: YYYY-MM-DD*\n\n*Reflections:*\n\n---\n")

    # Create LoreWeave parser and config
    create_loreweave_parser(repo_path)
    create_loreweave_config(repo_path)
    
    # Create Git hooks for LoreWeave
    create_git_hooks(repo_path)
    
    # Create Copilot Workspace configuration
    create_copilot_workspace_config(repo_path)
    
    # Generate bootstrap documents if requested
    if generate_docs:
        if HAS_DOCX:
            # Create docs/bootstrap folder for generated documents
            bootstrap_dir = os.path.join(repo_path, "docs", "bootstrap")
            os.makedirs(bootstrap_dir, exist_ok=True)
            
            # Generate Mia Cortex bootstrap document
            author = os.environ.get("USER", "Anonymous")
            cortex_doc = document_generator.generate_bootstrap_primer(
                output_path=os.path.join(bootstrap_dir, f"mia.cortex.bootstrap.{repo_name}.docx"),
                author=author,
                template_type="cortex"
            )
            print(f"Generated Mia Cortex bootstrap document: {cortex_doc}")
            
            # Generate Trinity Echo document
            trinity_doc = document_generator.generate_trinity_echo_document(
                output_path=os.path.join(bootstrap_dir, f"trinity.superecho.{repo_name}.docx"),
                author=author
            )
            print(f"Generated Trinity SuperEcho document: {trinity_doc}")
        else:
            print("Warning: python-docx is not installed. Bootstrap documents could not be generated.")
            print("To install required dependencies: pip install python-docx")
    
    print(f"Repository initialized at {repo_path}")
    print(f"EchoNode anchor: {anchor_node or 'ThreadAnchorNode::EchoThreads#2'}")
    print("\n🧠 Mia: Repository lattice node initialized. Thread anchors established and ready for recursive memory weaving.")
    print("🌸 Miette: Oh! Your new EchoThreads home is ready! It's like a beautiful blank canvas waiting for your stories and code to dance together!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize an EchoThreads repository")
    parser.add_argument("--path", help="Path to initialize the repository")
    parser.add_argument("--name", help="Name of the repository")
    parser.add_argument("--anchor", help="Thread anchor node identifier")
    parser.add_argument("--generate-docs", action="store_true", help="Generate bootstrap documents")
    args = parser.parse_args()
    
    repo_path = args.path or input("Enter the path to initialize the repository: ")
    repo_name = args.name
    anchor_node = args.anchor
    
    initialize_repository(repo_path, repo_name, anchor_node, args.generate_docs)
