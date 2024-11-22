import psycopg2

DB_CONFIG = {
    #Put own credentials
    "dbname": "",
    "user": "",
    "password": "",
    "host": "",
    "port": "",
}

SQL_CREATE_TABLES = """
-- Table for League
CREATE TABLE IF NOT EXISTS League (
    LeagueID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Country VARCHAR(50)
);

-- Table for Players
CREATE TABLE IF NOT EXISTS Players (
    PlayerID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Position VARCHAR(20),
    Nationality VARCHAR(20)
);

-- Table for Goalkeepers
CREATE TABLE IF NOT EXISTS Goalkeepers (
    PlayerID INT PRIMARY KEY,
    Saves INT,
    ShotsFaced INT,
    ShotsSaved INT,
    CleanSheets INT,
    SavePercentage INT,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

-- Table for Teams
CREATE TABLE IF NOT EXISTS Teams (
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(50),
    Coach VARCHAR(50),
    FoundedYear INT,
    LeagueID INT,
    FOREIGN KEY (LeagueID) REFERENCES League(LeagueID)
);

-- Table for Matches
CREATE TABLE IF NOT EXISTS Matches (
    MatchID INT PRIMARY KEY,
    Date DATE,
    HomeTeamID INT,
    AwayTeamID INT,
    Result VARCHAR(10),
    FOREIGN KEY (HomeTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Teams(TeamID)
);

-- Table for Match Events
CREATE TABLE IF NOT EXISTS MatchEvents (
    EventID INT PRIMARY KEY,
    MatchID INT,
    EventType VARCHAR(50),
    PlayerID INT,
    EventMinute INT,
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

-- Table for Player Statistics
CREATE TABLE IF NOT EXISTS Statistics (
    StatID INT PRIMARY KEY,
    PlayerID INT,
    MatchID INT,
    Goals INT,
    Assists INT,
    YellowCards INT,
    RedCards INT,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);

-- Table for Historical Data
CREATE TABLE IF NOT EXISTS HistoricalData (
    RecordID INT PRIMARY KEY,
    TeamID INT,
    Season VARCHAR(20),
    GamesPlayed INT,
    Wins INT,
    Draws INT,
    Losses INT,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);
"""

def create_tables():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        #Create the Tables in Postgres
        cur.execute(SQL_CREATE_TABLES)
        conn.commit()
        print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()
