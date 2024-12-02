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
### Design Considerations

- **IS-A Relationship:**
   - Players entity is the parent entity, Goalkeeper and Defender inherit from Players, each having specific attributes (e.g., CleanSheets for Goalkeepers, Tackles for Defenders).

- **A weak entity:**
   - The MatchStatistics table is a weak entity because it relies on the MatchID from Matches as part of its identity.

- **A complex referential integrity (i.e. using assertions or triggers):**
   - Ensure valid results in the Result attribute (e.g., “Win”, “Loss”, “Draw”).

- **A hard-coded views that filters some rows and columns, based on the user access rights (i.e. a full access user may see all columns while a low-key user may only see certain columns and for a subset of data):**
    - The view MatchesInCity filters matches that took place in the city of Sevilla. This view simplifies querying and allows users to easily retrieve match information specific to that city.

- **Use of domains and types:**
    - Limiting to only the 2023 season.
  
### 2. Implement a relational database
We have designed a relational database schema to organize and store soccer data efficiently. The relational model uses multiple tables to capture entities such as Players, Teams, Matches, and more. 

The database schema includes:
- **Players**: Stores player information such as name, position, nationality, and related statistics.
- **Teams**: Includes team information like team name, founding year, and country.
- **Matches**: Stores match details such as date, home and away teams, and the final score.
- **Leagues**: Contains league information, including league name and associated teams.
- **MatchStatistics**: Contains statistics for matches, like possession, shots, and fouls.
- **Goalkeepers/Defenders**: Inherit from the Players entity and store specific attributes relevant to the respective positions (e.g., CleanSheets for Goalkeepers, Tackles for Defenders).

This schema was implemented by running Python scripts that are connected to the SQL database. 

### 3. Populate the Relational Database from at Least Two Various Sources, by Consuming Public APIs

The relational database is populated by consuming data from two public APIs that provide soccer-related statistics. These data sources are:

1. **API Football** ([https://www.api-football.com/](https://www.api-football.com/)):
   - A RESTful API that provides extensive soccer data, including player profiles, match statistics, league information, and more. We use this API to gather player information, match results, and team statistics.
   
2. **Free API Live Football Data** ([https://rapidapi.com/Creativesdev/api/free-api-live-football-data](https://rapidapi.com/Creativesdev/api/free-api-live-football-data)):
   - This API also offers RESTful endpoints that provide live match data, player statistics, and league standings. We use this API to fetch real-time match data and incorporate it into our database.

We process the data retrieved from these APIs using Python scripts. 

## Phase 2: NoSQL Database Implementation
### 1. Design a NoSQL Database

For the NoSQL implementation, we will use **Neo4j**, a graph database, to store and manage soccer-related data. 

We will write Python scripts to read data from the relational database and transfer it into Neo4j through CSV files. These scripts will use the **neo4j** Python driver to connect to the database and insert the data into  a CSV files that will be inserted as nodes and relationships.
### Design Considerations


During the transfer from the relational database to Neo4j, we may make some design modifications:
- **IS-A Relationships**: In the relational model, we had separate tables for Goalkeepers, Defenders, and other player types. In Neo4j, we will model these as a single **Player** node with a property (e.g., `position`) to distinguish between different types of players. 
- **Weak Entities**: Entities such as **MatchStatistics**, which were considered weak in the relational model, will now be embedded as relationships in Neo4j. For example, match statistics like possession, shots, and fouls will be stored as relationships between the **Match** node and the **Team** node, rather than as a separate entity.
- **Relationships**: In Neo4j, relationships between entities (e.g., Players belong to Teams, Matches involve Teams, etc.) will be explicitly represented using **edges**. This allows us to efficiently query connected data and navigate relationships.


# Report Document
## Football Data Population System

The **Football Data Population System** is built to integrate data from **Football API-Sports** and **Free API Live Football Data** into both **relational** and **NoSQL** databases. The system automates the process of fetching, processing, and storing data related to leagues, seasons, matches, teams, and match statistics. 

---

### Approach

The system uses asynchronous HTTP requests to retrieve data from Football API-Sports. To handle large datasets and avoid API bans, data is processed in batches:
1. **Filtering & Transformation**: The fetched data is filtered, validated, and transformed to match the schema of the target database.
2. **Data Insertion**: After processing, the data is inserted into the database while applying deduplication strategies to avoid data conflicts.

---

### Key Components

1. **Leagues and Seasons**: Handles the retrieval and storage of league details and their corresponding seasons.
2. **Matches**: Collects match data, including fixtures and detailed match information for specific seasons and leagues.
3. **Teams**: Extracts and stores information about teams and their affiliations with various leagues.
4. **Match Statistics**: Processes match statistics, such as possession, fouls, shots, and more, and inserts them into the database.

---

### Database Interaction

The system is designed around a relational database schema that includes the following entities:
- Leagues
- Seasons
- Matches
- Teams
- Match Statistics

During the data insertion process, the **SQL ON CONFLICT** clause is used to ensure no duplication occurs, maintaining data integrity.

---

### Error Handling

The system is equipped with robust error-handling mechanisms:
- **Retry Mechanism**: Uses **exponential backoff** to retry failed requests due to transient issues.
- **Logging Failed Matches**: Matches with missing data or other errors are logged in a **failed_matches.txt** file for future reprocessing.

---

### Batch Processing

The system performs batch processing to:
- Minimize the load on the API and avoid overloading.
- Prevent API bans by ensuring request frequency remains within allowed limits.

---

### Challenges

#### 1. API Rate Limits
- **Problem**: The API limits the number of requests that can be made within a given timeframe.
- **Solution**: The system uses **batching with delays** between requests and implements a retry mechanism to handle `429 Too Many Requests` errors efficiently.

#### 2. Data Completeness
- **Problem**: Some matches may have incomplete statistics or missing team information.
- **Solution**: Matches with incomplete data are flagged and logged in **failed_matches.txt** for future reprocessing.

---

### Future Improvements

1. **Database Optimization**:
   - Implement **indexing** to speed up query performance, especially for match statistics.
   - Consider **partitioning** data based on seasons to optimize data retrieval.

2. **Advanced Logging**:
   - Develop a more robust **centralized logging system** to improve tracking of all failed requests and errors.

3. **Automated Retry Mechanism**:
   - Implement a script that automatically retries processing for matches recorded in **failed_matches.txt**.

---

### Conclusion

The **Football Data Population System** provides a reliable and scalable solution for integrating football data into relational and NoSQL databases. It is designed to handle API rate limits and data inconsistencies through error handling strategies and efficient processing. With future improvements like advanced logging and automated retry mechanisms, the system will continue to grow in reliability and performance.
