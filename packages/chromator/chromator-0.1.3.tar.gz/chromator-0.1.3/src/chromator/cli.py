import argparse
import sys

from hsluv import hex_to_hsluv, hsluv_to_hex
from yachalk import chalk

from .colors import shades


def print_shades_css(
        label: str,
        hex_1: str,
        hex_2: str = None,
        step: int = 5,
        extrapolate: float = 0,
) -> None:
    h_1, s_1, l_1 = color_1 = hex_to_hsluv(f"#{hex_1}")
    hex_1_fg = hsluv_to_hex((h_1, s_1, (l_1 + 50) % 100))

    if hex_2:
        h_2, s_2, l_2 = color_2 = hex_to_hsluv(f"#{hex_2}")
        hex_2_fg = hsluv_to_hex((h_2, s_2, (l_2 + 50) % 100))
        sys.stdout.write(f"""/*
Based on:

#{chalk.hex(hex_1_fg).bg_hex(hex_1)(hex_1)}:
- Hue: {h_1:.1f}°
- Saturation: {s_1:.1f}%
- Lightness: {l_1:.1f}%

#{chalk.hex(hex_2_fg).bg_hex(hex_2)(hex_2)}:
- Hue: {h_2:.1f}°
- Saturation: {s_2:.1f}%
- Lightness: {l_2:.1f}%
*/
""")

    else:
        color_2 = None
        sys.stdout.write(f"""/*
Based on #{chalk.hex(hex_1_fg).bg_hex(hex_1)(hex_1)}:
- Hue: {h_1:.1f}°
- Saturation: {s_1:.1f}%
- Lightness: {l_1:.1f}%
*/
""")

    for (hue, sat, i) in shades(color_1, color_2, step, extrapolate):
        new_hex_bg = hsluv_to_hex((hue, sat, i))
        new_hex_fg = hsluv_to_hex((hue, sat, (i + 50) % 100))
        sys.stdout.write(chalk.hex(new_hex_fg).bg_hex(new_hex_bg)(
            f"""--{label}-{i:03d}: {new_hex_bg};
"""))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label", type=str)
    parser.add_argument("-c1", "--color1", type=str)
    parser.add_argument("-c2", "--color2", type=str, default=None)
    parser.add_argument("-s", "--step", type=int, default=5)
    parser.add_argument("-e", "--extrapolate", type=int, default=0)
    args = parser.parse_args()

    # chalk.set_color_mode(chalk.get_color_mode())
    print_shades_css(
        args.label,
        args.color1,
        args.color2,
        args.step,
        args.extrapolate / 100,
    )
