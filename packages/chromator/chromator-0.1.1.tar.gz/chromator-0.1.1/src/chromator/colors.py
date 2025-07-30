from typing import Iterator


HSLuv = tuple[float, float, float]


# def hsluv_shades(color: HSLuv, step: int):
#     hue, saturation, lightness = color
#     return [(hue, saturation, i) for i in range(step, 100, step)]


# def print_shades_css(label: str, color_hex: str, step: int) -> None:
#     hue, saturation, lightness = hex_to_hsluv(color_hex)
#     print(f'''
#   /*
#   Based on {color_hex}
#   HSLuv:
#   - Hue: {hue:.1f}
#   - Saturation: {saturation:.1f}
#   - Lightness: {lightness:.1f}
#   */
# ''')
#     for i in range(step, 100, step):
#         new_hex = hsluv_to_hex((hue, saturation, i))
#         print(chalk.hex('#000' if i > 50 else '#fff').bg_hex(new_hex)(f'  --{label}-{i * 10}: {new_hex};'))
#     print()


def interpolate_numbers(n_1: float, n_2: float, f: float):
    return n_1 + (n_2 - n_1) * f


def interpolate_angles(a_1: float, a_2: float, f: float):
    d = (a_2 - a_1) % 360
    return (a_1 + (d if d < 180 else d - 360) * f) % 360


def cap_between(v: float, v_min: float, v_max: float):
    return min(max(v_min, v), v_max)


def shades(color_1: HSLuv, color_2: HSLuv, step: int, extrapolate: float) -> Iterator[HSLuv]:
    h_1, s_1, l_1 = color_1
    h_2, s_2, l_2 = color_2
    l_1_extra = interpolate_numbers(l_1, 0, extrapolate)
    l_2_extra = interpolate_numbers(l_2, 100, extrapolate)
    l_diff = l_2_extra - l_1_extra
    for i in range(step, 100, step):
        f = cap_between((i - l_1_extra) / l_diff, 0.0, 1.0)
        hue, sat = interpolate_angles(h_1, h_2, f), interpolate_numbers(s_1, s_2, f)
        yield hue, sat, i


# def print_shades_css(label: str, color_hex_1: str, color_hex_2: str, step: int, extrapolate: float) -> None:
#     h_1, s_1, l_1 = hex_to_hsluv(color_hex_1)
#     h_2, s_2, l_2 = hex_to_hsluv(color_hex_2)
#     print(f'''
#   /*
#   Based on {color_hex_1} & {color_hex_2}
#
#   HSLuv {color_hex_1}:
#   - Hue: {h_1:.1f}
#   - Saturation: {s_1:.1f}
#   - Lightness: {l_1:.1f}
#
#   HSLuv {color_hex_2}:
#   - Hue: {h_2:.1f}
#   - Saturation: {s_2:.1f}
#   - Lightness: {l_2:.1f}
#   */
# ''')
#     l_1_extra = interpolate_numbers(l_1, 0, extrapolate)
#     l_2_extra = interpolate_numbers(l_2, 100, extrapolate)
#     l_diff = l_2_extra - l_1_extra
#     for i in range(step, 100, step):
#         f = cap_between((i - l_1_extra) / l_diff, 0.0, 1.0)
#         hue, sat = interpolate_angles(h_1, h_2, f), interpolate_numbers(s_1, s_2, f)
#         new_hex_bg, new_hex_fg = hsluv_to_hex((hue, sat, i)), hsluv_to_hex((hue, sat, (i + 50) % 100))
#         print(chalk.hex(new_hex_fg).bg_hex(new_hex_bg)(f'  --{label}-{i * 10}: {new_hex_bg};'))
#     print()
