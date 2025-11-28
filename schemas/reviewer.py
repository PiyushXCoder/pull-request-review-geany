class ReviewPullRequestMessage:
    def __init__(self, installation_id: str, repo_owner: str, repo_name: str, pr_number: int):
        self.installation_id = installation_id 
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.pr_number: int = pr_number
