import warnings
import vim
import re
import subprocess
from pathlib import Path
from shutil import copy
from appdirs import user_config_dir

user_dir = Path(user_config_dir("inkscape-figures", "Castel"))

if not user_dir.is_dir():
    user_dir.mkdir()

template = user_dir / 'template.svg'


def inkscape(path):
    with warnings.catch_warnings():
        # leaving a subprocess running after interpreter exit raises a
        # warning in Python3.7+
        warnings.simplefilter("ignore", ResourceWarning)
        subprocess.Popen(['inkscape', str(path)])


def latex_template(name, title):
    return [r"\begin{figure}[ht]",
            r"    \centering",
            rf"    \incfig{{{name}}}",
            rf"    \caption{{{title}}}",
            rf"    \label{{fig:{name}}}",
            r"\end{figure}"]


def setup_template():
    return [
        r"% figure support",
        r"\usepackage{import}",
        r"\usepackage{pdfpages}",
        r"\usepackage{transparent}",
        r"\usepackage{xcolor}",
        r"",
        r"\newcommand{\incfig}[2][1]{",
        r"    \def\svgwidth{#1\columnwidth}",
        r"    \import{./figures/}{#2.pdf_tex}",
        r"}"

    ]


def create(title, root):
    """
    Creates a figure.

    First argument is the title of the figure
    Second argument is the figure directory.

    """
    title = title.strip()
    file_name = title.replace(' ', '-').lower() + '.svg'
    figures = Path(root).absolute()
    if not figures.exists():
        figures.mkdir()

    figure_path = figures / file_name

    # If a file with this name already exists, append a '2'.
    if figure_path.exists():
        print(title + ' 2')
        return

    copy(str(template), str(figure_path))
    inkscape(figure_path)

    # Print the code for including the figure to stdout.
    # Copy the indentation of the input.
    # print(indent(latex_template(figure_path.stem, title), indentation=leading_spaces))
    # vim.current.line = indent(latex_template(
    # figure_path.stem, title), indentation=leading_spaces)
    r = vim.current.range
    r.append(latex_template(figure_path.stem, title))
    del vim.current.line

    print("Created figure: ", figure_path)


def get_title(title_line):
    regex = r"(?:incfig{)(.*?)(?:})"
    match = re.search(regex, title_line, flags=0)
    return match.group(1)


def edit(title, root):
    title = title.strip()
    file_name = title.replace(' ', '-').lower() + '.svg'
    figures = Path(root).absolute()
    figure_path = figures / file_name
    inkscape(figure_path)

    print("Edit figure: ", figure_path)


def setup():
    vim.current.range.append(setup_template())
