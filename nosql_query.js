
db.matches.aggregate([
    {
        $lookup: {
            from: "stats",
            localField: "matchid",
            foreignField: "matchid",
            as: "match_stats"
        }
    },
    { $unwind: "$match_stats" },
    {
        $group: {
            _id: "$hometeamid",
            home_fouls: { $sum: "$match_stats.foulshome" },
            away_fouls: { $sum: "$match_stats.foulsaway" }
        }
    }
]);

//create index
db.players.createIndex({ teamid: 1 });
//query after index
db.players.find({ teamid: 101 });