
# region Imports
from math import pi, sin, cos

from geo.animation import Animation, EllispePartAnimation
from geo.quadrant import Quadrant
from geo.debug import DEBUG_LEVEL, DebugLevel
from geo.point import Point2D
from geo.shape import Shape
# endregion Imports

class Arc(Shape):
	def __init__(self, start, mid, end, id=None, opacity=1, animation=True, style=True):
		super().__init__(id, animation=Animation if animation else None, style=style)
		if style:
			# Set new default style
			self.set_style(fill_color="none", custom=False)
		if animation:
			self.set_animation_start(start, opacity)
		self.start_point = start
		self.anim_point = start

		self.mid = start - mid
		self.middle_point = start - mid

		self.end = end - start
		self.end_point = end - start

		# More option for arc
		self.rot_x = 0
		self.large_arc = False
		self.invert = False

	# region Animation
	def reset(self):
		self.animations.reset()
		self.anim_point = self.start_point.copy()

	def apply_translation(self, value):
		self.anim_point += value

	def apply_inflation(self, value):
		raise Exception("Not supported yet")
	# endregion Animation

	# region SVG
	def bounding_quadrant(self):
		"""Return a quadrant who contain the shape.
		Returns:
			Quadrant: The quadrant who contain the shape.
		"""
		box = Quadrant.empty_quadrant(2)
		for point in (self.anim_point, self.middle_point, self.end_point):
			box.add_point(point)
		return box

	def svg_content(self):
		"""Return a string who describe the shape.
		Returns:
			str: The string who describe the shape.
		"""
		return f'<path d="m {"{} {}".format(*self.anim_point.coordinates)} ' \
		       f'a {"{} {}".format(*self.mid.coordinates)}' \
		       f" {self.rot_x} {1 if self.large_arc else 0} {1 if self.invert else 0}" \
		       f' {"{} {}".format(*self.end.coordinates)}" {self.get_styles()}></path>'
	# endregion SVG

	# region Override
	def __str__(self):
		return f"{self.__class__.__name__}(Start : {self.start_point} Mid : {self.radius_values} End : {self.end_point})"
	# endregion Override

class EllipseArc(Shape):
	def __init__(self, center, radius, start_angle, end_angle, id=None, opacity=1, animation=True, style=True):
		super().__init__(id, animation=EllispePartAnimation if animation else None, style=style)
		if style:
			# Set new default style
			self.set_style(fill_color="none", custom=False)
		if animation:
			self.animations.set_start(center, opacity, [start_angle, end_angle])

		# Default value, use for reset
		self.center = center
		self.radius = radius
		self.sa = start_angle
		self.ea = end_angle
		self.start_point = None
		self.end_point = None

		# Value of animation
		self.center_anim = center.copy()
		self.radius_anim = radius.copy()
		self.sa_anim = start_angle
		self.ea_anim = end_angle

		# Compute values of start and end with the given angles
		self.compute_angles()

		# More option for arc
		self.rot_x = 0
		self.invert = False
		self.large_arc = False

	def compute_angles(self):
		# Compute angle and apply it to source and dest point
		rx, ry = self.radius_anim
		sr, er = -self.sa_anim * pi / 180, -self.ea_anim * pi / 180
		self.start_point = self.center_anim + Point2D(rx * cos(sr), ry * sin(sr))
		self.end_point = self.center_anim + Point2D(rx * cos(er), ry * sin(er))

		self.large_arc = int(abs(self.ea_anim - self.sa_anim) > 180)
		self.invert = int(self.ea_anim < self.sa_anim)

	# region Animation
	def reset(self):
		self.animations.reset()
		# self.center_anim = self.center.copy()
		self.radius_anim = self.radius.copy()
		self.sa_anim = self.sa.copy()
		self.ea_anim = self.ea.copy()

	def apply_translation(self, value):
		self.center_anim += value

	def apply_inflation(self, value):
		self.radius_anim += value

	def apply_angles(self, angles):
		sa, ea = angles
		self.sa_anim += sa
		self.ea_anim += ea
		self.compute_angles()

	# endregion Animation

	# region SVG
	def bounding_quadrant(self):
		"""Return a quadrant who contain the shape.

		Returns:
			Quadrant: The quadrant who contain the shape.
		"""
		box = Quadrant.empty_quadrant(2)
		for point in (self.start_point, self.end_point):
			box.add_point(point)
		return box

	def svg_content(self):
		"""Return a string who describe the shape.

		Returns:
			str: The string who describe the shape.
		"""
		arc = "M {sx} {sy} " \
		      "A {rx} {ry}, " \
		      "{rot_x}, {fl}, {invert}, " \
		      "{dx} {dy}"

		rx, ry = self.radius_anim
		sx, sy = self.start_point
		dx, dy = self.end_point

		arc = arc.format(sx=sx, sy=sy, rx=rx, ry=ry,
		                 rot_x=self.rot_x,
		                 fl=self.large_arc,
		                 invert=self.invert,
		                 dx=dx, dy=dy)

		string = f'<path d="{arc}" {self.get_styles()}></path>'

		if DEBUG_LEVEL.value <= DebugLevel.VISUAL.value:
			string += f"{self.center_anim.svg_content()} {self.start_point.svg_content()} {self.end_point.svg_content()}"

		return string
	# endregion SVG

	# region Override
	def __str__(self):
		return f"{self.__class__.__name__}(Start : {self.start_point} Center : {self.center_anim} End : {self.end_point})"
	# endregion Override
