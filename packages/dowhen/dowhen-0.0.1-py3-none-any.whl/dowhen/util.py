# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/dowhen/blob/master/NOTICE.txt


import inspect


def get_line_number(code, identifier):
    if not isinstance(identifier, (list, tuple)):
        identifier = [identifier]

    agreed_line_number = None

    for ident in identifier:
        if isinstance(ident, int):
            line_number = ident
        elif isinstance(ident, str):
            if ident.startswith("+") and ident[1:].isdigit():
                line_number = code.co_firstlineno + int(ident[1:])
            else:
                lines, start_line = inspect.getsourcelines(code)
                for i, line in enumerate(lines):
                    if line.strip().startswith(ident):
                        line_number = start_line + i
                        break
                else:
                    return None
        else:
            raise TypeError(f"Unknown identifier type: {type(ident)}")

        if agreed_line_number is None:
            agreed_line_number = line_number
        elif agreed_line_number != line_number:
            return None

    return agreed_line_number
