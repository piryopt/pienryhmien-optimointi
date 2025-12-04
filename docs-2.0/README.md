# Jakaja 2.0

![GHA workflow badge](https://github.com/piryopt/pienryhmien-optimointi/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/piryopt/pienryhmien-optimointi/graph/badge.svg?token=RUVDRPFG4Z)](https://codecov.io/gh/piryopt/pienryhmien-optimointi)

**NOTE! This is version 2.0! Old documentation can be found in [here](https://github.com/piryopt/pienryhmien-optimointi/tree/main/documentation)**

https://jakaja.it.helsinki.fi/

Jakaja is a group assignment optimization application originally developed in the Software Engineering Lab course at the University of Helsinki.  
The system helps assign students into groups based on their preferences, using the **Hungarian Algorithm**. For simplicity's sake, survey creators will be referred to as teachers and responders as students. Teachers can create surveys, to which students submit their preferences for the selection. After the teacher closes the survey, the system divides students into groups based on their responses. The results can be exported to Excel.

The goal of **Jakaja 2.0** is to extend and refine the original system to better handle real-world requirements and improve maintainability.

## Differences from Jakaja 1.0

## Improvements

### Group Size Constraints

- Teachers can define **minimum and maximum group sizes**.
- Groups can be marked as **mandatory**.
- With mandatory groups, group sizes are **strictly enforced**, taking priority over student preferences. (Mandatory groups must still meet the minimum size.)

### Multi-Stage Surveys

- Introduces a new survey type that consists of **multiple stages** (e.g., weeks or time periods).
- During survey creation, **group options are defined separately for each stage**.
- During the answering phase, users **rank group options for each stage**.
  - Groups can have **a shared participation limit across all stages**.
  - Users can mark themselves as **absent** for specific stages.
- After the answering phase, group assignment is performed using the **Hungarian algorithm**, taking absences and participation limits into account.
- Results can be exported as a **single Excel file**, with a **separate sheet for each stage**.
- Multi-stage surveys support all regular survey features such as **copying** and **editing**.

### User Interface & Usability

- The whole interface has been redesigned to be **faster, cleaner, and easier to use**.
- Navigation and layouts are more intuitive, making it simpler to find what you need.
- Includes many **small improvements and fixes** to make the overall experience smoother and more reliable.

### Trash Bin

- Deleted surveys remain in the trash bin for **one week** before being automatically removed.
- Surveys in the trash bin include options to **restore** or **permanently delete** them.

### Demos

- 1st demo (17.10.2025)
- Final demo (12.12.2025)

### Product documentation

    - The product documentation of the previous version is up to date with the newest version of jakaja and it can be found in the root of this repository, in the README.md file.

### Project practicalities and progress documentation

- [Definition of done](https://github.com/piryopt/pienryhmien-optimointi/tree/main/docs-2.0/definition_of_done.md)
- [Product backlog](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=1#gid=1)
- Sprint backlogs

  - [Sprint 0](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=1494077212#gid=1494077212)
  - [Sprint 1](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=1824336089#gid=1824336089)
  - [Sprint 2](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=927574909#gid=927574909)
  - [Sprint 3](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=407338365#gid=407338365)
  - [Sprint 4](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=441830011#gid=441830011)
  - [Sprint 5](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=266792610#gid=266792610)
  - [Sprint 6](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=1919874456#gid=1919874456)
  - [Sprint 7](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=1386915800#gid=1386915800)

- [Working hours](https://docs.google.com/spreadsheets/d/1t5yTwkchwrcYQXv5IyxEG7nFUolOFOQFECdHL8PKsaw/edit?gid=1447160151#gid=1447160151)

### Project team communication

- Telegram
- Meeting up on campus

### The project team

Students:

- Boris Banchev
- Joni Ursin
- Sasu Paukku
- Nanna Ketola
- Tomi Poutanen
- Niilo Kuronen

Supervisor:

- Dodo Lökström
