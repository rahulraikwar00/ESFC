import os
import csv
import click
import requests

GITHUB_API_URL = 'https://api.github.com/graphql'

def run_query(token, repo):
    """Make the API call using requests.post."""
    repo = repo.split("/")
    name = repo[1]
    owner = repo[0]
    query = query_string(name, owner)
    headers = {"Authorization": f"token {token}"}
    try:
        res = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"GitHub API request failed: {e}")

def query_string(name, owner):
    """Build the query string based on the repository name and owner."""
    query = f'
    {{
        repository(name: "{name}", owner: "{owner}") {{
            ref(qualifiedName: "master") {{
                target {{
                    ... on Commit {{
                        id
                        history {{
                            pageInfo {{
                                hasNextPage
                            }}
                            edges {{
                                node {{
                                    author {{
                                        name
                                        email
                                        user {{
                                            name
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}'
    return query

def write_csv(csv_writer, user_data):
    """Write user data to the CSV file."""
    csv_writer.writerow(user_data)

def extract_user_data(edge):
    """Extract user data from the GraphQL result."""
    email = edge['node']['author']['email'].split("+")[-1]
    user_name = edge['node']['author']['name']
    name = edge['node']['author']['user']['name']
    return {'Name': f"{name}", 'Username': f"{user_name}", 'Email': f"{email}"}

def process_result(csv_writer, result):
    """Process the GraphQL result and write unique user data to the CSV file."""
    unique_user_name = set()
    for edge in result['data']['repository']['ref']['target']['history']['edges']:
        user_data = extract_user_data(edge)
        if user_data['Username'] not in unique_user_name:
            write_csv(csv_writer, user_data)
            unique_user_name.add(user_data['Username'])

@click.command()
@click.argument('token', required=True, type=click.STRING)
@click.argument('repo', required=True, type=click.STRING)
def main(token, repo):
    """
    Fetch email, name, and username from a GitHub repository and store them in a CSV file.

    Usage:
    python email_scrap.py <token> <repo_name>
    """
    with open('commits_email.csv', 'w') as new_file:
        fieldnames = ['Name', 'Username', 'Email']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()
        try:
            result = run_query(token, repo)
            process_result(csv_writer, result)
        except Exception as e:
            click.secho(f"Error: {e}", fg='red', bold=True)
            return

    click.secho(f'\n-> 👍 Successfully Saved at {os.path.abspath(os.getcwd())}', fg='green', bold=True)

if __name__ == '__main__':
    main()
