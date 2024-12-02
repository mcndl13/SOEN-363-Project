from db_config import get_connection

SQL_CREATE_TABLES = """
CREATE TYPE MatchResult AS ENUM ('Home', 'Draw', 'Away');

CREATE DOMAIN AgeDomain AS INT CHECK (VALUE > 0 AND VALUE < 100);

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

CREATE TABLE IF NOT EXISTS ExternalTeamMapping (
    MappingID SERIAL PRIMARY KEY,
    TeamID INT NOT NULL,
    ExternalAPIID VARCHAR(225) NOT NULL,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
    UNIQUE (ExternalAPIID)
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
    HomeTeamID INT NOT NULL,
    AwayTeamID INT NOT NULL,
    SeasonID INT NOT NULL,
    Result MatchResult,
    WinnerTeamID INT,
    City VARCHAR(255),
    Venue VARCHAR(255),
    FOREIGN KEY (HomeTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (WinnerTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (SeasonID) REFERENCES Seasons(SeasonID),
    CONSTRAINT no_self_match CHECK (HomeTeamID <> AwayTeamID),
    CONSTRAINT valid_winner CHECK (
        WinnerTeamID IS NULL OR WinnerTeamID = HomeTeamID OR WinnerTeamID = AwayTeamID
    )
);

CREATE TABLE IF NOT EXISTS Players (
    PlayerID INT PRIMARY KEY,
    JerseyNumber INT,
    Position VARCHAR(225),
    LastName VARCHAR(225),
    FirstName VARCHAR(225),
    Age AgeDomain DEFAULT NULL, -- Default value set to NULL
    Nationality VARCHAR(225),
    TeamID INT NOT NULL,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

CREATE TABLE IF NOT EXISTS Goalkeeper (
    PlayerID INT PRIMARY KEY,
    CleanSheets INT DEFAULT 0,
    PenaltySaves INT DEFAULT 0,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

CREATE TABLE IF NOT EXISTS Defender (
    PlayerID INT PRIMARY KEY,
    Tackles INT DEFAULT 0,
    Interceptions INT DEFAULT 0,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

CREATE TABLE IF NOT EXISTS MatchStatistics (
    StatID SERIAL PRIMARY KEY,
    MatchID INT NOT NULL,     
    PossessionHome INT,
    PossessionAway INT,
    ShotsOnTargetHome INT,
    ShotsOnTargetAway INT,
    ShotsOffTargetHome INT,
    ShotsOffTargetAway INT,
    CornersHome INT,
    CornersAway INT,
    FoulsHome INT,
    FoulsAway INT,
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    UNIQUE (MatchID)
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
