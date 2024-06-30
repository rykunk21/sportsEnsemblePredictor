

pub mod players;
pub mod teams;
pub mod games;

pub use teams::defense;
pub use teams::offense;
pub use teams::special_teams;

struct Team {
    id: u8,
    name: String,
    wins: i8,
    players: Vec<u8>, // Store player IDs
    offensive_stats: offense::Summary,
    defensive_stats: defense::Summary,
    special_teams_stats: special_teams::Summary,
}

