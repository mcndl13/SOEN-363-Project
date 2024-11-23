-- Basic SELECT with a simple WHERE clause
SELECT * FROM Defender d
WHERE d.tackles > 10;

-- Basic SELECT with GROUP BY clause (without having)
SELECT Country, COUNT(*) AS TeamCount
FROM Teams
GROUP BY Country;

--Basic SELECT with GROUP BY clause (with having)
SELECT Country, COUNT(*) AS TeamCount
FROM Teams
GROUP BY Country
HAVING COUNT(*) > 5;

-- Simple JOIN query
SELECT Teams.TeamName, League.Name AS LeagueName
FROM Teams
JOIN TeamLeagues ON Teams.TeamID = TeamLeagues.TeamID
JOIN League ON TeamLeagues.LeagueID = League.LeagueID;


-- Simple Cartesian Product with WHERE clause:
SELECT Teams.TeamName, League.Name AS LeagueName
FROM Teams, League, TeamLeagues
WHERE Teams.TeamID = TeamLeagues.TeamID
  AND TeamLeagues.LeagueID = League.LeagueID;

--   Inner JOIN
SELECT Matches.MatchID, Teams.TeamName AS HomeTeam, Seasons.SeasonYear
FROM Matches
INNER JOIN Teams ON Matches.HomeTeamID = Teams.TeamID
INNER JOIN Seasons ON Matches.SeasonID = Seasons.SeasonID;

--  Left JOIN
SELECT Matches.MatchID, Teams.TeamName AS HomeTeam, League.Name AS LeagueName
FROM Matches
LEFT JOIN Teams ON Matches.HomeTeamID = Teams.TeamID
LEFT JOIN TeamLeagues ON Teams.TeamID = TeamLeagues.TeamID
LEFT JOIN League ON TeamLeagues.LeagueID = League.LeagueID;

-- Right JOIN
SELECT Matches.MatchID, Teams.TeamName AS AwayTeam, Matches.City
FROM Matches
RIGHT JOIN Teams ON Matches.AwayTeamID = Teams.TeamID;

-- Full JOIN
SELECT Matches.MatchID, Teams.TeamName, Matches.Venue
FROM Matches
FULL OUTER JOIN Teams ON Matches.HomeTeamID = Teams.TeamID;

-- Using NULL values
SELECT *
FROM Matches
WHERE WinnerTeamID IS NULL;

-- 	Using NULL to show non-applicable data
SELECT PlayerID, CleanSheets 
FROM Goalkeeper
WHERE CleanSheets IS NULL;

-- Correlated Queries ex1
SELECT TeamName
FROM Teams t
WHERE EXISTS (
    SELECT 1
    FROM Players p
    WHERE p.TeamID = t.TeamID AND p.Age < 25
);

---- Correlated Queries ex2
SELECT TeamName
FROM Teams t
WHERE TeamID NOT IN (
    SELECT TeamID 
    FROM Matches 
    WHERE WinnerTeamID IS NOT NULL
);


-- Set OPERATIONS : union
SELECT TeamName 
FROM Teams
WHERE Country = 'England'
UNION
SELECT TeamName
FROM Teams
WHERE FoundedYear > 1900;

-- Set OPERATIONS : intersect
SELECT TeamName 
FROM Teams
WHERE Country = 'England'
INTERSECT
SELECT TeamName
FROM Teams
WHERE FoundedYear > 1900;

-- Set OPERATIONS : except
SELECT TeamName 
FROM Teams
WHERE Country = 'England'
EXCEPT
SELECT TeamName
FROM Teams
WHERE FoundedYear > 1900;

-- HARD-CODED view ( matches in sevilla)
CREATE  VIEW MatchesinCity AS
SELECT 
    Matches.MatchID,
    Matches.Date,
    Matches.City,
    Matches.Venue,
    HomeTeam.TeamName AS HomeTeam,
    AwayTeam.TeamName AS AwayTeam,
    Matches.Result
FROM 
    Matches
INNER JOIN Teams AS HomeTeam ON Matches.HomeTeamID = HomeTeam.TeamID
INNER JOIN Teams AS AwayTeam ON Matches.AwayTeamID = AwayTeam.TeamID
WHERE 
    Matches.City = 'Sevilla'; 

SELECT * FROM MatchesInSevilla;
-- Overlap Constraint
SELECT TeamName
FROM Teams
WHERE TeamID IN (
    SELECT HomeTeamID 
    FROM Matches
) AND TeamID IN (
    SELECT AwayTeamID 
    FROM Matches
);

-- Covering Constraint
SELECT TeamID
FROM Teams
WHERE NOT EXISTS (
    SELECT 1
    FROM Matches
    WHERE Matches.HomeTeamID = Teams.TeamID
       OR Matches.AwayTeamID = Teams.TeamID
);

-- regular nested query using NOT IN
SELECT t.TeamID, t.TeamName
FROM Teams t
WHERE NOT EXISTS (
    SELECT 1
    FROM Matches m
    WHERE m.HomeTeamID = t.TeamID
    AND m.AwayTeamID NOT IN (
        SELECT AwayTeamID 
        FROM Matches 
        WHERE HomeTeamID = t.TeamID
    )
);

-- correlated nested query using NOT EXISTS and EXCEPT
SELECT t.TeamID, t.TeamName
FROM Teams t
WHERE NOT EXISTS (
    SELECT MatchID
    FROM Matches
    WHERE AwayTeamID = t.TeamID
    EXCEPT
    SELECT MatchID
    FROM Matches
    WHERE HomeTeamID = t.TeamID
);


