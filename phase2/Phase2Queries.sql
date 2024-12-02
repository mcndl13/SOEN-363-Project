1. Basic Search Query

MATCH (p:Player)-[:PLAYS_FOR]->(t:Team {team_id: 101})
RETURN p;

MATCH (t:Team {team_id: 101})
RETURN t

2. Aggregate Data Query

MATCH (p:Player)-[:PLAYS_FOR]->(t:Team)
RETURN t.team_id AS TeamID, COUNT(p) AS PlayerCount;

MATCH (m:Match)-[:IN_SEASON]->(s:Season {season_id: 1})
RETURN COUNT(m) AS matches_in_season

3. Top N Entities Query

MATCH (t:Team)
RETURN t.team_id AS TeamID, t.name AS TeamName, t.founded_year AS FoundedYear
ORDER BY t.founded_year DESC
LIMIT 2;

MATCH (t:Team)<-[:HOME_TEAM|:AWAY_TEAM]-(m:Match)
RETURN t.name AS team_name, COUNT(m) AS matches_played
ORDER BY matches_played DESC
LIMIT 5

4. Relational Group By Query (NoSQL Style Aggregate per Category)

MATCH (t:Team)<-[:HOME_TEAM|:AWAY_TEAM]-(m:Match)-[:HAS_STATISTICS]->(ms:MatchStatistics)
RETURN t.name AS team_name,
       SUM(ms.fouls_home) AS total_home_fouls,
       SUM(ms.fouls_away) AS total_away_fouls

MATCH (t:Team)-[:PARTICIPATES_IN]->(l:League)
RETURN l.name AS league_name, COUNT(t) AS total_teams
ORDER BY total_teams DESC

5. Index Creation and Performance Comparison

CREATE INDEX team_id_index FOR (t:Team) ON (t.team_id);

CREATE INDEX season_id_index FOR (s:Season) ON (s.season_id);

CREATE INDEX team_name_index FOR (t:Team) ON (t.name);

6. Full-Text Search

MATCH (t:Team)
WHERE t.name CONTAINS "Real"
RETURN t.name

CREATE FULLTEXT INDEX team_name_fulltext
FOR (t:Team)
ON EACH [t.name]
OPTIONS {
  indexConfig: {
    `fulltext.analyzer`: "standard-folding",
    `fulltext.eventually_consistent`: true
  }
}

CALL db.index.fulltext.queryNodes("team_name_fulltext", "Real")
YIELD node AS t, score
RETURN t.name, score
ORDER BY score DESC;
