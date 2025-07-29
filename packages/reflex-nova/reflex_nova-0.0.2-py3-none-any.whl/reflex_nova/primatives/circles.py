from reflex_nova.primatives import Point
from reflex_nova.primatives.circle import Circle
from reflex_nova.primatives.segment import Segment


def make_circle_from_points(a: Point, b: Point, c: Point):
    """
    Creates a circle that passes through three points: `a`, `b`
    and `c`.

    :param a: `Point`
    :param b: `Point`
    :param c: `Point`
    :return: `Circle`
    """
    chord_one_bisec = Segment(a, b).bisector
    chord_two_bisec = Segment(b, c).bisector
    center = chord_one_bisec.intersection_with(chord_two_bisec)
    radius = center.distance_to(a)

    return Circle(center, radius)
