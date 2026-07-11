from dataclasses import dataclass
import questionary
import subprocess
import argparse
import sys


# QUESTIONARY_STYLE = questionary.Style([
#     ('qmark',       'fg:cyan bold'),  # Token for question mark
#     ('question',    'bold'),          # Token for question text
#     ('answer',      'fg:green bold'), # Token for answer text
#     ('pointer',     'fg:cyan bold'),  # Token for selection pointer
#     ('highlighted', 'fg:cyan bold'),  # Token for highlighted choice
#     ('selected',    'fg:cyan bold'),  # Token for selected choice
# ])

QUESTIONARY_STYLE = questionary.Style([
    ('qmark',       'fg:#FFB300 bold'), # Question mark prefix
    ('question',    'bold'),            # The question itself
    ('answer',      'fg:#FFB300 bold'), # Your answer text
    ('pointer',     'fg:#FFB300 bold'), # Pointer for lists
    ('highlighted', 'fg:#FFB300'),      # Highlighted list items
    ('selected',    'fg:#FFB300'),      # Selected items in checkboxes
    ('separator',   'fg:#FF8F00'),      # Separators
    ('instruction', 'fg:#B0BEC5'),      # Subtext instructions
])


class git:
    @dataclass
    class File:
        state: str
        path: str

    @staticmethod
    def changed_files() -> list[File]:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        files = []

        for line in result.stdout.splitlines():
            files.append(git.File(line[:2], line[3:]))

        return files


def run(commit: bool, push: bool, upstream: bool):
    changed = git.changed_files()

    if not changed:
        print('No changes to stage')
        sys.exit(0)

    choices = [f'{file.state} {file.path}' for file in changed]

    selected = questionary.checkbox(
        'Select files to stage (Space to select, Enter to confirm):',
        choices=choices,
        style=QUESTIONARY_STYLE
    ).ask()

    if not selected:
        print('No files selected')
        sys.exit(0)

    for item in selected:
        filepath = item[3:]
        subprocess.run(['git', 'add', filepath])
        print(f'Staged: {filepath}')

    if commit:
        commit_message = questionary.text('Commit message:').ask()
        subprocess.run(['git', 'commit', '-m', commit_message])

        if push:
            cmd = ['git', 'push']
            
            if upstream:
                cmd.extend(['-u', 'origin', 'HEAD'])
            
            subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(prog='git-add')

    parser.add_argument('-c', '--commit',   action='store_true', help='Commit changes after selecting files', dest='commit')
    parser.add_argument('-p', '--push',     action='store_true', help='Push after commiting changes', dest='push')
    parser.add_argument('-u', '--upstream', action='store_true', help='Instead of normal push, run "push -u origin HEAD" (Useful when creating branches upstream)', dest='upstream')
    # TODO: Styles

    args = parser.parse_args()

    run(args.commit, args.push, args.upstream)


if __name__ == '__main__':
    main()
