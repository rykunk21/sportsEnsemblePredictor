
use std::collections::{HashMap, HashSet};
use std::error::Error;

use crate::nfl::players::*;
use crate::web::util::{parse_player_table, get_player_team};

//                    //
//  LEAGUE FUNCTIONS  //
//                    //

pub fn get_league_players(year: u32) -> Result<HashMap<String, Player>, Box<dyn Error>> { 

    dbg!("Getting League Summary ...");
    let league_summary = get_league_player_summary(year).unwrap();
    dbg!("League Summary Complete!");
    
    let mut player_summaries = HashMap::new();

    let player_count= league_summary.len();
    let mut current_count = 1;
    for (url_suffix, stats) in league_summary.iter() {

        dbg!(format!("Scraping player {}: {} of {}", url_suffix, current_count, player_count));

        let url = format!("https://www.nfl.com/players/{}", url_suffix);

        let info = match get_player_team(&url) {
            Ok(info) => info,
            Err(e) => {
                eprintln!("Error fetching player team data for {}: {}", url_suffix, e);
                current_count += 1;
                continue; // Skip to the next iteration of the loop
            }
        };
    

        let name =  info[0].to_owned();
        let position = Position::from(&info[1]).unwrap();
        
        let jersey_num = match info[2].trim_start_matches('•').trim_start_matches('#').trim().parse::<u8>() {
            Ok(num) => num,
            Err(e) => {
                eprintln!("Error parsing jersey number from URL {}: {}", url, e);
                255
            }
        };
        let team_parts: Vec<&str> = info[3].split_whitespace().collect();
        let team = team_parts.last().unwrap_or(&"").to_string();

        let status = info[4].to_owned();

        let player = Player {
            name,
            jersey_num,
            team,
            status,
            position,
            stats: stats.clone()
        };

        dbg!(&player);
        current_count += 1;
        player_summaries.insert(url_suffix.clone(), player);
    }

    Ok(player_summaries)

}

pub fn get_league_player_summary(year: u32) -> Result<HashMap<String, Summary>, Box<dyn Error>> {
    let passing: HashMap<String, Passing> = get_league_passing(year)?;
    let rushing: HashMap<String, Rushing> = get_league_rushing(year)?;
    let receiving: HashMap<String, Receiving> = get_league_receiving(year)?;
    let fumbles: HashMap<String, Fumbles> = get_league_fumbles(year)?;
    let tackles: HashMap<String, Tackles> = get_league_tackles(year)?;
    let interceptions: HashMap<String, Interceptions> = get_league_interceptions(year)?;
    let field_goals: HashMap<String, FieldGoals> = get_league_field_goals(year)?;
    let kickoffs: HashMap<String, Kickoffs> = get_league_kickoffs(year)?;
    let kickoff_returns: HashMap<String, KickoffReturns> = get_league_kickoff_returns(year)?;
    let punting: HashMap<String, Punting> = get_league_punting(year)?;
    let punt_returns: HashMap<String, PuntReturns> = get_league_punt_returns(year)?;

    let mut all_players = HashSet::new();

    for key in passing.keys() {
        all_players.insert(key.clone());
    }
    for key in rushing.keys() {
        all_players.insert(key.clone());
    }
    for key in receiving.keys() {
        all_players.insert(key.clone());
    }
    for key in fumbles.keys() {
        all_players.insert(key.clone());
    }
    for key in tackles.keys() {
        all_players.insert(key.clone());
    }
    for key in interceptions.keys() {
        all_players.insert(key.clone());
    }
    for key in field_goals.keys() {
        all_players.insert(key.clone());
    }
    for key in kickoffs.keys() {
        all_players.insert(key.clone());
    }
    for key in kickoff_returns.keys() {
        all_players.insert(key.clone());
    }
    for key in punting.keys() {
        all_players.insert(key.clone());
    }
    for key in punt_returns.keys() {
        all_players.insert(key.clone());
    }

    for key in &all_players {
        println!("{}", key)
    }

    let mut league_summary = HashMap::new();

    for player in &all_players {
        let passing_data = passing.get(player).cloned().unwrap_or_default();
        let rushing_data = rushing.get(player).cloned().unwrap_or_default();
        let receiving_data = receiving.get(player).cloned().unwrap_or_default();
        let fumbles_data = fumbles.get(player).cloned().unwrap_or_default();
        let tackles_data = tackles.get(player).cloned().unwrap_or_default();
        let interceptions_data = interceptions.get(player).cloned().unwrap_or_default();
        let field_goals_data = field_goals.get(player).cloned().unwrap_or_default();
        let kickoffs_data = kickoffs.get(player).cloned().unwrap_or_default();
        let kickoff_returns_data = kickoff_returns.get(player).cloned().unwrap_or_default();
        let punting_data = punting.get(player).cloned().unwrap_or_default();
        let punt_returns_data = punt_returns.get(player).cloned().unwrap_or_default();

        let player_summary = Summary {
            passing: passing_data,
            rushing: rushing_data,
            receiving: receiving_data,
            fumbles: fumbles_data,
            tackles: tackles_data,
            interceptions: interceptions_data,
            field_goals: field_goals_data,
            kickoffs: kickoffs_data,
            kickoff_returns: kickoff_returns_data,
            punting: punting_data,
            punt_returns: punt_returns_data,
        };

        league_summary.insert(player.clone(), player_summary);
    }

    Ok(league_summary)
}

