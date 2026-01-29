#!/usr/bin/env python3
"""
Example script demonstrating how to load and use agent model configuration.

This shows how you could build tooling around the .agent-models.json config
to ensure consistent model usage across your development workflow.
"""

import json
from pathlib import Path
from typing import Dict, Any


class AgentModelConfig:
    """Load and access agent model configuration."""
    
    def __init__(self, config_path: str = ".agent-models.json"):
        """
        Initialize configuration from JSON file.
        
        Args:
            config_path: Path to the .agent-models.json file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        with open(self.config_path) as f:
            return json.load(f)
    
    def get_model(self, agent_name: str) -> str:
        """
        Get the model for a specific agent.
        
        Args:
            agent_name: Name of the agent (e.g., 'implementation', 'critic_primary')
            
        Returns:
            Model identifier (e.g., 'claude-sonnet-4.5')
            
        Raises:
            KeyError: If agent name not found in configuration
        """
        return self.config['agents'][agent_name]['model']
    
    def get_agent_info(self, agent_name: str) -> Dict[str, str]:
        """
        Get full information about an agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Dictionary with name, model, provider, and rationale
        """
        return self.config['agents'][agent_name]
    
    def list_agents(self) -> list[str]:
        """List all configured agents."""
        return list(self.config['agents'].keys())
    
    def print_summary(self):
        """Print a summary of all agent configurations."""
        print("Agent Model Configuration")
        print("=" * 80)
        print(f"Version: {self.config['version']}")
        print(f"Project: {self.config['metadata']['project']}")
        print(f"Last Updated: {self.config['metadata']['last_updated']}")
        print("\nAgents:")
        print("-" * 80)
        
        for agent_name in self.list_agents():
            info = self.get_agent_info(agent_name)
            print(f"\n{info['name']}")
            print(f"  Model: {info['model']}")
            print(f"  Provider: {info['provider']}")
            print(f"  Rationale: {info['rationale']}")


def main():
    """Demonstrate configuration usage."""
    # Load configuration
    config = AgentModelConfig()
    
    # Print summary
    config.print_summary()
    
    print("\n" + "=" * 80)
    print("\nExample Usage:")
    print("-" * 80)
    
    # Get specific models
    impl_model = config.get_model('implementation')
    print(f"\nImplementation Agent uses: {impl_model}")
    
    critic_model = config.get_model('critic_secondary')
    print(f"Secondary Critic uses: {critic_model}")
    
    # Show how you might use this in code
    print("\n" + "-" * 80)
    print("\nExample Code:")
    print("""
# In your automation scripts:
from agent_config import AgentModelConfig

config = AgentModelConfig()

# When invoking implementation agent
task(
    agent_type="general-purpose",
    model=config.get_model('implementation'),
    description="Implement feature",
    prompt="..."
)

# When invoking secondary critic
task(
    agent_type="general-purpose",
    model=config.get_model('critic_secondary'),
    description="Review code",
    prompt="..."
)
""")


if __name__ == "__main__":
    main()
