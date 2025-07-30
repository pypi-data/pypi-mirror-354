import argparse
import sys

from hsluv import hex_to_hsluv, hsluv_to_hex
from yachalk import chalk

from .colors import HSLuv, shades


def contrasting_color(color: HSLuv) -> HSLuv:
    hue, saturation, lightness = color
    return hue, saturation, (lightness + 50) % 100


def colored(color: HSLuv, s: str = None):
    bg_hex = hsluv_to_hex(color)
    fg_hex = hsluv_to_hex(contrasting_color(color))
    return chalk.hex(fg_hex).bg_hex(bg_hex)(s or bg_hex)


def css_color_comment(color: HSLuv):
    hue, saturation, lightness = color
    return f"""
{colored(color)}:
- Hue: {hue:.1f}°
- Saturation: {saturation:.1f}%
- Lightness: {lightness:.1f}%"""


def print_shades_css(
        label: str,
        hex_1: str,
        hex_2: str = None,
        step: int = 5,
        extrapolate: float = 0,
) -> None:
    color_1 = hex_to_hsluv(f"#{hex_1}")

    if hex_2:
        color_2 = hex_to_hsluv(f"#{hex_2}")
        sys.stdout.write(f"""/*
Based on:
{css_color_comment(color_1)}
{css_color_comment(color_2)}
*/
""")

    else:
        color_2 = None
        sys.stdout.write(f"""/*
Based on:
{css_color_comment(color_1)}
*/
""")

    for h, s, i in shades(color_1, color_2, step, extrapolate / 100):
        color_var = f"--{label}-{i:03d}: {hsluv_to_hex((h, s, i))};\n"
        sys.stdout.write(colored((h, s, i), color_var))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label", type=str)
    parser.add_argument("-c", "--color1", type=str)
    parser.add_argument("-k", "--color2", type=str, default=None)
    parser.add_argument("-s", "--step", type=int, default=5)
    parser.add_argument("-e", "--extrapolate", type=int, default=0)
    args = parser.parse_args()
    print_shades_css(args.label, args.color1, args.color2, args.step, args.extrapolate)
