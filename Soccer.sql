CREATE TABLE Players (
    PlayerID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Position VARCHAR(20),
    Nationality VARCHAR(20)
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
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(50),
    Coach VARCHAR(50),
    FoundedYear INT,
    League VARCHAR(20)
);

CREATE TABLE Matches (
    MatchID INT PRIMARY KEY,
    Date DATE,
    HomeTeamID INT,
    AwayTeamID INT,
    Result VARCHAR(10),
    FOREIGN KEY (HomeTeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (AwayTeamID) REFERENCES Teams(TeamID)
);

CREATE TABLE MatchEvents (
    EventID INT PRIMARY KEY,
    MatchID INT,
    EventType VARCHAR(50),
    PlayerID INT,
    EventMinute INT,
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

CREATE TABLE Statistics (
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

CREATE TABLE HistoricalData (
    RecordID INT PRIMARY KEY,
    TeamID INT,
    Season VARCHAR(20),
    GamesPlayed INT,
    Wins INT,
    Draws INT,
    Losses INT,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);
