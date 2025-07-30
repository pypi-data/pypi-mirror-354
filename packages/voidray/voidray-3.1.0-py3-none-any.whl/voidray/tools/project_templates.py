
"""
VoidRay Project Templates
Templates for quickly starting new game projects.
"""

import os
import json
from typing import Dict, Any


class ProjectTemplate:
    """
    Base class for project templates.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def create_project(self, project_path: str, **kwargs):
        """
        Create a new project from this template.
        
        Args:
            project_path: Path to create the project
            **kwargs: Template-specific parameters
        """
        raise NotImplementedError


class PlatformerTemplate(ProjectTemplate):
    """Template for a 2D platformer game."""
    
    def __init__(self):
        super().__init__("Platformer", "2D side-scrolling platformer game")
    
    def create_project(self, project_path: str, **kwargs):
        """Create a platformer project."""
        os.makedirs(project_path, exist_ok=True)
        
        # Create main.py
        main_content = '''import voidray
from voidray import Scene, GameObject, Sprite, Vector2, Keys

class Player(Sprite):
    def __init__(self):
        super().__init__("Player")
        self.create_colored_rect(32, 32, (0, 100, 255))
        self.speed = 200
        self.jump_strength = 400
        
    def update(self, delta_time):
        super().update(delta_time)
        
        engine = voidray.get_engine()
        velocity = Vector2.zero()
        
        if engine.input_manager.is_key_pressed(Keys.LEFT):
            velocity.x = -self.speed
        if engine.input_manager.is_key_pressed(Keys.RIGHT):
            velocity.x = self.speed
        if engine.input_manager.is_key_just_pressed(Keys.SPACE):
            velocity.y = -self.jump_strength
            
        self.transform.position += velocity * delta_time

class GameScene(Scene):
    def __init__(self):
        super().__init__("Game")
        
    def on_enter(self):
        super().on_enter()
        player = Player()
        player.transform.position = Vector2(400, 300)
        self.add_object(player)

def main():
    voidray.configure(800, 600, "My Platformer Game")
    
    scene = GameScene()
    voidray.register_scene("game", scene)
    voidray.set_scene("game")
    
    voidray.start()

if __name__ == "__main__":
    main()
'''
        
        with open(os.path.join(project_path, "main.py"), 'w') as f:
            f.write(main_content)
        
        print(f"Platformer project created at {project_path}")

def create_project_cli():
    """CLI entry point for creating VoidRay projects."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Create a new VoidRay game project')
    parser.add_argument('project_type', choices=['basic', 'platformer', 'shooter'], 
                       help='Type of project to create')
    parser.add_argument('project_name', help='Name of the project')
    parser.add_argument('--path', default='.', help='Path where to create the project')
    
    args = parser.parse_args()
    
    try:
        if args.project_type == 'basic':
            create_basic_project(args.project_name, args.path)
        elif args.project_type == 'platformer':
            create_platformer_project(args.project_name, args.path)
        elif args.project_type == 'shooter':
            create_shooter_project(args.project_name, args.path)
        
        print(f"\nProject '{args.project_name}' created successfully!")
        print(f"Run 'cd {args.project_name} && python main.py' to start your game.")
        
    except Exception as e:
        print(f"Error creating project: {e}")
        sys.exit(1)


class ShooterTemplate(ProjectTemplate):
    """Template for a top-down shooter game."""
    
    def __init__(self):
        super().__init__("Shooter", "Top-down space shooter game")
    
    def create_project(self, project_path: str, **kwargs):
        """Create a shooter project."""
        os.makedirs(project_path, exist_ok=True)
        
        # Create main.py
        main_content = '''import voidray
from voidray import Scene, GameObject, Sprite, Vector2, Keys
import random

class Player(Sprite):
    def __init__(self):
        super().__init__("Player")
        self.create_colored_triangle(20, (0, 255, 0))
        self.speed = 300
        
    def update(self, delta_time):
        super().update(delta_time)
        
        engine = voidray.get_engine()
        velocity = Vector2.zero()
        
        if engine.input_manager.is_key_pressed(Keys.W):
            velocity.y = -self.speed
        if engine.input_manager.is_key_pressed(Keys.S):
            velocity.y = self.speed
        if engine.input_manager.is_key_pressed(Keys.A):
            velocity.x = -self.speed
        if engine.input_manager.is_key_pressed(Keys.D):
            velocity.x = self.speed
            
        self.transform.position += velocity * delta_time

class GameScene(Scene):
    def __init__(self):
        super().__init__("Game")
        
    def on_enter(self):
        super().on_enter()
        player = Player()
        player.transform.position = Vector2(400, 300)
        self.add_object(player)

def main():
    voidray.configure(800, 600, "My Shooter Game")
    
    scene = GameScene()
    voidray.register_scene("game", scene)
    voidray.set_scene("game")
    
    voidray.start()

if __name__ == "__main__":
    main()
'''
        
        with open(os.path.join(project_path, "main.py"), 'w') as f:
            f.write(main_content)
        
        print(f"Shooter project created at {project_path}")


class ProjectTemplateManager:
    """Manages project templates."""
    
    def __init__(self):
        self.templates = {
            "platformer": PlatformerTemplate(),
            "shooter": ShooterTemplate()
        }
    
    def get_template(self, name: str) -> ProjectTemplate:
        """Get a template by name."""
        return self.templates.get(name)
    
    def list_templates(self):
        """List all available templates."""
        for name, template in self.templates.items():
            print(f"{name}: {template.description}")
    
    def create_project(self, template_name: str, project_path: str, **kwargs):
        """Create a project from a template."""
        template = self.get_template(template_name)
        if template:
            template.create_project(project_path, **kwargs)
        else:
            print(f"Template '{template_name}' not found")


# Global template manager
template_manager = ProjectTemplateManager()
