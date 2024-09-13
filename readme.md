# NaNda: AI-Powered Commit Message Generator

## Overview
NaNda is an intelligent chatbot designed to automatically generate comprehensive commit messages for GitHub repositories. Leveraging Azure's AI inference service, NaNda analyzes your code changes and task descriptions to create detailed, context-aware commit messages.

## Features
- Automatic parsing of `git diff` for staged changes
- Integration with Azure AI inference service
- Generation of structured commit messages based on code changes and task descriptions
- Support for custom commit message formatting instructions

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/victor-salles/nanda
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your GitHub token: `GITHUB_TOKEN="your-github-token-here"`

## Usage
1. Stage your changes in the repository you want to generate a commit message for.
2. Run the NaNda script:
   ```
   python nanda.py
   ```
3. For now the task description and repository locations are hardcoded, so you will have to edit the `nanda.py` file to specify the task description and repository location:
   - Open `nanda.py` in your preferred text editor
   - Locate the variables `TASK_DESCRIPTION` and `REPOSITORY_PATH`
   - Update these variables with your specific task description and the path to your repository
4. NaNda will analyze your changes and generate a commit message.

## Configuration
You can customize the behavior of NaNda by modifying the following files:
- `instructions.py`: Contains the initial context, commit instructions, and prompt structure for the chatbot.
- `nanda.py`: Main script that implements the chatbot's functionality.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements
- Special thanks to NaN Systems team specially Israel Teixeira for the opportunity to work on this project.
