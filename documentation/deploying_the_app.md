# Deployment etc.
This file will cover how the app gets from your computer to production.

TLDR: Github (actions) -> quay.io -> OpenShift (fetches it)

## The Codebase
The codebase is in Github and utilizes Github Actions in many forms. The two files in .github/workflows, staging.yml and production.yml define how the deployment happens.

First we'll cover pushing to staging, then production

## Github To Quay.io
When pushing a branch, staging.yml will create an Docker image to a site called quay.io (you should be invited here somehow). The most relvent lines are the last three of staging.yml. registry defines, well the registry. Username is name of the repository + name of the robot user (not related to robot tests!). Password is read from Github -> Settings -> Secrets and variables -> Actions -> Repository secrets. The token is originally from the quay.io registry, (I think) from https://quay.io/organization/pienryhmien-optimointi?tab=robots, click the gear -> View Credentials. I don't think these things need to be changes, but if for some reason you change the quay.io registry, these need to be changed.

## Quay.io To OpenShift
OpenShift fetches the image, and creates the app using the Dockerfile. Both of the pods do it automatically already.