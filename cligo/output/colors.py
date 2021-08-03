import os
import re
from jinja2.filters import pass_environment


__all__ = ['colorFilter', 'colorText']

RESET_RE = '\033\[0m'
RESET = '\033[0m'

COLORS = dict(list(zip(['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', ],
                       list(range(30, 38)))))

COLORS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in COLORS.values()])

BACKGROUNDS = dict(
    list(zip(['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'],
             list(range(40, 48)))))

BACKGROUNDS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in BACKGROUNDS.values()])


@pass_environment
def colorFilter(environment=None, text=None, color=None, bg_color=None):
    """
    Jinja2 text color filer.
    environment: is jinja2 parameter.
    """

    return colorText(text=text, color=color, bg_color=bg_color)


def colorText(text=None, color=None, bg_color=None):
    """
    Available colors:
        grey, red, green, yellow, blue, magenta, cyan, white

    Available backgrounds:
        grey, red, green, yellow, blue, magenta, cyan, white

    Available attributes:
        bold, blink, dark, reverse, concealed, underline
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'

        if color is not None:
            text = re.sub(COLORS_RE + '(.*?)' + RESET_RE, r'\1', text)
            text = fmt_str % (COLORS[color], text)

        if bg_color is not None:
            text = re.sub(BACKGROUNDS_RE + '(.*?)' + RESET_RE, r'\1', text)
            text = fmt_str % (BACKGROUNDS[bg_color], text)

        return text + RESET

    else:
        return text
