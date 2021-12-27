# Madison Big Data Meetup Jan 2022

# Overview
This repo showcases running a [Dagster](https://dagster.io/) project locally. This is not an exhaustive demonstration of everything you can accomplish with Dagster but wanted to demonstrate some of the main abstractions of the framework.

Dagit is the UI to interface with Dagster and the 

### Workspaces
There are two pipelines in this workspace `bmi` and `etl`.

| Pipeline | Description | Concepts |
| --- | --- | --- |
| bmi | Calcuate BMI | op, graph, job, schedule, sensor |
| etl | Load data from a system into another system |  resource, config |

# Quick Start
This assumes you have [Docker](https://www.docker.com/) and [Taskfile](https://taskfile.dev/#/) on your local machine. To start up the project do the following:

1. `task start:detached`
2. Access dagit: [http://localhost:3000/](http://localhost:3000/)