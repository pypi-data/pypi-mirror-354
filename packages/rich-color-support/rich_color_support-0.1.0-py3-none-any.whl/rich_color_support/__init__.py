# rich_color_support/__init__.py
import logging
import random
import typing
from enum import StrEnum

logger = logging.getLogger(__name__)


class RichColorsBase(StrEnum):
    pass


class RichColors(RichColorsBase):
    """Rich descriptive color names for 8-bit terminal colors (excluding basic, bright, and grey colors)"""  # noqa: E501

    NAVY_BLUE = "navy_blue"
    DARK_BLUE = "dark_blue"
    BLUE3 = "blue3"
    BLUE1 = "blue1"
    DARK_GREEN = "dark_green"
    DEEP_SKY_BLUE4 = "deep_sky_blue4"
    DODGER_BLUE3 = "dodger_blue3"
    DODGER_BLUE2 = "dodger_blue2"
    GREEN4 = "green4"
    SPRING_GREEN4 = "spring_green4"
    TURQUOISE4 = "turquoise4"
    DEEP_SKY_BLUE3 = "deep_sky_blue3"
    DODGER_BLUE1 = "dodger_blue1"
    DARK_CYAN = "dark_cyan"
    LIGHT_SEA_GREEN = "light_sea_green"
    DEEP_SKY_BLUE2 = "deep_sky_blue2"
    DEEP_SKY_BLUE1 = "deep_sky_blue1"
    GREEN3 = "green3"
    SPRING_GREEN3 = "spring_green3"
    CYAN3 = "cyan3"
    DARK_TURQUOISE = "dark_turquoise"
    TURQUOISE2 = "turquoise2"
    GREEN1 = "green1"
    SPRING_GREEN2 = "spring_green2"
    SPRING_GREEN1 = "spring_green1"
    MEDIUM_SPRING_GREEN = "medium_spring_green"
    CYAN2 = "cyan2"
    CYAN1 = "cyan1"
    PURPLE4 = "purple4"
    PURPLE3 = "purple3"
    BLUE_VIOLET = "blue_violet"
    MEDIUM_PURPLE4 = "medium_purple4"
    SLATE_BLUE3 = "slate_blue3"
    ROYAL_BLUE1 = "royal_blue1"
    CHARTREUSE4 = "chartreuse4"
    PALE_TURQUOISE4 = "pale_turquoise4"
    STEEL_BLUE = "steel_blue"
    STEEL_BLUE3 = "steel_blue3"
    CORNFLOWER_BLUE = "cornflower_blue"
    DARK_SEA_GREEN4 = "dark_sea_green4"
    CADET_BLUE = "cadet_blue"
    SKY_BLUE3 = "sky_blue3"
    CHARTREUSE3 = "chartreuse3"
    SEA_GREEN3 = "sea_green3"
    AQUAMARINE3 = "aquamarine3"
    MEDIUM_TURQUOISE = "medium_turquoise"
    STEEL_BLUE1 = "steel_blue1"
    SEA_GREEN2 = "sea_green2"
    SEA_GREEN1 = "sea_green1"
    DARK_SLATE_GRAY2 = "dark_slate_gray2"
    DARK_RED = "dark_red"
    DARK_MAGENTA = "dark_magenta"
    ORANGE4 = "orange4"
    LIGHT_PINK4 = "light_pink4"
    PLUM4 = "plum4"
    MEDIUM_PURPLE3 = "medium_purple3"
    SLATE_BLUE1 = "slate_blue1"
    WHEAT4 = "wheat4"
    LIGHT_SLATE_GREY = "light_slate_grey"
    MEDIUM_PURPLE = "medium_purple"
    LIGHT_SLATE_BLUE = "light_slate_blue"
    YELLOW4 = "yellow4"
    DARK_SEA_GREEN = "dark_sea_green"
    LIGHT_SKY_BLUE3 = "light_sky_blue3"
    SKY_BLUE2 = "sky_blue2"
    CHARTREUSE2 = "chartreuse2"
    PALE_GREEN3 = "pale_green3"
    DARK_SLATE_GRAY3 = "dark_slate_gray3"
    SKY_BLUE1 = "sky_blue1"
    CHARTREUSE1 = "chartreuse1"
    LIGHT_GREEN = "light_green"
    AQUAMARINE1 = "aquamarine1"
    DARK_SLATE_GRAY1 = "dark_slate_gray1"
    DEEP_PINK4 = "deep_pink4"
    MEDIUM_VIOLET_RED = "medium_violet_red"
    DARK_VIOLET = "dark_violet"
    PURPLE = "purple"
    MEDIUM_ORCHID3 = "medium_orchid3"
    MEDIUM_ORCHID = "medium_orchid"
    DARK_GOLDENROD = "dark_goldenrod"
    ROSY_BROWN = "rosy_brown"
    MEDIUM_PURPLE2 = "medium_purple2"
    MEDIUM_PURPLE1 = "medium_purple1"
    DARK_KHAKI = "dark_khaki"
    NAVAJO_WHITE3 = "navajo_white3"
    LIGHT_STEEL_BLUE3 = "light_steel_blue3"
    LIGHT_STEEL_BLUE = "light_steel_blue"
    DARK_OLIVE_GREEN3 = "dark_olive_green3"
    DARK_SEA_GREEN3 = "dark_sea_green3"
    LIGHT_CYAN3 = "light_cyan3"
    LIGHT_SKY_BLUE1 = "light_sky_blue1"
    GREEN_YELLOW = "green_yellow"
    DARK_OLIVE_GREEN2 = "dark_olive_green2"
    PALE_GREEN1 = "pale_green1"
    DARK_SEA_GREEN2 = "dark_sea_green2"
    PALE_TURQUOISE1 = "pale_turquoise1"
    RED3 = "red3"
    DEEP_PINK3 = "deep_pink3"
    MAGENTA3 = "magenta3"
    DARK_ORANGE3 = "dark_orange3"
    INDIAN_RED = "indian_red"
    HOT_PINK3 = "hot_pink3"
    HOT_PINK2 = "hot_pink2"
    ORCHID = "orchid"
    ORANGE3 = "orange3"
    LIGHT_SALMON3 = "light_salmon3"
    LIGHT_PINK3 = "light_pink3"
    PINK3 = "pink3"
    PLUM3 = "plum3"
    VIOLET = "violet"
    GOLD3 = "gold3"
    LIGHT_GOLDENROD3 = "light_goldenrod3"
    TAN = "tan"
    MISTY_ROSE3 = "misty_rose3"
    THISTLE3 = "thistle3"
    PLUM2 = "plum2"
    YELLOW3 = "yellow3"
    KHAKI3 = "khaki3"
    LIGHT_YELLOW3 = "light_yellow3"
    LIGHT_STEEL_BLUE1 = "light_steel_blue1"
    YELLOW2 = "yellow2"
    DARK_OLIVE_GREEN1 = "dark_olive_green1"
    DARK_SEA_GREEN1 = "dark_sea_green1"
    HONEYDEW2 = "honeydew2"
    LIGHT_CYAN1 = "light_cyan1"
    RED1 = "red1"
    DEEP_PINK2 = "deep_pink2"
    DEEP_PINK1 = "deep_pink1"
    MAGENTA2 = "magenta2"
    MAGENTA1 = "magenta1"
    ORANGE_RED1 = "orange_red1"
    INDIAN_RED1 = "indian_red1"
    HOT_PINK = "hot_pink"
    MEDIUM_ORCHID1 = "medium_orchid1"
    DARK_ORANGE = "dark_orange"
    SALMON1 = "salmon1"
    LIGHT_CORAL = "light_coral"
    PALE_VIOLET_RED1 = "pale_violet_red1"
    ORCHID2 = "orchid2"
    ORCHID1 = "orchid1"
    ORANGE1 = "orange1"
    SANDY_BROWN = "sandy_brown"
    LIGHT_SALMON1 = "light_salmon1"
    LIGHT_PINK1 = "light_pink1"
    PINK1 = "pink1"
    PLUM1 = "plum1"
    GOLD1 = "gold1"
    LIGHT_GOLDENROD2 = "light_goldenrod2"
    NAVAJO_WHITE1 = "navajo_white1"
    MISTY_ROSE1 = "misty_rose1"
    THISTLE1 = "thistle1"
    YELLOW1 = "yellow1"
    LIGHT_GOLDENROD1 = "light_goldenrod1"
    KHAKI1 = "khaki1"
    WHEAT1 = "wheat1"
    CORNSILK1 = "cornsilk1"


