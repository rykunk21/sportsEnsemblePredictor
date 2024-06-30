use std::collections::HashMap;
use std::error::Error;

use crate::nfl::{defense, offense, special_teams};
use crate::web::util::parse_table;

//                    //
//  LEAGUE FUNCTIONS  //
//                    //
pub fn get_league_offense(year: u32) -> Result<HashMap<String, offense::Summary>, Box<dyn Error>> {
    let passing_data = get_offense_passing(year)?;
    let rushing_data = get_offense_rushing(year)?;
    let receiving_data = get_offense_receiving(year)?;
    let scoring_data = get_offense_scoring(year)?;

    let mut league_summary = HashMap::new();

    for team in passing_data.keys() {
        let passing = passing_data.get(team).unwrap().clone();
        let rushing = rushing_data.get(team).unwrap().clone();
        let receiving = receiving_data.get(team).unwrap().clone();
        let scoring = scoring_data.get(team).unwrap().clone();

        let summary = offense::Summary {
            passing,
            rushing,
            receiving,
            scoring,
        };

        league_summary.insert(team.clone(), summary);
    }

    Ok(league_summary)
}

pub fn get_league_defense(year: u32) -> Result<HashMap<String, defense::Summary>, Box<dyn Error>> {
    let passing_data = get_defense_passing(year)?;
    let rushing_data = get_defense_rushing(year)?;
    let receiving_data = get_defense_receiving(year)?;
    let scoring_data = get_defense_scoring(year)?;
    let tackles_data = get_defense_tackles(year)?;
    let downs_data = get_defense_downs(year)?;
    let fumbles_data = get_defense_fumbles(year)?;
    let interceptions_data = get_defense_interceptions(year)?;

    let mut league_summary = HashMap::new();

    for team in passing_data.keys() {
        let passing = passing_data.get(team).unwrap().clone();
        let rushing = rushing_data.get(team).unwrap().clone();
        let receiving = receiving_data.get(team).unwrap().clone();
        let scoring = scoring_data.get(team).unwrap().clone();
        let tackles = tackles_data.get(team).unwrap().clone();
        let downs = downs_data.get(team).unwrap().clone();
        let fumbles = fumbles_data.get(team).unwrap().clone();
        let interceptions = interceptions_data.get(team).unwrap().clone();

        let summary = defense::Summary {
            passing,
            receiving,
            rushing,
            scoring,
            tackles,
            downs,
            fumbles,
            interceptions,
        };

        league_summary.insert(team.clone(), summary);
    }

    Ok(league_summary)
}

pub fn get_league_special_teams(
    year: u32,
) -> Result<HashMap<String, special_teams::Summary>, Box<dyn Error>> {
    let field_goal_data = get_special_teams_field_goal(year)?;
    let scoring_data = get_special_teams_scoring(year)?;
    let kickoffs_data = get_special_teams_kickoffs(year)?;
    let kickoff_return_data = get_special_teams_kickoff_return(year)?;
    let punting_data = get_special_teams_punting(year)?;
    let punt_returns_data = get_special_teams_punt_returns(year)?;

    let mut league_summary = HashMap::new();

    for team in field_goal_data.keys() {
        let field_goals = field_goal_data.get(team).unwrap().clone();
        let scoring = scoring_data.get(team).unwrap().clone();
        let kickoffs = kickoffs_data.get(team).unwrap().clone();
        let kickoff_returns = kickoff_return_data.get(team).unwrap().clone();
        let punting = punting_data.get(team).unwrap().clone();
        let punt_returns = punt_returns_data.get(team).unwrap().clone();

        let summary = special_teams::Summary {
            field_goals,
            scoring,
            kickoffs,
            kickoff_returns,
            punting,
            punt_returns,
        };

        league_summary.insert(team.clone(), summary);
    }

    Ok(league_summary)
}

//                  //
//  TEAM FUNCTIONS  //
//                  //
pub fn get_offense_stats(team: &str, year: u32) -> Result<offense::Summary, Box<dyn Error>> {
    let league_offense = get_league_offense(year)?;

    league_offense
        .get(team)
        .cloned()
        .ok_or_else(|| format!("No data found for team: {}", team).into())
}

pub fn get_defense_stats(team: &str, year: u32) -> Result<defense::Summary, Box<dyn Error>> {
    let league_defense = get_league_defense(year)?;

    league_defense
        .get(team)
        .cloned()
        .ok_or_else(|| format!("No data found for team: {}", team).into())
}

pub fn get_special_teams_stats(
    team: &str,
    year: u32,
) -> Result<special_teams::Summary, Box<dyn Error>> {
    let league_special_teams = get_league_special_teams(year)?;

    league_special_teams
        .get(team)
        .cloned()
        .ok_or_else(|| format!("No data found for team: {}", team).into())
}

//                     //
//  OFFENSE FUNCTIONS  //
//                     //
pub fn get_offense_passing(year: u32) -> Result<HashMap<String, offense::Passing>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/offense/passing/{}/reg/all",
        year
    );
    parse_table(&url, offense::Passing::from)
}

pub fn get_offense_rushing(year: u32) -> Result<HashMap<String, offense::Rushing>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/offense/rushing/{}/reg/all",
        year
    );
    parse_table(&url, offense::Rushing::from)
}

pub fn get_offense_receiving(
    year: u32,
) -> Result<HashMap<String, offense::Receiving>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/offense/receiving/{}/reg/all",
        year
    );
    parse_table(&url, offense::Receiving::from)
}

