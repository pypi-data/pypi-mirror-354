"""
VoidRay Rigidbody

Provides physics simulation for game objects including velocity,
acceleration, and physics properties like mass and drag.
"""

from ..core.component import Component
from ..math.vector2 import Vector2


class Rigidbody(Component):
    """
    A physics component that gives game objects physical properties
    and behavior in the physics simulation.
    """

    def __init__(self, mass: float = 1.0, drag: float = 0.0, angular_drag: float = 0.0):
        """Initialize the rigidbody component."""
        super().__init__()
        self.mass = max(0.1, mass)  # Prevent zero or negative mass
        self.velocity = Vector2(0, 0)
        self.angular_velocity = 0.0
        self.drag = max(0.0, drag)
        self.angular_drag = max(0.0, angular_drag)
        self.use_gravity = True
        self.is_kinematic = False
        self.accumulated_force = Vector2(0, 0)
        self.accumulated_torque = 0.0

        # Physics material properties
        self.bounciness = 0.0  # Restitution coefficient
        self.friction = 0.5   # Friction coefficient

        # Sleeping system
        self.is_sleeping = False
        self.sleep_timer = 0.0

        # Position and rotation constraints
        self.freeze_position_x = False
        self.freeze_position_y = False
        self.freeze_rotation = False

    def on_attach(self) -> None:
        """Called when attached to a game object."""
        # Register with physics system if available
        if hasattr(self.game_object, 'scene') and self.game_object.scene:
            engine = self.game_object.scene.engine
            if engine and hasattr(engine, 'physics_system'):
                engine.physics_system.add_rigidbody(self)

    def on_detach(self) -> None:
        """Called when detached from a game object."""
        # Unregister from physics system if available
        if hasattr(self.game_object, 'scene') and self.game_object.scene:
            engine = self.game_object.scene.engine
            if engine and hasattr(engine, 'physics_system'):
                engine.physics_system.remove_rigidbody(self)

    def add_force(self, force: Vector2) -> None:
        """
        Add a force to the rigidbody (F = ma, so acceleration = F/m).

        Args:
            force: The force vector to apply
        """
        if not self.is_kinematic:
            self.accumulated_force += force

    def add_impulse(self, impulse: Vector2) -> None:
        """
        Add an impulse to the rigidbody (immediate velocity change).

        Args:
            impulse: The impulse vector to apply
        """
        if not self.is_kinematic:
            velocity_change = impulse / self.mass
            self.velocity += velocity_change

    def add_torque(self, torque: float) -> None:
        """
        Add rotational torque to the rigidbody.

        Args:
            torque: The torque to apply (in degrees per second squared)
        """
        if not self.is_kinematic:
            self.accumulated_torque += torque

    def set_velocity(self, velocity: Vector2) -> None:
        """
        Set the rigidbody's velocity directly.

        Args:
            velocity: The new velocity vector
        """
        self.velocity = velocity.copy()

    def set_angular_velocity(self, angular_velocity: float) -> None:
        """
        Set the rigidbody's angular velocity directly.

        Args:
            angular_velocity: The new angular velocity in degrees per second
        """
        self.angular_velocity = angular_velocity

    def stop(self) -> None:
        """Stop all motion by setting velocities to zero."""
        self.velocity = Vector2.zero()
        self.angular_velocity = 0.0
        self.accumulated_force = Vector2.zero()
        self.accumulated_torque = 0.0

    def set_mass(self, mass: float) -> None:
        """
        Set the mass of the rigidbody.

        Args:
            mass: The new mass (must be positive)
        """
        self.mass = max(0.01, mass)  # Prevent zero or negative mass

    def set_drag(self, drag: float) -> None:
        """
        Set the linear drag coefficient.

        Args:
            drag: The drag coefficient (0 = no drag, higher = more drag)
        """
        self.drag = max(0, drag)

    def set_angular_drag(self, angular_drag: float) -> None:
        """
        Set the angular drag coefficient.

        Args:
            angular_drag: The angular drag coefficient
        """
        self.angular_drag = max(0, angular_drag)

    def set_bounciness(self, bounciness: float) -> None:
        """
        Set the bounciness (restitution) of the rigidbody.

        Args:
            bounciness: The bounciness factor (0 = no bounce, 1 = perfect bounce)
        """
        self.bounciness = max(0, min(1, bounciness))

    def set_gravity_enabled(self, enabled: bool) -> None:
        """
        Enable or disable gravity for this rigidbody.

        Args:
            enabled: Whether gravity should affect this rigidbody
        """
        self.use_gravity = enabled

    def freeze_position(self, x: bool = False, y: bool = False) -> None:
        """
        Freeze position on specific axes.

        Args:
            x: Whether to freeze X position
            y: Whether to freeze Y position
        """
        self.freeze_position_x = x
        self.freeze_position_y = y

    def set_freeze_rotation(self, freeze: bool) -> None:
        """
        Freeze or unfreeze rotation.

        Args:
            freeze: Whether to freeze rotation
        """
        self.freeze_rotation = freeze

    def update(self, delta_time: float) -> None:
        """
        Update the rigidbody physics simulation.

        Args:
            delta_time: Time elapsed since last frame
        """
        if self.is_kinematic or not self.game_object:
            return

        # Apply accumulated forces
        if self.accumulated_force.magnitude() > 0:
            acceleration = self.accumulated_force / self.mass
            self.velocity += acceleration * delta_time
            self.accumulated_force = Vector2.zero()

        # Apply accumulated torque
        if self.accumulated_torque != 0 and not self.freeze_rotation:
            angular_acceleration = self.accumulated_torque / self.mass
            self.angular_velocity += angular_acceleration * delta_time
            self.accumulated_torque = 0.0

        # Apply drag
        if self.drag > 0:
            drag_factor = max(0, 1 - self.drag * delta_time)
            self.velocity *= drag_factor

        # Apply angular drag
        if self.angular_drag > 0:
            angular_drag_factor = max(0, 1 - self.angular_drag * delta_time)
            self.angular_velocity *= angular_drag_factor

        # Update position
        if not self.freeze_position_x:
            self.game_object.transform.position.x += self.velocity.x * delta_time
        if not self.freeze_position_y:
            self.game_object.transform.position.y += self.velocity.y * delta_time

        # Update rotation
        if not self.freeze_rotation:
            self.game_object.transform.rotation += self.angular_velocity * delta_time

    def get_kinetic_energy(self) -> float:
        """
        Calculate the kinetic energy of the rigidbody.

        Returns:
            The kinetic energy (0.5 * m * v^2)
        """
        speed_squared = self.velocity.magnitude_squared()
        return 0.5 * self.mass * speed_squared

    def get_momentum(self) -> Vector2:
        """
        Calculate the momentum of the rigidbody.

        Returns:
            The momentum vector (m * v)
        """
        return self.velocity * self.mass

    def __str__(self) -> str:
        return f"Rigidbody(mass={self.mass}, velocity={self.velocity})"

    def __repr__(self) -> str:
        return (f"Rigidbody(mass={self.mass}, velocity={self.velocity}, "
                f"angular_velocity={self.angular_velocity}, use_gravity={self.use_gravity})")