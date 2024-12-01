-- Basic search query
SELECT * FROM players WHERE teamid = 101;

-- Query for aggregate data
SELECT teamid, COUNT(*) AS player_count
FROM players
GROUP BY teamid;

-- Find Top N Entities Satisfying a Criterion
SELECT * FROM teams
ORDER BY foundedyear DESC
LIMIT 2;

--creating index
CREATE INDEX idx_teamid ON players (teamid);

--query after index
SELECT * FROM players WHERE teamid = 101;


--full text search
SELECT * FROM teams
WHERE teamname LIKE '%Real%';