pub fn get_offense_scoring(year: u32) -> Result<HashMap<String, offense::Scoring>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/offense/scoring/{}/reg/all",
        year
    );
    parse_table(&url, offense::Scoring::from)
}

pub fn get_offense_downs(year: u32) -> Result<HashMap<String, offense::Downs>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/downs/scoring/{}/reg/all",
        year
    );
    parse_table(&url, offense::Downs::from)
}

//                     //
//  DEFENSE FUNCTIONS  //
//                     //

pub fn get_defense_passing(year: u32) -> Result<HashMap<String, defense::Passing>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/passing/{}/reg/all",
        year
    );
    parse_table(&url, defense::Passing::from)
}

pub fn get_defense_rushing(year: u32) -> Result<HashMap<String, defense::Rushing>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/rushing/{}/reg/all",
        year
    );
    parse_table(&url, defense::Rushing::from)
}

pub fn get_defense_receiving(
    year: u32,
) -> Result<HashMap<String, defense::Receiving>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/receiving/{}/reg/all",
        year
    );
    parse_table(&url, defense::Receiving::from)
}

pub fn get_defense_scoring(year: u32) -> Result<HashMap<String, defense::Scoring>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/scoring/{}/reg/all",
        year
    );
    parse_table(&url, defense::Scoring::from)
}

pub fn get_defense_tackles(year: u32) -> Result<HashMap<String, defense::Tackles>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/tackles/{}/reg/all",
        year
    );
    parse_table(&url, defense::Tackles::from)
}

pub fn get_defense_downs(year: u32) -> Result<HashMap<String, defense::Downs>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/downs/{}/reg/all",
        year
    );
    parse_table(&url, defense::Downs::from)
}

pub fn get_defense_fumbles(year: u32) -> Result<HashMap<String, defense::Fumbles>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/fumbles/{}/reg/all",
        year
    );
    parse_table(&url, defense::Fumbles::from)
}

pub fn get_defense_interceptions(
    year: u32,
) -> Result<HashMap<String, defense::Interceptions>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/defense/interceptions/{}/reg/all",
        year
    );
    parse_table(&url, defense::Interceptions::from)
}

//                           //
//  SPECIAL TEAMS FUNCTIONS  //
//                           //
pub fn get_special_teams_field_goal(
    year: u32,
) -> Result<HashMap<String, special_teams::FieldGoals>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/special-teams/field-goals/{}/reg/all",
        year
    );
    parse_table(&url, special_teams::FieldGoals::from)
}

pub fn get_special_teams_scoring(
    year: u32,
) -> Result<HashMap<String, special_teams::Scoring>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/special-teams/scoring/{}/reg/all",
        year
    );
    parse_table(&url, special_teams::Scoring::from)
}

pub fn get_special_teams_kickoffs(
    year: u32,
) -> Result<HashMap<String, special_teams::Kickoffs>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/special-teams/kickoffs/{}/reg/all",
        year
    );
    parse_table(&url, special_teams::Kickoffs::from)
}

pub fn get_special_teams_kickoff_return(
    year: u32,
) -> Result<HashMap<String, special_teams::KickoffReturns>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/special-teams/kickoff-return/{}/reg/all",
        year
    );
    parse_table(&url, special_teams::KickoffReturns::from)
}

pub fn get_special_teams_punting(
    year: u32,
) -> Result<HashMap<String, special_teams::Punting>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/special-teams/punting/{}/reg/all",
        year
    );
    parse_table(&url, special_teams::Punting::from)
}

pub fn get_special_teams_punt_returns(
    year: u32,
) -> Result<HashMap<String, special_teams::PuntReturns>, Box<dyn Error>> {
    let url = format!(
        "https://www.nfl.com/stats/team-stats/special-teams/punt-returns/{}/reg/all",
        year
    );
    parse_table(&url, special_teams::PuntReturns::from)
}

//          //
//  TESTS   //
//          //
mod test {
    use super::*;

    #[test]
    fn test_get_offense_passing() {
        let data = get_offense_passing(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_offense_rushing() {
        let data = get_offense_rushing(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_offense_recieving() {
        let data = get_offense_receiving(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_offense_scoring() {
        let data = get_offense_scoring(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_offense_downs() {
        let data = get_offense_downs(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_passing() {
        let data = get_defense_passing(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_rushing() {
        let data = get_defense_rushing(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_receiving() {
        let data = get_defense_receiving(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_scoring() {
        let data = get_defense_scoring(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_tackles() {
        let data = get_defense_tackles(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_downs() {
        let data = get_defense_downs(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_fumbles() {
        let data = get_defense_fumbles(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_defense_interceptions() {
        let data = get_defense_interceptions(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_special_teams_field_goal() {
        let data = get_special_teams_field_goal(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_special_teams_scoring() {
        let data = get_special_teams_scoring(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_special_teams_kickoffs() {
        let data = get_special_teams_kickoffs(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_special_teams_kickoff_return() {
        let data = get_special_teams_kickoff_return(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_special_teams_punting() {
        let data = get_special_teams_punting(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_special_teams_punt_returns() {
        let data = get_special_teams_punt_returns(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_league_offense() {
        let data = get_league_offense(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_league_defense() {
        let data = get_league_defense(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_league_special_teams() {
        let data = get_league_special_teams(2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_team_offense() {
        let data = get_offense_stats("Patriots", 2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_team_defense() {
        let data = get_defense_stats("Patriots", 2023).unwrap();
        println!("{:?}", data);
    }

    #[test]
    fn test_get_team_special_teams() {
        let data = get_special_teams_stats("Patriots", 2023);
        println!("{:?}", data);
    }
}
