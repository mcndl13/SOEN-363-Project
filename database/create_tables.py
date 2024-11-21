import psycopg2
from psycopg2 import Error
import db.config

# Connect to your PostgreSQL database using config values
conn = psycopg2.connect(
    dbname=db.config.DB_NAME,
    user=db.config.DB_USER,
    password=db.config.DB_PASSWORD,
    host=db.config.DB_HOST,
    port=db.config.DB_PORT
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# SQL commands for creating the tables
sql_statements = """
CREATE TABLE Players (
    PlayerID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Position VARCHAR(20),
    Nationality VARCHAR(20)
);

CREATE TABLE League (
    LeagueID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Country VARCHAR(50)
);

CREATE TABLE Goalkeepers (
    PlayerID INT PRIMARY KEY,
    Saves INT,
    ShotsFaced INT,
    ShotsSaved INT,
    CleanSheets INT,
    SavePercentage INT,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

CREATE TABLE Teams (
    TeamID SERIAL PRIMARY KEY,
    TeamName VARCHAR(50),
    Coach VARCHAR(50),
    FoundedYear INT,
    LeagueID INT,
    FOREIGN KEY (LeagueID) REFERENCES League(LeagueID)
);

CREATE TABLE Matches (
    MatchID SERIAL PRIMARY KEY,
    Date DATE,
    HomeTeamID INT,
    AwayTeamID INT,
    Result VARCHAR(10),
    FOREIGN KEY (HomeTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Teams(TeamID)
);

CREATE TABLE MatchEvents (
    EventID SERIAL PRIMARY KEY,
    MatchID INT,
    EventType VARCHAR(50),
    PlayerID INT,
    EventMinute INT,
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

CREATE TABLE Statistics (
    StatID SERIAL PRIMARY KEY,
    PlayerID INT,
    MatchID INT,
    Goals INT,
    Assists INT,
    YellowCards INT,
    RedCards INT,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);

CREATE TABLE HistoricalData (
    RecordID SERIAL PRIMARY KEY,
    TeamID INT,
    Season VARCHAR(20),
    GamesPlayed INT,
    Wins INT,
    Draws INT,
    Losses INT,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);
"""

try:
    # Execute the SQL commands to create the tables
    cursor.execute(sql_statements)

    # Commit the transaction to save the changes
    conn.commit()

    print("Tables created successfully!")

except Exception as e:
    # If there is any error
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
