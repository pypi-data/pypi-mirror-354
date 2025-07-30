import json
import os
from collections import defaultdict

this = os.path.dirname(__file__)
COLORS = defaultdict()
with open(os.path.join(this, 'static/colorhunt.json'), 'r') as reader:
    data = json.loads(reader.read())
    for category in data:
        key = list(category.keys())[0]
        items = category[key]
        colors = []
        for item in items:
            colors.extend([color['hex'] for color in  item['colors']])
        COLORS[key] = colors

class PALETTES:
    pastel      = COLORS['pastel']
    vintage     = COLORS['vintage']
    retro       = COLORS['retro']
    neon        = COLORS['neon']
    gold        = COLORS['gold']
    light       = COLORS['light']
    dark        = COLORS['dark']
    warm        = COLORS['warm']
    cold        = COLORS['cold']
    summer      = COLORS['summer']
    fall        = COLORS['fall']
    winter      = COLORS['winter']
    spring      = COLORS['spring']
    happy       = COLORS['happy']
    nature      = COLORS['nature']
    earth       = COLORS['earth']
    night       = COLORS['night']
    space       = COLORS['space']
    rainbow     = COLORS['rainbow']
    gradient    = COLORS['gradient']
    sunset      = COLORS['sunset']
    sky         = COLORS['sky']
    sea         = COLORS['sea']
    kids        = COLORS['kids']
    skin        = COLORS['skin']
    food        = COLORS['food']
    cream       = COLORS['cream']
    coffee      = COLORS['coffee']
    wedding     = COLORS['wedding']
    christmas   = COLORS['christmas']
    halloween   = COLORS['halloween']