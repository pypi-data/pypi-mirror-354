"""
VoidRay Enhanced Asset Loader
Advanced asset management system supporting streaming, caching, and multiple formats.
"""

import pygame
import json
import os
import threading
import pickle
import hashlib
from typing import Dict, Any, Optional, List, Tuple, Union
from pathlib import Path


class AssetCache:
    """LRU cache for loaded assets."""

    def __init__(self, max_size: int = 200):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []

    def get(self, key: str) -> Any:
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def put(self, key: str, value: Any):
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]

        self.cache[key] = value
        self.access_order.append(key)

    def clear(self):
        self.cache.clear()
        self.access_order.clear()


class AssetMetadata:
    """Metadata for loaded assets."""

    def __init__(self, asset_type: str, file_path: str, size: int, 
                 last_modified: float, checksum: str = ""):
        self.asset_type = asset_type
        self.file_path = file_path
        self.size = size
        self.last_modified = last_modified
        self.checksum = checksum
        self.load_count = 0
        self.last_accessed = 0


class AssetLoader:
    """
    Enhanced asset loader with streaming, caching, and performance optimizations.
    """

    def __init__(self, cache_size: int = 200, enable_streaming: bool = True):
        """
        Initialize the enhanced asset loader.

        Args:
            cache_size: Maximum number of assets to keep in memory
            enable_streaming: Whether to enable streaming for large assets
        """
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.data: Dict[str, Any] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.textures: Dict[str, pygame.Surface] = {}  # For 2.5D textures
        self.animations: Dict[str, List[pygame.Surface]] = {}

        # Enhanced features
        self.cache = AssetCache(cache_size)
        self.metadata: Dict[str, AssetMetadata] = {}
        self.enable_streaming = enable_streaming
        self.loading_threads: List[threading.Thread] = []
        self.async_callbacks: Dict[str, callable] = {}

        # Asset search paths with priority
        self.search_paths = {
            "image": ["assets/images/", "assets/textures/", "images/", "textures/", "./"],
            "sound": ["assets/sounds/", "assets/audio/", "sounds/", "audio/", "./"],
            "data": ["assets/data/", "data/", "config/", "./"],
            "font": ["assets/fonts/", "fonts/", "./"],
            "texture": ["assets/textures/", "assets/images/", "textures/", "./"],
            "animation": ["assets/animations/", "animations/", "./"]
        }

        # Supported file formats
        self.supported_formats = {
            "image": [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tga", ".webp"],
            "sound": [".wav", ".ogg", ".mp3", ".flac"],
            "data": [".json", ".xml", ".yaml", ".yml", ".txt"],
            "font": [".ttf", ".otf"],
            "texture": [".png", ".jpg", ".jpeg", ".bmp", ".tga"],
            "animation": [".gif", ".json"]  # JSON for sprite sheets
        }

        # Asset processing options
        self.default_image_convert = True
        self.default_alpha_convert = True
        self.texture_compression = False
        self.auto_generate_mipmaps = False

        print("Enhanced asset loader initialized")

    def add_search_path(self, asset_type: str, path: str, priority: int = 0):
        """
        Add a search path for specific asset type with priority.

        Args:
            asset_type: Type of asset
            path: Path to add
            priority: Priority (0 = highest priority)
        """
        if asset_type in self.search_paths:
            if priority == 0:
                self.search_paths[asset_type].insert(0, path)
            else:
                self.search_paths[asset_type].append(path)

    def _find_file(self, filename: str, asset_type: str) -> Optional[str]:
        """Find a file in search paths with format validation."""
        search_paths = self.search_paths.get(asset_type, ["./"])
        supported_exts = self.supported_formats.get(asset_type, [])

        # If filename already has extension, check if supported
        file_ext = Path(filename).suffix.lower()
        if file_ext and supported_exts and file_ext not in supported_exts:
            print(f"Warning: Unsupported format {file_ext} for {asset_type}")

        for path in search_paths:
            full_path = os.path.join(path, filename)
            if os.path.exists(full_path):
                return full_path

            # Try with different extensions if no extension provided
            if not file_ext and supported_exts:
                for ext in supported_exts:
                    test_path = full_path + ext
                    if os.path.exists(test_path):
                        return test_path

        return None

    def _get_file_metadata(self, file_path: str, asset_type: str) -> AssetMetadata:
        """Get or create metadata for a file."""
        if file_path in self.metadata:
            return self.metadata[file_path]

        try:
            stat = os.stat(file_path)
            size = stat.st_size
            last_modified = stat.st_mtime

            # Generate checksum for change detection
            checksum = ""
            if size < 1024 * 1024:  # Only for files < 1MB
                with open(file_path, 'rb') as f:
                    checksum = hashlib.md5(f.read()).hexdigest()

            metadata = AssetMetadata(asset_type, file_path, size, last_modified, checksum)
            self.metadata[file_path] = metadata
            return metadata

        except OSError:
            return AssetMetadata(asset_type, file_path, 0, 0)

    def load_image(self, name: str, filename: str, convert_alpha: bool = None,
                   scale: Tuple[int, int] = None, streaming: bool = False, 
                   fallback_color: tuple = (255, 0, 255), validate: bool = True) -> pygame.Surface:
        """
        Load an image with enhanced options.

        Args:
            name: Asset identifier
            filename: Image filename
            convert_alpha: Whether to convert with alpha (None for auto-detect)
            scale: Optional scaling (width, height)
            streaming: Whether to use streaming for large images
        """
        if name in self.images:
            return self.images[name]

        # Check cache first
        cached = self.cache.get(f"image_{name}")
        if cached:
            self.images[name] = cached
            return cached

        file_path = self._find_file(filename, "image")
        if not file_path:
            print(f"Image file not found: {filename}")
            return self._create_placeholder_image(name, (32, 32))

        metadata = self._get_file_metadata(file_path, "image")

        try:
            # Validate image file if requested
            if validate and not self._validate_image_file(file_path):
                print(f"Image validation failed: {filename}")
                return self._create_placeholder_image(name, scale or (32, 32))
            
            # Handle streaming for large images
            if streaming and metadata.size > 2 * 1024 * 1024:  # > 2MB
                print(f"Streaming large image: {filename}")
                # For streaming, we might load a lower resolution version first
                surface = pygame.image.load(file_path)
            else:
                surface = pygame.image.load(file_path)

            # Auto-detect alpha channel if not specified
            if convert_alpha is None:
                convert_alpha = filename.lower().endswith(('.png', '.gif')) or surface.get_masks()[3] != 0

            # Convert surface
            if convert_alpha:
                surface = surface.convert_alpha()
            else:
                surface = surface.convert()

            # Apply scaling if requested
            if scale:
                surface = pygame.transform.scale(surface, scale)

            # Store in cache and memory
            self.cache.put(f"image_{name}", surface)
            self.images[name] = surface
            metadata.load_count += 1

            print(f"Loaded image: {name} from {file_path} ({metadata.size} bytes)")
            return surface

        except pygame.error as e:
            print(f"Error loading image {file_path}: {e}")
            return self._create_placeholder_image(name, scale or (32, 32))

    def load_texture(self, name: str, filename: str, 
                    generate_mipmaps: bool = False, tile_size: Tuple[int, int] = None) -> pygame.Surface:
        """
        Load texture specifically for 2.5D rendering with enhanced options.

        Args:
            name: Texture identifier
            filename: Texture filename
            generate_mipmaps: Whether to generate mipmaps for distance rendering
            tile_size: Optional tile size for texture tiling
        """
        surface = self.load_image(name, filename, convert_alpha=True)

        # Process texture for 2.5D rendering
        processed_surface = self._process_texture_for_2_5d(surface, tile_size)

        # Store as texture with potential preprocessing for 2.5D
        if generate_mipmaps or self.auto_generate_mipmaps:
            # Generate mipmaps for better distance rendering
            mipmaps = self._generate_mipmaps(processed_surface)
            self.textures[name] = {"base": processed_surface, "mipmaps": mipmaps}
        else:
            self.textures[name] = processed_surface

        return processed_surface
    
    def _process_texture_for_2_5d(self, surface: pygame.Surface, tile_size: Tuple[int, int] = None) -> pygame.Surface:
        """Process texture for optimal 2.5D rendering."""
        # Ensure texture is power of 2 for better performance
        width, height = surface.get_size()
        
        if tile_size:
            # Resize to specific tile size
            new_width, new_height = tile_size
        else:
            # Find next power of 2
            new_width = 1
            while new_width < width:
                new_width *= 2
            new_height = 1
            while new_height < height:
                new_height *= 2
            
            # Don't upscale too much
            if new_width > width * 2:
                new_width = width
            if new_height > height * 2:
                new_height = height
        
        if (new_width, new_height) != (width, height):
            return pygame.transform.scale(surface, (new_width, new_height))
        
        return surface

    def _generate_mipmaps(self, surface: pygame.Surface) -> List[pygame.Surface]:
        """Generate mipmaps for a texture."""
        mipmaps = []
        current = surface

        while current.get_width() > 1 and current.get_height() > 1:
            new_width = max(1, current.get_width() // 2)
            new_height = max(1, current.get_height() // 2)
            current = pygame.transform.scale(current, (new_width, new_height))
            mipmaps.append(current)

        return mipmaps

    def load_animation(self, name: str, filename: str, 
                      frame_count: int = None, frame_duration: float = 0.1) -> List[pygame.Surface]:
        """
        Load animation frames from sprite sheet or GIF.

        Args:
            name: Animation identifier
            filename: Animation filename
            frame_count: Number of frames (for sprite sheets)
            frame_duration: Duration per frame in seconds
        """
        if name in self.animations:
            return self.animations[name]

        file_path = self._find_file(filename, "animation")
        if not file_path:
            print(f"Animation file not found: {filename}")
            return []

        try:
            frames = []

            if filename.lower().endswith('.gif'):
                # Load GIF frames (basic implementation)
                # In a full implementation, you'd use a library like Pillow
                surface = pygame.image.load(file_path)
                frames = [surface]  # Simplified - would extract frames

            elif filename.lower().endswith('.json'):
                # Load sprite sheet definition
                with open(file_path, 'r') as f:
                    sheet_data = json.load(f)

                sheet_image = self.load_image(f"{name}_sheet", sheet_data["image"])

                for frame_data in sheet_data["frames"]:
                    x, y, w, h = frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]
                    frame = sheet_image.subsurface((x, y, w, h))
                    frames.append(frame.copy())

            else:
                # Single image - treat as one frame
                frames = [self.load_image(f"{name}_frame", filename)]

            self.animations[name] = frames
            print(f"Loaded animation: {name} with {len(frames)} frames")
            return frames

        except Exception as e:
            print(f"Error loading animation {file_path}: {e}")
            return []

    def load_sound_async(self, name: str, filename: str, callback: callable = None):
        """
        Load sound asynchronously to avoid blocking.

        Args:
            name: Sound identifier
            filename: Sound filename
            callback: Function to call when loading completes
        """
        def load_worker():
            try:
                self.load_sound(name, filename)
                if callback:
                    callback(name, True)
            except Exception as e:
                print(f"Async sound loading failed for {name}: {e}")
                if callback:
                    callback(name, False)

        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()
        self.loading_threads.append(thread)

    def load_sound(self, name: str, filename: str, volume: float = 1.0) -> pygame.mixer.Sound:
        """
        Load sound with volume pre-setting.

        Args:
            name: Sound identifier
            filename: Sound filename
            volume: Default volume (0.0 to 1.0)
        """
        if name in self.sounds:
            return self.sounds[name]

        # Check if mixer is available
        try:
            pygame.mixer.get_init()
        except pygame.error:
            print(f"Audio not available, skipping sound: {filename}")
            return None

        file_path = self._find_file(filename, "sound")
        if not file_path:
            print(f"Sound file not found: {filename}")
            return None

        metadata = self._get_file_metadata(file_path, "sound")

        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(volume)

            # Cache large sounds differently
            if metadata.size > 5 * 1024 * 1024:  # > 5MB
                print(f"Large sound file detected: {filename} ({metadata.size} bytes)")

            self.sounds[name] = sound
            self.cache.put(f"sound_{name}", sound)
            metadata.load_count += 1

            print(f"Loaded sound: {name} from {file_path}")
            return sound

        except pygame.error as e:
            print(f"Error loading sound {file_path}: {e}")
            return None

    def load_data(self, name: str, filename: str, format_hint: str = None) -> Any:
        """
        Load data with format auto-detection.

        Args:
            name: Data identifier
            filename: Data filename
            format_hint: Format hint ("json", "yaml", "xml", "pickle")
        """
        if name in self.data:
            return self.data[name]

        file_path = self._find_file(filename, "data")
        if not file_path:
            print(f"Data file not found: {filename}")
            self.data[name] = {}
            return {}

        metadata = self._get_file_metadata(file_path, "data")

        try:
            # Auto-detect format
            file_ext = Path(filename).suffix.lower()
            if format_hint:
                format_type = format_hint
            elif file_ext in ['.json']:
                format_type = 'json'
            elif file_ext in ['.yaml', '.yml']:
                format_type = 'yaml'
            elif file_ext in ['.xml']:
                format_type = 'xml'
            elif file_ext in ['.pkl', '.pickle']:
                format_type = 'pickle'
            else:
                format_type = 'json'  # Default

            # Load based on format
            if format_type == 'json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
            elif format_type == 'pickle':
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
            elif format_type == 'yaml':
                try:
                    import yaml
                    with open(file_path, 'r') as f:
                        data = yaml.safe_load(f)
                except ImportError:
                    print("PyYAML not available, falling back to JSON")
                    with open(file_path, 'r') as f:
                        data = json.load(f)
            else:
                # Plain text
                with open(file_path, 'r') as f:
                    data = f.read()

            self.data[name] = data
            self.cache.put(f"data_{name}", data)
            metadata.load_count += 1

            print(f"Loaded data: {name} from {file_path}")
            return data

        except Exception as e:
            print(f"Error loading data {file_path}: {e}")
            self.data[name] = {}
            return {}

    def _create_placeholder_image(self, name: str, size: Tuple[int, int]) -> pygame.Surface:
        """Create a placeholder image for missing assets."""
        surface = pygame.Surface(size)
        surface.fill((255, 0, 255))  # Magenta

        # Draw "missing" pattern
        for x in range(0, size[0], 8):
            for y in range(0, size[1], 8):
                if (x // 8 + y // 8) % 2:
                    pygame.draw.rect(surface, (0, 0, 0), (x, y, 8, 8))

        self.images[name] = surface
        return surface

    def preload_asset_pack(self, pack_name: str, pack_config: Dict[str, Any]):
        """
        Preload an entire asset pack for a level or scene.

        Args:
            pack_name: Name of the asset pack
            pack_config: Configuration dictionary
        """
        print(f"Preloading asset pack: {pack_name}")

        # Load images
        if "images" in pack_config:
            for name, config in pack_config["images"].items():
                if isinstance(config, str):
                    self.load_image(f"{pack_name}_{name}", config)
                else:
                    self.load_image(
                        f"{pack_name}_{name}", 
                        config["file"],
                        scale=config.get("scale"),
                        streaming=config.get("streaming", False)
                    )

        # Load sounds
        if "sounds" in pack_config:
            for name, config in pack_config["sounds"].items():
                if isinstance(config, str):
                    self.load_sound(f"{pack_name}_{name}", config)
                else:
                    self.load_sound(
                        f"{pack_name}_{name}",
                        config["file"],
                        volume=config.get("volume", 1.0)
                    )

        # Load animations
        if "animations" in pack_config:
            for name, config in pack_config["animations"].items():
                self.load_animation(f"{pack_name}_{name}", config["file"])

        # Load textures for 2.5D
        if "textures" in pack_config:
            for name, config in pack_config["textures"].items():
                if isinstance(config, str):
                    self.load_texture(f"{pack_name}_{name}", config)
                else:
                    self.load_texture(
                        f"{pack_name}_{name}",
                        config["file"],
                        generate_mipmaps=config.get("mipmaps", False)
                    )

        # Load level data for 2.5D maps
        if "levels" in pack_config:
            for name, config in pack_config["levels"].items():
                self.load_level_data(f"{pack_name}_{name}", config["file"])

        print(f"Asset pack '{pack_name}' preloaded successfully")
    
    def load_level_data(self, name: str, filename: str) -> Dict[str, Any]:
        """
        Load level data for 2.5D maps including walls, sectors, and textures.
        
        Args:
            name: Level identifier
            filename: Level data filename
            
        Returns:
            Level data dictionary
        """
        if name in self.data:
            return self.data[name]
        
        file_path = self._find_file(filename, "data")
        if not file_path:
            print(f"Level file not found: {filename}")
            return {}
        
        try:
            with open(file_path, 'r') as f:
                level_data = json.load(f)
            
            # Validate level data structure
            required_fields = ['walls', 'textures', 'spawn_point']
            for field in required_fields:
                if field not in level_data:
                    level_data[field] = [] if field != 'spawn_point' else {'x': 0, 'y': 0}
            
            # Preload textures referenced in the level
            if 'texture_pack' in level_data:
                for texture_name, texture_file in level_data['texture_pack'].items():
                    self.load_texture(f"level_{name}_{texture_name}", texture_file)
            
            self.data[name] = level_data
            print(f"Loaded level: {name} with {len(level_data.get('walls', []))} walls")
            return level_data
            
        except Exception as e:
            print(f"Error loading level {file_path}: {e}")
            return {}
    
    def create_sample_level(self, name: str) -> Dict[str, Any]:
        """Create a sample level for testing 2.5D rendering."""
        level_data = {
            "name": name,
            "spawn_point": {"x": 100, "y": 100},
            "walls": [
                # Outer walls
                {"start": {"x": 0, "y": 0}, "end": {"x": 500, "y": 0}, "texture": "brick", "height": 64},
                {"start": {"x": 500, "y": 0}, "end": {"x": 500, "y": 500}, "texture": "stone", "height": 64},
                {"start": {"x": 500, "y": 500}, "end": {"x": 0, "y": 500}, "texture": "brick", "height": 64},
                {"start": {"x": 0, "y": 500}, "end": {"x": 0, "y": 0}, "texture": "stone", "height": 64},
                
                # Inner room
                {"start": {"x": 200, "y": 200}, "end": {"x": 300, "y": 200}, "texture": "metal", "height": 48},
                {"start": {"x": 300, "y": 200}, "end": {"x": 300, "y": 300}, "texture": "metal", "height": 48},
                {"start": {"x": 300, "y": 300}, "end": {"x": 200, "y": 300}, "texture": "metal", "height": 48},
                {"start": {"x": 200, "y": 300}, "end": {"x": 200, "y": 250}, "texture": "metal", "height": 48},
            ],
            "sectors": [
                {
                    "floor_height": 0,
                    "ceiling_height": 64,
                    "floor_texture": "floor_tile",
                    "ceiling_texture": "ceiling_tile"
                }
            ],
            "sprites": [
                {"x": 150, "y": 150, "texture": "barrel", "scale": 1.0},
                {"x": 350, "y": 350, "texture": "pillar", "scale": 1.2}
            ],
            "lights": [
                {"x": 250, "y": 250, "intensity": 1.0, "radius": 100, "color": [255, 255, 200]}
            ],
            "texture_pack": {
                "brick": "brick_texture.png",
                "stone": "stone_texture.png", 
                "metal": "metal_texture.png",
                "floor_tile": "floor_texture.png",
                "ceiling_tile": "ceiling_texture.png",
                "barrel": "barrel_sprite.png",
                "pillar": "pillar_sprite.png"
            }
        }
        
        self.data[name] = level_data
        return level_data

    def get_asset_info(self, name: str) -> Optional[Dict]:
        """Get information about a loaded asset."""
        for asset_type in ["images", "sounds", "data", "fonts", "textures", "animations"]:
            assets = getattr(self, asset_type)
            if name in assets:
                # Find metadata
                metadata = None
                for path, meta in self.metadata.items():
                    if meta.asset_type == asset_type[:-1]:  # Remove 's'
                        metadata = meta
                        break

                return {
                    "type": asset_type[:-1],
                    "loaded": True,
                    "size": metadata.size if metadata else 0,
                    "load_count": metadata.load_count if metadata else 0,
                    "last_modified": metadata.last_modified if metadata else 0
                }

        return None

    def unload_asset_pack(self, pack_name: str):
        """Unload all assets from a specific pack."""
        prefix = f"{pack_name}_"

        # Remove from all asset types
        for asset_type in ["images", "sounds", "data", "fonts", "textures", "animations"]:
            assets = getattr(self, asset_type)
            keys_to_remove = [k for k in assets.keys() if k.startswith(prefix)]
            for key in keys_to_remove:
                del assets[key]

        # Clean cache
        cache_keys_to_remove = [k for k in self.cache.cache.keys() if prefix in k]
        for key in cache_keys_to_remove:
            if key in self.cache.cache:
                self.cache.access_order.remove(key)
                del self.cache.cache[key]

        print(f"Unloaded asset pack: {pack_name}")

    def get_memory_usage(self) -> Dict[str, int]:
        """Get memory usage statistics."""
        return {
            "images": len(self.images),
            "sounds": len(self.sounds),
            "data": len(self.data),
            "fonts": len(self.fonts),
            "textures": len(self.textures),
            "animations": len(self.animations),
            "cache_size": len(self.cache.cache),
            "cache_limit": self.cache.max_size
        }

    def optimize_memory(self):
        """Optimize memory usage by clearing unused assets."""
        # Remove assets that haven't been accessed recently
        current_time = pygame.time.get_ticks()
        threshold = 30000  # 30 seconds

        # This is a simplified cleanup - real implementation would track access times
        self.cache.clear()
        print("Memory optimization completed")

    def clear_all(self):
        """Clear all loaded assets."""
        self.images.clear()
        self.sounds.clear()
        self.data.clear()
        self.fonts.clear()
        self.textures.clear()
        self.animations.clear()
        self.cache.clear()
        self.metadata.clear()

        print("All assets cleared from memory")
    
    def _validate_image_file(self, file_path: str) -> bool:
        """Validate image file integrity."""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False
            
            # Check if file can be opened as image
            test_surface = pygame.image.load(file_path)
            if test_surface.get_width() == 0 or test_surface.get_height() == 0:
                return False
                
            return True
        except Exception:
            return False
    
    def validate_all_assets(self) -> Dict[str, List[str]]:
        """Validate all loaded assets and report issues."""
        issues = {
            'corrupted_images': [],
            'missing_sounds': [],
            'invalid_data': [],
            'memory_warnings': []
        }
        
        # Check images
        for name, surface in self.images.items():
            if not surface or surface.get_width() == 0 or surface.get_height() == 0:
                issues['corrupted_images'].append(name)
        
        # Check sounds
        for name, sound in self.sounds.items():
            if not sound:
                issues['missing_sounds'].append(name)
        
        # Check data files
        for name, data in self.data.items():
            if data is None:
                issues['invalid_data'].append(name)
        
        # Memory usage warnings
        total_assets = len(self.images) + len(self.sounds) + len(self.data)
        if total_assets > self.cache.max_size * 0.9:
            issues['memory_warnings'].append(f"High asset count: {total_assets}")
        
        return issues
    
    def create_asset_manifest(self, output_path: str = "asset_manifest.json"):
        """Create a manifest of all loaded assets."""
        manifest = {
            'created_at': time.time(),
            'engine_version': '3.0.5',
            'assets': {
                'images': {
                    name: {
                        'size': surface.get_size(),
                        'format': 'RGBA' if surface.get_flags() & pygame.SRCALPHA else 'RGB'
                    } for name, surface in self.images.items()
                },
                'sounds': {
                    name: {
                        'length': sound.get_length() if hasattr(sound, 'get_length') else 0
                    } for name, sound in self.sounds.items() if sound
                },
                'data': {
                    name: {
                        'type': type(data).__name__,
                        'size': len(str(data)) if data else 0
                    } for name, data in self.data.items()
                }
            },
            'statistics': self.get_memory_usage()
        }
        
        try:
            with open(output_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            print(f"Asset manifest created: {output_path}")
        except Exception as e:
            print(f"Failed to create asset manifest: {e}")
    
    def preload_essential_assets(self):
        """Preload essential game assets for better performance."""
        essential_assets = {
            'ui': {
                'images': {
                    'button': 'ui/button.png',
                    'panel': 'ui/panel.png'
                },
                'sounds': {
                    'click': 'ui/click.wav',
                    'hover': 'ui/hover.wav'
                }
            },
            'effects': {
                'images': {
                    'particle': 'effects/particle.png',
                    'explosion': 'effects/explosion.png'
                },
                'sounds': {
                    'explosion': 'effects/explosion.wav'
                }
            }
        }
        
        for pack_name, pack_data in essential_assets.items():
            try:
                self.preload_asset_pack(pack_name, pack_data)
                print(f"Essential assets '{pack_name}' preloaded")
            except Exception as e:
                print(f"Failed to preload essential assets '{pack_name}': {e}")