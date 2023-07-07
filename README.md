# Jakaja application for small group assignment optimization
![GHA workflow badge](https://github.com/piryopt/pienryhmien-optimointi/workflows/CI/badge.svg)

This is the repository of the final product of the [Software Engineering Lab course](https://studies.helsinki.fi/courses/cur/otm-96ddc0a9-a15b-4717-bfdc-23872092b730) (the department of Computer Science in University of Helsinki). 

The application is designed for the Faculty of Educational Sciences of the University of Helsinki. The challenge is assigning large numbers of students into groups. In the past, the group assignment was handled manually with Excel sheets, being slow and tedious. Freely available application solutions are not suitable for large groups and it's difficult to take exceptions into account. The jakaja application is deisgned to fix the issue. A student user can put the options in order of preference and a teacher user can, handle plausible exceptions and assign students into groups.

Jakaja application uses [The Hungarian Algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) to assign students into optional groups. A teacher user can create a survey and a student user can fill their answer into that survey. After survey closes a teacher user handles exceptions and uses the algorithm to assign groups. The results are abailable in a table and can be exported to an Excel sheet. The goal is a fast, efficient and optimal group assignment for the whole group.


### Documentation

[The hungarian Algorithm description](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/hungarian.md)

[Database documentation](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/database_doc.md)

User guide (TBA)

Application architecture (TBA)

Application logic (TBA)


### Project team

Mikko Anttonen
Katja Kvintus
Viljami Latvala
Heli Parviainen
Rasmus Salmela
Jerry Tammi
