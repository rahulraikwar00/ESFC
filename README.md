# Email Scraper for Commit History

This Python script is designed to extract email addresses, names, and usernames from the commit history of a specified GitHub repository.

## Setup Instructions

### Prerequisites
- Make sure you have Python 3 installed. You can check your Python version with `python --version`.
- Obtain a GitHub Personal Access Token (PAT) [here](https://github.com/settings/tokens) with the necessary scopes (e.g., `repo`).

### Installation
1. Clone this repository: `git clone https://github.com/rahulraikwar00/email-scraper.git`
2. Navigate to the project directory: `cd email-scraper`
3. Install dependencies: `pip install -r requirements.txt`

## Run Instructions

### Command-Line Options
- To view available command-line options: `python email_scrape.py --help`

### Example Usage
- Run the script with your GitHub token and the target repository: `python email_scrape.py <your_github_token> <owner/repo>`

## Author

**[Rahul Raikwar](https://github.com/rahulraikwar00)**
- For inquiries or support, contact: [rahulraikwar.cse@gmail.com]

## Disclaimers

- This script requires a GitHub Personal Access Token (PAT) to authenticate with the GitHub API.
- It does not store your GitHub Personal Access Token (PAT) or any extracted data.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests [here](https://github.com/rahulraikwar00/email-scraper/issues).
