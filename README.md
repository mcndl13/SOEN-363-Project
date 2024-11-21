# SOEN 363 Database Project

## Proposal

### Scope and Goal
> This database will focus on soccer statistics, including player profiles, match results, team information, and historical data. It will allow users to query various statistics and trends in soccer.

### Entities and Attributes
Some of the following high-level entities we could use:

- Players: Player profiles including name, nationality, age, position, and statistics
- Teams: Team details such as name, league, and players associated with the team.
- Matches: Information about matches, including date, teams playing, score, and location.
- Leagues: Details about different leagues, including name and associated teams.

### Data sources
- Source 1: https://www.api-football.com/
- API Type: RESTful API
- Source 2: https://rapidapi.com/Creativesdev/api/free-api-live-football-data
- API Type: RESTful API

### Implementation Platform
Proposed RDBMS: PostgreSQL
Proposed NoSQL System: MongoDB

### Programming Platform
Language for API Consumption: Python
Scripting Language: SQL for database queries

### Data Collection Plan
1. Familiarise with APIs, plan data schema, and set up the PostgreSQL database.
2. Begin data collection from 2 data sources
3. Aim for initial datasets (players, teams)
4. Continue data collection, focusing on matches and statistics

### Collaborators
- Michael Shokralla (40209659)
- Mohamed Gueye (40247476)
- Mouhamed Kairson Coundoul (40248237)
- Youssef Francis (40246559)

## Phase 1
### 1. Design a relational database
- How you provide the link between the two data sources. Note that the data that you are collecting may not necessarily use same keys/identifiers.
- At least one IS-A relationship.
- At least one example of a weak entity.
- An example of a complex referential integrity (i.e. using assertions or triggers).
- Examples of a hard-coded views that filters some rows and columns, based on the user access rights (i.e. a full access user may see all columns while a low-key user may only see certain columns and for a subset of data.
- In addition to the above, demonstrate use of domains and types1
- Make sure that no real domain data is used as internal keys (primary/foreign)2
.
### 2. Implement a relational database
### 3. Populate the relational database from at least two various sources, by consuming public APIs