pub fn get_league_passing(year: u32) -> Result<HashMap<String, Passing>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/player-stats/category/passing/{}/reg/all/passingyards/desc",
        year
    );
    parse_player_table(&url, Passing::from)
}

pub fn get_league_rushing(year: u32) -> Result<HashMap<String, Rushing>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/player-stats/category/rushing/{}/reg/all/rushingyards/desc",
        year
    );
    parse_player_table(&url, Rushing::from)
}

pub fn get_league_receiving(year: u32) -> Result<HashMap<String, Receiving>, Box<dyn Error>> {
    let url = format!("https://www.nfl.com/stats/player-stats/category/receiving/{}/reg/all/receivingreceptions/desc", year);
    parse_player_table(&url, Receiving::from)
}

pub fn get_league_fumbles(year: u32) -> Result<HashMap<String, Fumbles>, Box<dyn Error>> {
    let url = format!("https://www.nfl.com/stats/player-stats/category/fumbles/{}/reg/all/defensiveforcedfumble/desc", year);
    parse_player_table(&url, Fumbles::from)
}

pub fn get_league_tackles(year: u32) -> Result<HashMap<String, Tackles>, Box<dyn Error>> {
    let url = format!("https://www.nfl.com/stats/player-stats/category/tackles/{}/reg/all/defensivecombinetackles/desc", year);
    parse_player_table(&url, Tackles::from)
}

pub fn get_league_interceptions(
    year: u32,
) -> Result<HashMap<String, Interceptions>, Box<dyn Error>> {
    let url = format!("https://www.nfl.com/stats/player-stats/category/interceptions/{}/reg/all/defensiveinterceptions/desc", year);
    parse_player_table(&url, Interceptions::from)
}

pub fn get_league_field_goals(year: u32) -> Result<HashMap<String, FieldGoals>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/player-stats/category/field-goals/{}/reg/all/kickingfgmade/desc",
        year
    );
    parse_player_table(&url, FieldGoals::from)
}

pub fn get_league_kickoffs(year: u32) -> Result<HashMap<String, Kickoffs>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/player-stats/category/kickoffs/{}/reg/all/kickofftotal/desc",
        year
    );
    parse_player_table(&url, Kickoffs::from)
}

pub fn get_league_kickoff_returns(
    year: u32,
) -> Result<HashMap<String, KickoffReturns>, Box<dyn Error>> {
    let url = format!("https://www.nfl.com/stats/player-stats/category/kickoff-returns/{}/reg/all/kickreturnsaverageyards/desc", year);
    parse_player_table(&url, KickoffReturns::from)
}

pub fn get_league_punting(year: u32) -> Result<HashMap<String, Punting>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/player-stats/category/punts/{}/reg/all/puntingaverageyards/desc",
        year
    );
    parse_player_table(&url, Punting::from)
}

pub fn get_league_punt_returns(year: u32) -> Result<HashMap<String, PuntReturns>, Box<dyn Error>> {
    let url = format!("https://www.nfl.com/stats/player-stats/category/punt-returns/{}/reg/all/puntreturnsaverageyards/desc", year);
    parse_player_table(&url, PuntReturns::from)
}

//                    //
//  PLAYER FUNCTIONS  //
//                    //
pub fn get_player(name: &str) -> Result<Player, Box<dyn Error>> {
    todo!()
}

pub fn get_player_passing(name: &str) -> Result<Passing, Box<dyn Error>> {
    todo!()
}

pub fn get_player_rushing(name: &str) -> Result<Rushing, Box<dyn Error>> {
    todo!()
}

pub fn get_player_receiving(name: &str) -> Result<Receiving, Box<dyn Error>> {
    todo!()
}

pub fn get_player_fumbles(name: &str) -> Result<Fumbles, Box<dyn Error>> {
    todo!()
}

pub fn get_player_tackles(name: &str) -> Result<Tackles, Box<dyn Error>> {
    todo!()
}

pub fn get_player_interceptions(name: &str) -> Result<Interceptions, Box<dyn Error>> {
    todo!()
}

pub fn get_player_feild_goals(name: &str) -> Result<FieldGoals, Box<dyn Error>> {
    todo!()
}

pub fn get_player_kickoffs(name: &str) -> Result<Kickoffs, Box<dyn Error>> {
    todo!()
}

pub fn get_player_kickoff_returns(name: &str) -> Result<KickoffReturns, Box<dyn Error>> {
    todo!()
}

mod test {
    use super::*;

    #[test]
    fn test_get_player_summaries() {
        let league = get_league_player_summary(2023);
        println!("{:?}", league);
    }

    #[test]
    fn test_get_players(){
        get_league_players(2023);
    }
    
    #[test]
    fn test_get_player_team(){

        let player = "derius-davis";

        let url = format!("https://www.nfl.com/players/{}", player);

        let data = get_player_team(&url).unwrap();

        println!("{:?}", data);
    }
}