class RichColors8(RichColorsBase):
    """8 most essential, high-contrast colors for terminal text"""

    RED = "red1"
    GREEN = "green1"
    BLUE = "blue1"
    YELLOW = "yellow1"
    MAGENTA = "magenta1"
    CYAN = "cyan1"
    WHITE = "white"
    ORANGE = "orange1"


class RichColors16(RichColorsBase):
    """16 popular, well-distinguished colors for terminal text"""

    RED = "red1"
    GREEN = "green1"
    BLUE = "blue1"
    YELLOW = "yellow1"
    MAGENTA = "magenta1"
    CYAN = "cyan1"
    WHITE = "white"
    ORANGE = "orange1"
    BRIGHT_RED = "bright_red"
    DARK_GREEN = "dark_green"
    ROYAL_BLUE = "royal_blue1"
    GOLD = "gold1"
    PURPLE = "purple"
    DARK_CYAN = "dark_cyan"
    LIGHT_CORAL = "light_coral"
    CHARTREUSE = "chartreuse1"


class RichColors32(RichColorsBase):
    """32 readable, distinguishable colors for rich terminal interfaces"""

    RED = "red1"
    GREEN = "green1"
    BLUE = "blue1"
    YELLOW = "yellow1"
    MAGENTA = "magenta1"
    CYAN = "cyan1"
    WHITE = "white"
    ORANGE = "orange1"
    BRIGHT_RED = "bright_red"
    DARK_GREEN = "dark_green"
    ROYAL_BLUE = "royal_blue1"
    GOLD = "gold1"
    PURPLE = "purple"
    DARK_CYAN = "dark_cyan"
    LIGHT_CORAL = "light_coral"
    CHARTREUSE = "chartreuse1"
    NAVY_BLUE = "navy_blue"
    SPRING_GREEN = "spring_green1"
    HOT_PINK = "hot_pink"
    TURQUOISE = "turquoise2"
    VIOLET = "violet"
    SALMON = "salmon1"
    STEEL_BLUE = "steel_blue"
    LIME_GREEN = "green_yellow"
    DARK_ORANGE = "dark_orange"
    MEDIUM_PURPLE = "medium_purple1"
    AQUAMARINE = "aquamarine1"
    INDIAN_RED = "indian_red1"
    CORNFLOWER = "cornflower_blue"
    KHAKI = "khaki1"
    ORCHID = "orchid1"
    TAN = "tan"


