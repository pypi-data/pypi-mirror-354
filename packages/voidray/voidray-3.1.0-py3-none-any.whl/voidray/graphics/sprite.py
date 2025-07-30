"""
VoidRay Sprite System
Handles sprite loading, animation, and rendering.
"""

import pygame
from typing import Optional, List
from ..core.game_object import GameObject
from ..math.vector2 import Vector2


class Sprite(GameObject):
    """
    A Sprite is a GameObject that can render an image.
    """

    def __init__(self, name: str = "Sprite", image_path: Optional[str] = None):
        """
        Initialize a new Sprite.

        Args:
            name: Name identifier for this sprite
            image_path: Path to the image file to load
        """
        super().__init__(name)

        self.surface: Optional[pygame.Surface] = None
        self.original_surface: Optional[pygame.Surface] = None
        self.color = (255, 255, 255)  # White tint by default
        self.alpha = 255  # Full opacity
        self.visible = True

        if image_path:
            self.load_image(image_path)

    def load_image(self, image_path: str):
        """
        Load an image from file.

        Args:
            image_path: Path to the image file
        """
        try:
            self.original_surface = pygame.image.load(image_path).convert_alpha()
            self.surface = self.original_surface.copy()
            print(f"Loaded sprite image: {image_path}")
        except pygame.error as e:
            print(f"Error loading sprite image {image_path}: {e}")
            # Create a placeholder colored rectangle
            self.original_surface = pygame.Surface((32, 32))
            self.original_surface.fill((255, 0, 255))  # Magenta placeholder
            self.surface = self.original_surface.copy()

    def create_colored_rect(self, width: int, height: int, color: tuple):
        """
        Create a simple colored rectangle as the sprite.

        Args:
            width: Rectangle width
            height: Rectangle height
            color: RGB color tuple
        """
        self.original_surface = pygame.Surface((width, height))
        self.original_surface.fill(color)
        self.surface = self.original_surface.copy()

    def create_colored_circle(self, radius: int, color: tuple):
        """
        Create a simple colored circle as the sprite.

        Args:
            radius: Circle radius
            color: RGB color tuple
        """
        size = radius * 2
        self.original_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.original_surface, color, (radius, radius), radius)
        self.surface = self.original_surface.copy()

    def set_color(self, color: tuple):
        """
        Set the color tint for this sprite.

        Args:
            color: RGB color tuple
        """
        self.color = color
        self._update_surface()

    def set_alpha(self, alpha: int):
        """
        Set the alpha transparency for this sprite.

        Args:
            alpha: Alpha value (0-255)
        """
        self.alpha = max(0, min(255, alpha))
        self._update_surface()

    def _update_surface(self):
        """
        Update the surface with current color and alpha settings.
        """
        if self.original_surface:
            self.surface = self.original_surface.copy()

            # Apply color tint
            if self.color != (255, 255, 255):
                color_surface = pygame.Surface(self.surface.get_size())
                color_surface.fill(self.color)
                self.surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_MULT)

            # Apply alpha
            if self.alpha < 255:
                self.surface.set_alpha(self.alpha)

    def get_size(self) -> Vector2:
        """
        Get the size of the sprite.

        Returns:
            Size as Vector2
        """
        if self.surface:
            return Vector2(self.surface.get_width(), self.surface.get_height())
        return Vector2(0, 0)

    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the sprite.

        Returns:
            pygame.Rect representing the sprite bounds
        """
        if self.surface:
            world_pos = self.get_world_position()
            size = self.get_size()
            world_scale = self.get_world_scale()

            scaled_width = size.x * world_scale.x
            scaled_height = size.y * world_scale.y

            return pygame.Rect(
                world_pos.x - scaled_width / 2,
                world_pos.y - scaled_height / 2,
                scaled_width,
                scaled_height
            )
        return pygame.Rect(0, 0, 0, 0)

    def render(self, renderer):
        """
        Render this sprite.

        Args:
            renderer: The renderer to draw with
        """
        if not self.active or not self.visible or not self.surface:
            return

        # Render this sprite
        world_pos = self.get_world_position()
        world_rotation = self.get_world_rotation()
        world_scale = self.get_world_scale()

        renderer.draw_sprite(self.surface, world_pos, world_rotation, world_scale)

        # Render children
        super().render(renderer)

    def add_component(self, component):
        """
        Add a component to this sprite.

        Args:
            component: Component to add
        """
        super().add_component(component)

        # Special handling for colliders
        if hasattr(component, 'get_world_position') and hasattr(component, 'check_collision'):
            # This is likely a collider, register it with physics system
            try:
                import voidray
                engine = voidray.get_engine()
                if hasattr(engine, 'physics_engine') and engine.physics_engine:
                    engine.physics_engine.add_collider(component)
                if hasattr(engine, 'physics_system') and engine.physics_system:
                    engine.physics_system.add_collider(component)
            except:
                pass  # Ignore if engine not available yet


class AnimatedSprite(Sprite):
    """
    An AnimatedSprite can play frame-based animations.
    """

    def __init__(self, name: str = "AnimatedSprite"):
        """
        Initialize a new AnimatedSprite.

        Args:
            name: Name identifier for this sprite
        """
        super().__init__(name)

        self.frames: List[pygame.Surface] = []
        self.current_frame = 0
        self.frame_time = 0.1  # Time per frame in seconds
        self.elapsed_time = 0.0
        self.playing = False
        self.loop = True

    def add_frame(self, image_path: str):
        """
        Add a frame to the animation.

        Args:
            image_path: Path to the frame image
        """
        try:
            frame = pygame.image.load(image_path).convert_alpha()
            self.frames.append(frame)

            # Set the first frame as the current surface
            if len(self.frames) == 1:
                self.original_surface = frame
                self.surface = frame.copy()

        except pygame.error as e:
            print(f"Error loading animation frame {image_path}: {e}")

    def load_spritesheet(self, image_path: str, frame_width: int, frame_height: int, 
                        frame_count: int):
        """
        Load frames from a spritesheet.

        Args:
            image_path: Path to the spritesheet image
            frame_width: Width of each frame
            frame_height: Height of each frame
            frame_count: Number of frames to extract
        """
        try:
            spritesheet = pygame.image.load(image_path).convert_alpha()

            frames_per_row = spritesheet.get_width() // frame_width

            for i in range(frame_count):
                row = i // frames_per_row
                col = i % frames_per_row

                x = col * frame_width
                y = row * frame_height

                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(spritesheet, (0, 0), (x, y, frame_width, frame_height))
                self.frames.append(frame)

            # Set the first frame as current
            if self.frames:
                self.original_surface = self.frames[0]
                self.surface = self.frames[0].copy()

        except pygame.error as e:
            print(f"Error loading spritesheet {image_path}: {e}")

    def play_animation(self, loop: bool = True):
        """
        Start playing the animation.

        Args:
            loop: Whether to loop the animation
        """
        self.playing = True
        self.loop = loop
        self.current_frame = 0
        self.elapsed_time = 0.0

    def stop_animation(self):
        """
        Stop playing the animation.
        """
        self.playing = False

    def set_frame_time(self, frame_time: float):
        """
        Set the time per frame.

        Args:
            frame_time: Time per frame in seconds
        """
        self.frame_time = frame_time

    def update(self, delta_time: float):
        """
        Update the animation.

        Args:
            delta_time: Time elapsed since last frame
        """
        super().update(delta_time)

        if self.playing and self.frames:
            self.elapsed_time += delta_time

            if self.elapsed_time >= self.frame_time:
                self.elapsed_time = 0.0
                self.current_frame += 1

                if self.current_frame >= len(self.frames):
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.current_frame = len(self.frames) - 1
                        self.playing = False

                # Update the current surface
                if 0 <= self.current_frame < len(self.frames):
                    self.original_surface = self.frames[self.current_frame]
                    self._update_surface()