import os
import sys


_to_erase: list[int] = []

def write_live(text: str, newline=False):
    """
    Write text to stdout, keeping track of what was written, so that it can be erased next time.

    Text lines are stripped to terminal column length.
    """
    erase_live()    
    columns, _ = os.get_terminal_size()

    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.rstrip()
        
        nb_chars = len(line)
        if nb_chars > columns:
            line = line[:columns-1] + '…'
            nb_chars = columns

        _to_erase.insert(0, nb_chars)

        sys.stdout.write(line)
        if newline or i < len(lines) - 1:
            sys.stdout.write('\n')

    if newline:
        _to_erase.insert(0, 0)
    
    sys.stdout.flush()


def erase_live():
    """
    Erase text written using :func:`write_live`.

    Text lines are stripped to terminal column length.
    """
    if not _to_erase:
        return
    
    for i, nb_chars in enumerate(_to_erase):
        if i == 0:
            sys.stdout.write('\r') # move to beginning of line
        else:
            sys.stdout.write('\033[F') # move to beginning of previous line
        sys.stdout.write(' ' * nb_chars)
    sys.stdout.write('\r')

    _to_erase.clear()