class RichColors64(RichColorsBase):
    """64 professional colors for advanced terminal applications"""

    RED = "red1"
    GREEN = "green1"
    BLUE = "blue1"
    YELLOW = "yellow1"
    MAGENTA = "magenta1"
    CYAN = "cyan1"
    WHITE = "white"
    ORANGE = "orange1"
    BRIGHT_RED = "bright_red"
    DARK_GREEN = "dark_green"
    ROYAL_BLUE = "royal_blue1"
    GOLD = "gold1"
    PURPLE = "purple"
    DARK_CYAN = "dark_cyan"
    LIGHT_CORAL = "light_coral"
    CHARTREUSE = "chartreuse1"
    NAVY_BLUE = "navy_blue"
    SPRING_GREEN = "spring_green1"
    HOT_PINK = "hot_pink"
    TURQUOISE = "turquoise2"
    VIOLET = "violet"
    SALMON = "salmon1"
    STEEL_BLUE = "steel_blue"
    LIME_GREEN = "green_yellow"
    DARK_ORANGE = "dark_orange"
    MEDIUM_PURPLE = "medium_purple1"
    AQUAMARINE = "aquamarine1"
    INDIAN_RED = "indian_red1"
    CORNFLOWER = "cornflower_blue"
    KHAKI = "khaki1"
    ORCHID = "orchid1"
    TAN = "tan"
    DEEP_SKY_BLUE = "deep_sky_blue1"
    SEA_GREEN = "sea_green1"
    MEDIUM_ORCHID = "medium_orchid1"
    SANDY_BROWN = "sandy_brown"
    LIGHT_SALMON = "light_salmon1"
    PALE_GREEN = "pale_green1"
    PINK = "pink1"
    PLUM = "plum1"
    WHEAT = "wheat1"
    MISTY_ROSE = "misty_rose1"
    THISTLE = "thistle1"
    DARK_TURQUOISE = "dark_turquoise"
    CADET_BLUE = "cadet_blue"
    DARK_SEA_GREEN = "dark_sea_green1"
    LIGHT_STEEL_BLUE = "light_steel_blue1"
    DARK_VIOLET = "dark_violet"
    ORANGE_RED = "orange_red1"
    YELLOW_GREEN = "yellow3"
    SLATE_BLUE = "slate_blue1"
    MEDIUM_TURQUOISE = "medium_turquoise"
    ROSY_BROWN = "rosy_brown"
    DARK_GOLDENROD = "dark_goldenrod"
    LIGHT_PINK = "light_pink1"
    PALE_TURQUOISE = "pale_turquoise1"
    NAVAJO_WHITE = "navajo_white1"
    HONEYDEW = "honeydew2"
    CORNSILK = "cornsilk1"
    LIGHT_CYAN = "light_cyan1"
    LIGHT_YELLOW = "light_yellow3"
    LIGHT_GREEN = "light_green"
    MEDIUM_SPRING_GREEN = "medium_spring_green"
    DARK_SLATE_GRAY = "dark_slate_gray1"


def get_color_set(size: int) -> typing.List[RichColorsBase]:
    """Get a color set of specified size"""

    if size > len(RichColors64):
        return list(RichColors)

    elif size == 64 or size > len(RichColors32):
        return list(RichColors64)

    elif size == 32 or size > len(RichColors16):
        return list(RichColors32)

    elif size == 16 or size > len(RichColors8):
        return list(RichColors16)

    elif size == 8:
        return list(RichColors8)

    elif size > 0:
        return random.sample(list(RichColors8), size)

    else:
        logger.warning(f"Invalid size: {size}, returning 8 colors")
        return list(RichColors8)


class RichColorRotator:
    def __init__(self, size: int = 16):
        self.size = size
        self.colors = get_color_set(size)
        random.shuffle(self.colors)

    def pick(self) -> RichColorsBase:
        if len(self.colors) == 0:
            self.colors = get_color_set(self.size)
            random.shuffle(self.colors)
        return self.colors.pop()
