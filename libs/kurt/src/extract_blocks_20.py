#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Tim Radvan
#
# This file is part of Kurt.
#
# Kurt is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Kurt is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with Kurt. If not, see <http://www.gnu.org/licenses/>.

"""Builds kurt/scratch20/commands_src.py.

Uses source code of Scratch 2.0 from GitHub:

    https://github.com/LLK/scratch-flash/blob/96a2a9a7fca2d042da25dc0d4423900163ab4f33/src/Specs.as

Original source code (development):

    https://github.com/LLK/scratch-flash/blob/develop/src/Specs.as
    
ScratchX source code (with extension):

    https://github.com/LLK/scratch-flash/blob/scratchx/src/Specs.as

"""

import os
import urllib


SCRATCH_URL = "https://raw.githubusercontent.com/LLK/scratch-flash/96a2a9a7fca2d042da25dc0d4423900163ab4f33/src/Specs.as"
SCRATCHX_URL = "https://raw.githubusercontent.com/LLK/scratch-flash/scratchx/src/Specs.as"

EXPERIMENTAL = True

if not EXPERIMENTAL:
    target_url = SCRATCH_URL
else:
    target_url = SCRATCHX_URL

# get file from repository (raw url)
contents = urllib.urlopen(target_url).read()

# split lines
lines = contents.split("\n")

out = "\
#!/usr/bin/env python\n\
# -*- coding: utf-8 -*-\n\
\n\
# Generated by src/extract_blocks_20.py\n"


def relpath(path):
    """
    Returns the complete path of a partial file given.

    @param path: The incomplete path of the file.
    @return: The string with the complete path in the OS.
    """

    return os.path.join(os.path.dirname(__file__), path)


def add_commands(list_name, commands, comment=None):
    """
    Function to generate a pythonized string with the commands from the original
    source code of Scratch.

    @param list_name: The name of the list variable that contains the commands.
    @param commands: The list per se.
    @param comment: The initial comment to clarify the code. Default: None. 
    """

    global out

    out += "\n"
    out += "# %s\n" % comment

    # write commands array
    if "%s = [" % list_name in out:
        out += "%s += [\n" % list_name
    else:
        out += "%s = [\n" % list_name

    # decompose string for extension (optional)
    if "extension" in comment:
        out += "# add extensions code if not auto-generated\n"

    # eval each line
    for idx in range(len(commands)):
        try:
            for cmd in eval(commands[idx]):
                out += "    %r,\n" % cmd
        except:
            pass

    out += "]\n"


if __name__ == "__main__":
    # search the index in the original source code
    extensions = False
    for (i, line) in enumerate(lines):
        if "commands:Array" in line:
            line_commands = i
            line_extensions = len(lines)

            for (j, line) in enumerate(lines):
                if "extensionSpecs:Array" in line:
                    extensions = True
                    line_extensions = j
                    break
            break

    # set the code for the general commands (and extensions)
    add_commands("commands",
                 lines[line_commands:line_extensions], "commands:Array")

    if extensions:
        add_commands("extras",
                     lines[line_extensions:], "extension:Array")

    # write the new code generated
    f = open(relpath("../kurt/scratch20/commands_src.py"), "w")
    f.write(out)
    f.close()
