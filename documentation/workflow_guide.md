## Workflow guide


### Do this first
* Set yourself ac 'Active' in [Slack](https://ohtuprojekti-hq.slack.com)
* Check [Slack]([https://ohtu-k.slack.com/messages/general/](https://ohtuprojekti-hq.slack.com)) messages
* Check [sprint backlog](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=466729438)
* Pull recent changes from GitHub: `git pull origin main`
  
### Completing a task
* Choose a task from the sprint backlog, write your name into the 'Assigned to' column and set task status to _In progress_
* Create a new branch `git checkout -b AddYourBranchNameHere` and switch to it `git checkout AddYourBranchNameHere`
* Write the code
* Writes tests (Unittest and/or Robot Framework UI tests)
* Run tests and debug until 100 % approval rate
* Commiting: add and commit changed files and push always to your own branch: `git push origin AddYourBranchNameHere`
* Create a pull request in GitHub
* Post a short message in Slack #pull-requess channel about new pull request requiring to be approved and merged. Include a short description of added functionalities and/or bud fixes and if the branch can be closed after approval.
* After the pull request is approved mark the task status as 'Done' in the sprint backlog

### Approving a pull request
* Check Slack #pull-requests channel for pull requests waiting for approval. Note: code submitter can't handle their own pull requests.
* Go to [GitHub pull requests](https://github.com/HY-TKTL/TKT20007-Ohjelmistotuotantoprojekti/pulls) and choose the pull request you want to handle
* Click "Files changed"
* Read the code and review changes/additions
* Check CI test results
* Handling the pull request:
   * Decline the request if there is any conflicts or others issues
   * Approve if no issues/conflicts

### When your workday is over
* Update sprint backlog if needed
* Add your daily hours to the [Tuntikirjanpito file](https://docs.google.com/spreadsheets/d/1rd8avaP7OGhgrX-mo4E5-mgfgCE71X50_aM8jR2hNEc/edit#gid=1189482618)
* Set yourself inactive in Slack
