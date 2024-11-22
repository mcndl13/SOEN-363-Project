from db_config import get_connection

SQL_CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS League (
    LeagueID INT PRIMARY KEY,
    Name VARCHAR(225),
    Country VARCHAR(225)
);

CREATE TABLE IF NOT EXISTS Seasons (
    SeasonID SERIAL PRIMARY KEY,
    LeagueID INT NOT NULL,
    SeasonYear INT NOT NULL,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (LeagueID) REFERENCES League(LeagueID),
    UNIQUE (LeagueID, SeasonYear)
);

CREATE TABLE IF NOT EXISTS Teams (
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(225),
    FoundedYear INT,
    Country VARCHAR(225)
);

CREATE TABLE IF NOT EXISTS TeamLeagues (
    TeamLeagueID SERIAL PRIMARY KEY,
    TeamID INT NOT NULL,
    LeagueID INT NOT NULL,
    SeasonID INT NOT NULL,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (LeagueID) REFERENCES League(LeagueID),
    FOREIGN KEY (SeasonID) REFERENCES Seasons(SeasonID),
    UNIQUE (TeamID, LeagueID, SeasonID)
);

CREATE TABLE IF NOT EXISTS Matches (
    MatchID INT PRIMARY KEY,
    Date DATE,
    HomeTeamID INT,
    AwayTeamID INT,
    SeasonID INT NOT NULL,
    Result VARCHAR(225),
    FOREIGN KEY (HomeTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (SeasonID) REFERENCES Seasons(SeasonID)
);

CREATE TABLE IF NOT EXISTS Players (
    PlayerID INT PRIMARY KEY,
    Name VARCHAR(225),
    Age INT,
    Nationality VARCHAR(225),
    TeamID INT NOT NULL,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

CREATE TABLE IF NOT EXISTS MatchStatistics (
    StatID SERIAL PRIMARY KEY,
    PlayerID INT NOT NULL,
    MatchID INT NOT NULL,
    Goals INT DEFAULT 0,
    Assists INT DEFAULT 0,
    YellowCards INT DEFAULT 0,
    RedCards INT DEFAULT 0,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    UNIQUE (PlayerID, MatchID)  -- Unique constraint added
);
"""

def create_tables():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute(SQL_CREATE_TABLES)
        conn.commit()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
