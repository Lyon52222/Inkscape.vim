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


def compile(title, root):
    title = title.strip()
    file_name = title.replace(' ', '-').lower() + '.svg'
    figures = Path(root).absolute()
    figure_path = figures / file_name

    pdf_path = figure_path.parent / (figure_path.stem + '.pdf')

    inkscape_version = subprocess.check_output(
        ['inkscape', '--version'], universal_newlines=True)

    # Convert
    # - 'Inkscape 0.92.4 (unknown)' to [0, 92, 4]
    # - 'Inkscape 1.1-dev (3a9df5bcce, 2020-03-18)' to [1, 1]
    # - 'Inkscape 1.0rc1' to [1, 0]
    inkscape_version = re.findall(r'[0-9.]+', inkscape_version)[0]
    inkscape_version_number = [int(part)
                               for part in inkscape_version.split('.')]

    # Right-pad the array with zeros (so [1, 1] becomes [1, 1, 0])
    inkscape_version_number = inkscape_version_number + \
        [0] * (3 - len(inkscape_version_number))

    # Tuple comparison is like version comparison
    if inkscape_version_number < [1, 0, 0]:
        command = [
            'inkscape',
            '--export-area-page',
            '--export-dpi', '300',
            '--export-pdf', pdf_path,
            '--export-latex', figure_path
        ]
    else:
        command = [
            'inkscape', figure_path,
            '--export-area-page',
            '--export-dpi', '300',
            '--export-type=pdf',
            '--export-latex',
            '--export-filename', pdf_path
        ]

    # Recompile the svg file
    completed_process = subprocess.run(command)

    if completed_process.returncode != 0:
        print("Compile Error: ", completed_process.returncode)
    else:
        print("Compile pdf: ", pdf_path)


def setup():
    vim.current.range.append(setup_template())
