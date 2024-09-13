# Jakaja application for small group assignment optimization
![GHA workflow badge](https://github.com/piryopt/pienryhmien-optimointi/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/piryopt/pienryhmien-optimointi/graph/badge.svg?token=RUVDRPFG4Z)](https://codecov.io/gh/piryopt/pienryhmien-optimointi)

### Project description

https://jakaja.it.helsinki.fi/

This is the repository of the final product of the [Software Engineering Lab course](https://studies.helsinki.fi/courses/cur/otm-96ddc0a9-a15b-4717-bfdc-23872092b730) (the department of Computer Science in University of Helsinki): [the **Jakaja** application](https://jakaja.it.helsinki.fi/).

The Jakaja application is designed for the Faculty of Educational Sciences of the University of Helsinki. The customers challenge is assigning large numbers of students into groups. In the past the group assignment was handled manually with Excel sheets, being slow and tedious. Freely available application solutions are not suitable for large groups and it's difficult to take exceptions into account. The jakaja application is designed to fix the issue. 

The Jakaja application uses [The Hungarian Algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) to assign students into optional groups. A teacher user can create a survey with different options and a student user can fill their answer into that survey. After the survey closes a teacher user handles exceptions and uses the algorithm to assign groups. The results are shown as a table and can be exported to an Excel sheet. The goal is a fast, efficient and optimal group assignment for the whole group.

### Demos

- [1st demo](https://youtu.be/z548R3cHm54) (30.6.2023)
- [Final demo](https://youtu.be/MJJqFB_mtdY) (1.9.2023)


### Product documentation

- [Application architecture](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/architecture.md)
- [Application logic](https://github.com/piryopt/pienryhmien-optimointi/blob/doc_changes/documentation/process_flow_chart.pdf)
- [The hungarian Algorithm description](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/hungarian.md)
- [Database documentation](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/database_docs/)
- [User guide for local testing](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/user_guide.md)
- [User guide for teachers](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/kayttoohje_opettaja_DRAFT.md) - in Finnish
- [Privacy statement](https://piryopt.ext.ocp-prod-0.k8s.it.helsinki.fi/privacy-policy)
- [License](https://github.com/piryopt/pienryhmien-optimointi/blob/main/LICENSE)
- [Testing documentation](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Testing.md)


### Project practicalities and documentation

- [The course instructions and requirements](https://github.com/HY-TKTL/TKT20007-Ohjelmistotuotantoprojekti) - in Finnish
- [Definition of done](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Definition%20of%20done.md)
- [Product backlog](https://tasks.office.com/HelsinkiFI.onmicrosoft.com/en-GB/Home/Planner/#/plantaskboard?groupId=ba568d54-ac10-4284-8546-4bd5009e3f22&planId=PWuNfrTpM0uMVnV2NHTlY5YAEsh-)
- [Project meetings](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/project_meetings.md)
- [Project practices agreed by the project team](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/project_practices.md)
- Sprint backlogs
  - [Sprint 1](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=466729438)
  - [Sprint 2](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=59763564)
  - [Sprint 3](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=1576777136)
  - [Sprint 4](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=1803644692)
  - [Sprint 5](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=453913023)
  - [Sprint 6](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=530975876)
  - [Final week](https://docs.google.com/spreadsheets/d/19JN28VdVESQVGfSUTVLsMB2tkSZfw3HZhc6R9kpa-ng/edit#gid=257246197)
- [Workflow guide](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/workflow_guide.md)
- [Working hours](https://docs.google.com/spreadsheets/d/1rd8avaP7OGhgrX-mo4E5-mgfgCE71X50_aM8jR2hNEc/edit#gid=1189482618)
- [Sprint retrospective memo](https://helsinkifi-my.sharepoint.com/:w:/g/personal/kvintus_ad_helsinki_fi/ESr_fS3hEUVMsg00DHP5vWEBpPcCFS8eZlOT8pXTcdTooA?e=kuOmxE) 


### Project team communication

- [Slack](https://ohtuprojekti-hq.slack.com)
- Zoom


### The project team

Students:
- Mikko Anttonen
- Katja Kvintus
- Viljami Latvala
- Heli Parviainen
- Rasmus Salmela
- Jerry Tammi

Supervisor:
- Tuukka Puonti
