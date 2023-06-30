import html
import re

from behave.formatter.ansi_escapes import colors, escapes

from cucu import logger

ESC_SEQ = r"\x1b["
TRANSLATION = {v: f'<span style="color: {k};">' for k, v in colors.items()} | {
    escapes["reset"]: "</span>",
    escapes["up"]: "",  # ignore away move cursor up 1
    ESC_SEQ + "46": "",  # ignore DELETE (num keypad)
    ESC_SEQ + "48": "",  # ignore INSERT (num keypad)
    ESC_SEQ + "49": "",  # ignore END (num keypad)
    ESC_SEQ + "50": "",  # ignore DOWN ARROW (num keypad)
    ESC_SEQ + "51": "",  # ignore PAGE DOWN (num keypad)
    ESC_SEQ + "52": "",  # ignore LEFT ARROW (num keypad)
    ESC_SEQ + "54": "",  # ignore RIGHT ARROW (num keypad)
    ESC_SEQ + "55": "",  # ignore HOME (num keypad)
    ESC_SEQ + "56": "",  # ignore UP ARROW (num keypad)
    ESC_SEQ + "57": "",  # ignore PAGE UP (num keypad)
}
RE_TO_HTML = re.compile("|".join(map(re.escape, TRANSLATION)))

RE_TO_REMOVE = re.compile(r"\x1b\[0m|\x1b\[0;\d\dm")


def remove_ansi(input: str) -> str:
    return RE_TO_REMOVE.sub("", input)


def parse_log_to_html(input: str) -> str:
    """
    Parse an ansi color log to html
    """

    body_start = '<body style="color: white; background-color: 333;">'  # use dark bg since colors are from behave
    body_end = "</body>\n"
    result = f"{body_start}<pre>\n{RE_TO_HTML.sub(lambda match: TRANSLATION[match.group(0)], html.escape(input, quote=False))}\n</pre>{body_end}"
    if ESC_SEQ in result:
        lines = "\n".join([x for x in result.split("\n") if ESC_SEQ in x])
        logger.info(f"Detected unmapped ansi escape code!:\n{lines}")

    return result