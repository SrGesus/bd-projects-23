# bd-projects-23
DataBase Projects
## Project 1
The first delivery is about creating an Entity-Relationship graph of a healthcare services provider with many clinics, employees, clients, their medications, symptoms, etc. etc..
Along with some other exercises.

## Project 2
The second delivery is implementing the referred system in PostgreSQL, populating the data, adding Integrity Constraints, creating indexes to hasten accesses, analysing the data with OLAP, and developing a webserver with [Flask](https://flask.palletsprojects.com/en/3.0.x/) with an API to create, schedule, and cancel appointments.

### Deploying project 2
Make sure you have your docker socket running.
```bash
git clone git@github.com:SrGesus/bd-projects-23.git --recurse-submodules
cd bd-projects-23/p02/bdist-workspace
docker compose -f docker-compose..app.yml up
```
