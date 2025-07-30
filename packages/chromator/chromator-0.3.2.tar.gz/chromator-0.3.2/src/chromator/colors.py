from collections.abc import Iterator

HSLuv = tuple[float, float, float]


def contrasting_color(color: HSLuv) -> HSLuv:
    hue, saturation, lightness = color
    return hue, saturation, (lightness + 50) % 100


def interpolate_numbers(n_1: float, n_2: float, f: float):
    return n_1 + (n_2 - n_1) * f


FULL_CIRCLE = 360
HALF_CIRCLE = FULL_CIRCLE // 2


def interpolate_angles(a_1: float, a_2: float, f: float):
    d = (a_2 - a_1) % FULL_CIRCLE
    return (a_1 + (d if d < HALF_CIRCLE else d - FULL_CIRCLE) * f) % FULL_CIRCLE


def cap_between(v: float, v_min: float, v_max: float):
    return min(max(v_min, v), v_max)


def shades_1(
        color: HSLuv,
        step: int = 5,
        inclusive: bool = False,
) -> Iterator[HSLuv]:
    hue, saturation, _ = color
    s = step if inclusive else 0
    for lightness in range(step - s, 100 + s, step):
        yield hue, saturation, lightness


def shades_2(
        color_1: HSLuv,
        color_2: HSLuv,
        step: int = 5,
        extrapolate: float = 0,
        inclusive: bool = False,
) -> Iterator[HSLuv]:
    _, _, l_1 = color_1
    _, _, l_2 = color_2
    if l_1 > l_2:
        color_1, color_2 = color_2, color_1
    h_1, s_1, l_1 = color_1
    h_2, s_2, l_2 = color_2
    l_1 = interpolate_numbers(l_1, 0, extrapolate)
    l_2 = interpolate_numbers(l_2, 100, extrapolate)
    s = step if inclusive else 0
    for lightness in range(step - s, 100 + s, step):
        f = cap_between((lightness - l_1) / (l_2 - l_1), 0.0, 1.0)
        hue = interpolate_angles(h_1, h_2, f)
        saturation = interpolate_numbers(s_1, s_2, f)
        yield hue, saturation, lightness


def shades(
        color_1: HSLuv,
        color_2: HSLuv = None,
        step: int = 5,
        extrapolate: float = 0,
        inclusive: bool = False,
):
    if color_2:
        yield from shades_2(color_1, color_2, step, extrapolate, inclusive)
    else:
        yield from shades_1(color_1, step, inclusive)
