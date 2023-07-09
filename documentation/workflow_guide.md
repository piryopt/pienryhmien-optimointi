## Workflow guide


### Do this first
* Set yourself ac 'Active' in [Slack](https://ohtuprojekti-hq.slack.com)
* Check [slack]([https://ohtu-k.slack.com/messages/general/](https://ohtuprojekti-hq.slack.com)) messages
* Check [sprint backlog](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=466729438)
* Pull recent changes from GitHub `git pull origin main`
  
### Completing a task
* Choose a task from the sprint backlog, write your name into the 'Assigned to' column and set task status to _In progress_
* Create a new branch `git checkout -b AddYourBranchNameHere` and switch to it `git checkout AddYourBranchNameHere`
* Write the code
* Writes tests (Unittest and/or Robot Framework UI tests)
* [branching practices etc.](https://github.com/agis-/git-style-guide)
* Commiting: add and commit changed files and push always to your own branch `git push origin AddYourBranchNameHere`
* Create a pull request in GitHub
* Post a short message in Slack #pull-requess channel about new pull request requiring to be approved and merged
* After the pull request is approved mark the task status as 'Done' in the sprint backlog

### When your workday is over
* Add your daily hours to the [Tuntikirjanpito file](https://docs.google.com/spreadsheets/d/1rd8avaP7OGhgrX-mo4E5-mgfgCE71X50_aM8jR2hNEc/edit#gid=1189482618)
