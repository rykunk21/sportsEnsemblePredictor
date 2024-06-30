use std::time::Duration;


struct Game {
    id: u8,
    first_q: Vec<Drive>,
    second_q: Vec<Drive>,
    third_q: Vec<Drive>,
    fourth_q: Vec<Drive>,
    home_id: u8, // Store team IDs
    away_id: u8, // Store team IDs
}

enum DriveResult {
    Punt,
    Touchdown,
    Fumble,
    TurnoverOnDowns,
    FieldGoal,
    EndGame,
}

enum PlayType {
    Run,
    Pass(bool),
    Punt,
    Turnover,
}

struct Down {
    num: i8,
    dist: i8,
}

struct Drive {
    team_id: u32, // Store team ID
    start_line: i8,
    play_count: i8,
    plays: Vec<Play>,
    yards: i8,
    time: Duration,
    result: DriveResult,
}

struct Play {
    before: Down,
    after: Down,
    play_type: PlayType,
    player_ids: Vec<u32>, // Store player IDs
}
