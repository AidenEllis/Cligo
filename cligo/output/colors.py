import os
import re
from jinja2.filters import pass_environment


__all__ = ['colorFilter']

RESET_RE = '\033\[0m'
RESET = '\033[0m'

COLORS = dict(list(zip(['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', ],
                       list(range(30, 38)))))

COLORS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in COLORS.values()])

HIGHLIGHTS = dict(
    list(zip(['bg_grey', 'bg_red', 'bg_green', 'bg_yellow', 'bg_blue', 'bg_magenta', 'bg_cyan', 'bg_white'],
             list(range(40, 48)))))

HIGHLIGHTS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in HIGHLIGHTS.values()])

ATTRIBUTES = dict(list(zip(['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', ],
                           list(range(30, 38)))))

ATTRIBUTES_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in ATTRIBUTES.values()])


@pass_environment
def colorFilter(environment=None, text=None, color=None, background_color=None, attributes=None):
    """Jinja2 text color filer.

    environment is jinja2 parameter.

    Available colors:
        red, green, yellow, blue, magenta, cyan, white

    Available backgrounds:
        bg_grey, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white

    Available attributes:
        bold, blink, dark, reverse, concealed, underline
    """

    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'

        if color is not None:
            text = re.sub(COLORS_RE + '(.*?)' + RESET_RE, r'\1', text)
            text = fmt_str % (COLORS[color], text)

        if background_color is not None:
            text = re.sub(HIGHLIGHTS_RE + '(.*?)' + RESET_RE, r'\1', text)
            text = fmt_str % (HIGHLIGHTS[background_color], text)

        if attributes is not None:
            text = re.sub(ATTRIBUTES_RE + '(.*?)' + RESET_RE, r'\1', text)

            for attr in attributes:
                text = fmt_str % (ATTRIBUTES[attr], text)

        return text + RESET

    else:
        return text
