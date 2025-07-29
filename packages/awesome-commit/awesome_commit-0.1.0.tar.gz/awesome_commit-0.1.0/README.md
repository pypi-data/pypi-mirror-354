# Awesome Commit - An AI Git Commit Helper

## Setup

Clone the project and run the following commands to install the dependencies:

```bash
pip install uv
uv venv --python python3.12
uv pip install -r requirements.txt
```

Copy the `.env.template` file to `.env` and add your Gemini API key.

To obtain a Gemini API key, go to [Google AI Studio](https://aistudio.google.com/
)
and click the "Get API Key" button.

If you plan to use this for corporate work, you may need to use a corporate
Google account to access the Google AI Studio. If you do not want Google to
use your code or prompts to improve their AI models, you may want to switch
to a corporate or paid plan.

## Usage

To run the git commit CLI helper, run the following command:

```bash
source .venv/bin/activate # Activate the virtual environment
PYTHONPATH=src python -m awesome_commit # Run the git commit CLI helper
```

## Integrate with Git

To integrate the git commit CLI helper with git, add the following line to
your `.gitconfig` file:

```text
[alias]
        # Enable commit-ai
        ai = "!PYTHONPATH=<path-to>/src <path-to>/git-cli/.venv/bin/python -m awesome_commit"
```

Update the `<path-to>` with the path to the project directory.

Now, you can run the git commit CLI helper using the following command:

```bash
git ai
```

## Building from source

You can build the package from source with the following commands:

```bash
source .venv/bin/activate
uv pip install build
python -m build
```
