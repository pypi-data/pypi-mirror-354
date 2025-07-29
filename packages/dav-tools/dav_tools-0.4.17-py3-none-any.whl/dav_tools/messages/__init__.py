'''Print messages on screen and ask for user input.'''

import sys as _sys

from .formatted_text import TextFormat
from .formatted_text import FormattedText

from .utils import read_input as _read_input
from .utils import clear_line as _clear_line

_debug_counter = 0


def message(*text: str | object,
            text_min_len: list[int] = [], default_text_options: list = [], additional_text_options: list[list] = [[]],
            icon: str = None, icon_options: list = [],
            end: str = '\n', file = _sys.stderr) -> str:
    '''
    Generic and customizable message.

    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param default_text_options: Styling options applied to all messages.
    :param additional_text_options: Styling options applied to single messages.
    :param icon: Character to use as icon, between ``[ ]``.
    :param icon_options: Styling options applied to the icon.
    :param end: Character to output at the end of the message.
    :param file: Where to write the message.
    '''

    _clear_line(file=file)

    result = ''

    # icon
    if icon is not None:
        result += str(FormattedText(f'[{icon}]',  *icon_options, TextFormat.Style.BOLD))
        result += ' '
    
    # text
    for i in range(len(text)):
        line_text = str(text[i])
        line_options = (default_text_options + additional_text_options[i]) if i < len(additional_text_options) else default_text_options
        line_end = ' ' if i < len(text) - 1 else ''

        result += str(FormattedText(line_text, *line_options))
        result += line_end

        # padding
        if i < len(text_min_len):
            line_padding = text_min_len[i] - len(line_text)
            if line_padding > 0:
               result += ' ' * line_padding

    # printing
    if file is not None:
        print(result, file=file, end=end, flush=True)
    
    return result
    

def debug(*text: str | object, color: bytes = TextFormat.Color.PURPLE, text_min_len: list[int] = [], text_options: list[list] = [[]], file = _sys.stderr):
    '''
    Debugging message, which stands out from all other messages. Each messages has also a unique ID.
    
    :param text: The message(s) to print.
    :param color: Message color. Default = Purple
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param file: Where to write the message.
    '''

    global _debug_counter
    _debug_counter += 1

    message(*text,
            icon=f'DEBUG {_debug_counter:04}',
            icon_options=[
                color,
                TextFormat.Style.REVERSE,
            ],
            text_min_len=text_min_len,
            default_text_options=[
                color,
            ],
            additional_text_options=text_options,
            file=file)

def info(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], file = _sys.stderr):
    '''
    Message indicating an information.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param file: Where to write the message.
    '''

    message(*text,
            icon='*',
            icon_options=[
                TextFormat.Color.CYAN
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.CYAN
            ],
            additional_text_options=text_options,
            file=file)


def progress(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], file = _sys.stderr):
    '''
    Message indicating an action which is still happening.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param file: Where to write the message.
    '''

    message(*text,
            icon=' ',
            end='\r',
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Style.DIM,
                TextFormat.Style.ITALIC
            ],
            additional_text_options=text_options
    )


def error(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], file = _sys.stderr):
    '''
    Message indicating an error.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param file: Where to write the message.
    '''
    
    message(*text, 
            icon='-', 
            icon_options=[
                TextFormat.Color.RED
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.RED
            ],
            additional_text_options=text_options,
            file=file
    )


def critical_error(*text: str | object, text_min_len: list[int] = [], exit_code: int = 1, file = _sys.stderr):
    '''
    Message indicating a critical error. The program terminates after showing this message.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param exit_code: The exit code of the program.
    :param file: Where to write the message.
    '''
    
    message(*text, 
            icon='x', 
            icon_options=[
                TextFormat.Color.RED
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.RED
            ],
            file=file
    )

    _sys.exit(exit_code)


def warning(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], file = _sys.stderr):
    '''
    Message indicating a warning.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param file: Where to write the message.
    '''

    message(*text, 
            icon='!', 
            icon_options=[
                TextFormat.Color.YELLOW
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.YELLOW
            ],
            additional_text_options=text_options,
            file=file
    )


def success(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], file = _sys.stderr):
    '''
    Message indicating a successfully completed action.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param file: Where to write the message.
    '''

    message(*text, 
            icon='+', 
            icon_options=[
                TextFormat.Color.GREEN
            ],
            text_min_len=text_min_len,
            default_text_options=[TextFormat.Color.GREEN],
            additional_text_options=text_options,
            file=file
    )


def ask(question: str, end=': ', secret: bool = False, file = _sys.stderr) -> str:
    '''
    Prints a question to screen and returns the answer.
    
    :param question: The question to print.
    :param end: Characters to be printed at the end of the question.
    :param file: Where to write the message.
    
    :returns: The user's answer.
    '''

    message(f'{question}{end}',
            icon='?',
            icon_options=[
                TextFormat.Color.PURPLE
            ],
            default_text_options=[TextFormat.Color.PURPLE],
            end='',
            file=file)
    
    return _read_input(
        TextFormat.Color.PURPLE,
        TextFormat.Style.ITALIC,
        secret=secret,
        file=file
    )

def ask_yn(text: str, default_yes=False, file = _sys.stderr) -> bool:
    '''
    Prints a question asking the user a Yes/No question.
    Returns the answer as a boolean (Yes = True, No = False).
    
    :param text: The message to print.
    :param default_yes: Automatically accept when pressing Enter.
    :param file: Where to write the message.
    '''
    message = f'{text}'

    if default_yes:
        message += f' (Y/n)'
    else:
        message += f' (y/N)'

    while True:
        answer = ask(message, end=' ', file=file)

        if answer.lower() == 'y' or (len(answer) == 0 and default_yes):
            return True
        if answer.lower() == 'n' or (len(answer) == 0 and not default_yes):
            return False


def ask_continue(text: str=None, default_yes=False, file = _sys.stderr):
    '''
    Prints a question asking the user if they want to continue executing the program:
    a positive answer makes the program continues its normal execution;
    a negative answer terminates the program.
    Optionally supports a custom message.
    
    :param text: The message to print.
    :param default_yes: Automatically accept when pressing Enter.
    :param file: Where to write the message.
    '''
    if text is not None:
        message = f'{text}. Continue?'
    else:
        message = 'Continue?'

    if not ask_yn(message, default_yes=default_yes, file=file):
        _sys.exit(1)


