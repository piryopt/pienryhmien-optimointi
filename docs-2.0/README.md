# Jakaja 2.0

Jakaja is a group assignment optimization application originally developed in the Software Engineering Lab course at the University of Helsinki.  
The system helps assign students into groups based on their preferences, using the **Hungarian Algorithm**. For simplicity's sake, survey creators will be referred to as teachers and responders as students. Teachers can create surveys, to which students submit their preferences for the selection. After the teacher closes the survey, the system divides students into groups based on their responses. The results can be exported to Excel.

The goal of **Jakaja 2.0** is to extend and refine the original system to better handle real-world requirements and improve maintainability.

## Differences from Jakaja 1.0

### Improvements

- **Group size constraints:**

  - Teachers can define **minimum and maximum group sizes**
  - Group size rules are **stronger than student preferences** (Mandatory groups must still reach a minimum size)

- **Multi-dimensional preferences:**

  - Instead of only a single theme, students can express preferences along **two axes** (_topic_ and _schedule_, or _placement_ and _partner experience_)
  - The assignment algorithm considers both dimensions in optimization

- **Priority groups:**
  - Teachers can assign higher or lower **priority weights** to certain groups
  - Algorithm adapts to balance preferences with these weights

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
