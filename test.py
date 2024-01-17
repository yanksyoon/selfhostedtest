import argparse
import secrets
import time

from git import Repo
from github import Github
from github.GithubException import GithubException
from github.Repository import Repository

parser = argparse.ArgumentParser(description="test")
parser.add_argument("--token", type=str, help="token")

ns = parser.parse_args()

client = Github(ns.token)
repo: Repository = client.get_repo("yanksyoon/selfhostedtest")

test_branch = f"test/{secrets.token_hex(4)}"
print(Repo().head.commit.hexsha, f"refs/heads/{test_branch}")
branch_ref = repo.create_git_ref(
    ref=f"refs/heads/{test_branch}", sha=Repo().head.commit.hexsha
)


def get_branch():
    """Get newly created branch."""
    try:
        branch = repo.get_branch(test_branch)
    except GithubException as err:
        if err.status == 404:
            return False
        raise
    return branch


while not get_branch():
    print("sleep")
    time.sleep(5)

branch = get_branch()
workflow = repo.get_workflow("workflow_dispatch_ssh_debug.yaml")
assert workflow.create_dispatch(
    branch, inputs={"runner": "hello world"}
), "Failed to dispatch workflow"
