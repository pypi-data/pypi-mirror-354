import argparse

from hsluv import hex_to_hsluv, hsluv_to_hex
from yachalk import chalk, ColorMode

from .colors import shades


# def shades_1() -> None:
#     parser = argparse.ArgumentParser()
#     parser.add_argument('label', type=str)
#     parser.add_argument('hex', type=str)
#     parser.add_argument('--step', type=int, default=10)
#     args = parser.parse_args()
#     print_shades_css(args.label, f'#{args.hex}', args.step)
#
#
# def shades() -> None:
#     parser = argparse.ArgumentParser()
#     parser.add_argument('label', type=str)
#     parser.add_argument('hex1', type=str)
#     parser.add_argument('hex2', type=str)
#     parser.add_argument('-s', '--step', type=int, default=5)
#     parser.add_argument('-e', '--extrapolate', type=int, default=0)
#     args = parser.parse_args()
#     print_shades_css_2(args.label, f'#{args.hex1}', f'#{args.hex2}', args.step, args.extrapolate / 100)


def print_shades_css(label: str, color_hex_1: str, color_hex_2: str, step: int, extrapolate: float) -> None:
    h_1, s_1, l_1 = hex_to_hsluv(color_hex_1)
    h_2, s_2, l_2 = hex_to_hsluv(color_hex_2)
    print(f'''
  /*
  Based on {color_hex_1} & {color_hex_2} 

  HSLuv {color_hex_1}:
  - Hue: {h_1:.1f}
  - Saturation: {s_1:.1f}
  - Lightness: {l_1:.1f}

  HSLuv {color_hex_2}:
  - Hue: {h_2:.1f}
  - Saturation: {s_2:.1f}
  - Lightness: {l_2:.1f}
  */
''')
    for (hue, sat, i) in shades((h_1, s_1, l_1), (h_2, s_2, l_2), step, extrapolate):
        new_hex_bg = hsluv_to_hex((hue, sat, i))
        new_hex_fg = hsluv_to_hex((hue, sat, (i + 50) % 100))
        print(chalk.hex(new_hex_fg).bg_hex(new_hex_bg)(f'  --{label}-{i * 10}: {new_hex_bg};'))
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('label', type=str)
    parser.add_argument('hex1', type=str)
    parser.add_argument('hex2', type=str)
    parser.add_argument('-s', '--step', type=int, default=5)
    parser.add_argument('-e', '--extrapolate', type=int, default=0)
    args = parser.parse_args()
    print_shades_css(args.label, f'#{args.hex1}', f'#{args.hex2}', args.step, args.extrapolate / 100)
