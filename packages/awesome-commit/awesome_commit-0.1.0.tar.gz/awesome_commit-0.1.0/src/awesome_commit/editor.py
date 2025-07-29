import tempfile
import subprocess

from awesome_commit.config import AppConfig as config


def edit_file(file_path):
    """Edit a file using the default text editor."""
    cmd = config.COMMIT_EDITOR + " " + file_path
    subprocess.call(cmd, shell=True)


def edit_text(text):
    """Edit text using the default text editor."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(text)
        temp_file.close()
        edit_file(temp_file.name)
        with open(temp_file.name) as f:
            edited_text = f.read()
    return edited_text
