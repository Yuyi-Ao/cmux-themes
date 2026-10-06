#!/usr/bin/env python3
"""Crop and arrange real cmux screenshots; preserve the original image files.
Requires ImageMagick 7. Crops target the checked-in 2424x1508 captures.
"""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ['slate', 'cool-light', 'plum']
STYLES = ['10-adithsureshbabu', '09-loganoxo', 'tokyo-night']

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', default='/System/Library/Fonts/Menlo.ttc', help='Path to a readable font, or an ImageMagick font name')
    args = parser.parse_args()
    if not shutil.which('magick'):
        raise SystemExit('ImageMagick 7 is required only to rebuild preview sheets.')
    def run(*parts):
        subprocess.run(['magick', *map(str, parts)], check=True, timeout=30)
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        def tile(source, title, crop, width, filename):
            size = subprocess.check_output(['magick', 'identify', '-format', '%wx%h', str(source)], text=True)
            if size != '2424x1508':
                raise ValueError(f'Capture geometry changed for {source.name}: {size}; review crop coordinates.')
            body = temp/(filename+'-body.png')
            label = temp/(filename+'-label.png')
            result = temp/(filename+'.png')
            run(source, '-crop', crop, '+repage', '-resize', str(width), body)
            run('-size', f'{width}x38', 'xc:#151922', '-font', args.font, '-pointsize', '20', '-fill', '#d5dce3', '-gravity', 'West', '-annotate', '+14+0', title, label)
            run(label, body, '-append', result)
            return result
        theme_tiles = [tile(ROOT/'previews/cmux'/f'{n}.png', n, '1885x950+500+115', 1440, n) for n in THEMES]
        run(*theme_tiles, '-append', ROOT/'previews/cmux/overview.png')
        style_tiles = [tile(ROOT/'previews/starship'/f'{n}.png', n, '1885x170+500+230', 1440, 'style-'+n) for n in STYLES]
        run(*style_tiles, '-append', ROOT/'previews/starship/overview.png')
    print('Built cmux/overview.png and starship/overview.png. Inspect both before publishing.')

if __name__ == '__main__':
    main()
