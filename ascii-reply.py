import sys, os, json, re
from art import text2art
from github import Github

try:
    # Get GitHub Token
    gh_token = os.environ['GITHUB_TOKEN']
except:
    print('Error getting GITHUB_TOKEN from environment')
    sys.exit(1)

try:
    # Get GitHub Event Payload
    # GitHub Actions saves the event payload JSON at $GITHUB_EVENT_PATH
    payload_path = os.environ['GITHUB_EVENT_PATH']
except:
    print('Error getting GITHUB_EVENT_PATH from environment')
    sys.exit(1)

try:
    # Read GitHub Event Payload
    with open(payload_path) as f:
        payload = json.load(f)
except Exception as e:
    print('Error loading payload JSON file: ' + str(e))
    sys.exit(1)

try:
    # GitHub API
    g = Github(gh_token)

    # Repo
    repo_name = payload['repository']['full_name']
    repo = g.get_repo(repo_name)

    # Issue
    issue_number = payload['issue']['number']
    issue = repo.get_issue(number=issue_number)

    # Comment body
    comment_body = payload['comment']['body']
except Exception as e:
    print(str(e))
    sys.exit(1)

try:
    # Remove the "/<command> " at the start of the comment
    text = re.sub(r'^\/\w+\ ', '', comment_body)
except:
    raise

assert text !='' , "Command argument is empty!"

# Reply body (markdown)
ascii_text = text2art(text, font='random-medium')
ascii_comment = f"""```
{ascii_text}
```
"""

try:
    # Write issue comment
    issue.create_comment(ascii_comment)
except Exception as e:
    print(str(e))
    sys.exit(1)

print(f"Wrote: {text}")