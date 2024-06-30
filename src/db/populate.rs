
use tokio::task;

#[tokio::main]
pub async fn populate_special_teams(year: u32) -> surrealdb::Result<()> {

    let data = task::spawn_blocking(move || {
        crate::web::teams::get_league_special_teams(year).expect("ERROR IN STATS")

    }).await;

    match data {
        Ok(st_summary_map) => {
            // Iterate over the HashMap<String, offense::Summary>
            for (team_name, summary) in st_summary_map.iter() {
                println!("Team: {}", team_name);
                
                super::insert("special_teams", team_name, summary).await?;
            }
        },
        Err(e) => {
            eprintln!("Error fetching league offense data: {}", e);
            // Handle the error as needed
        }
    }

    Ok(())
}

#[tokio::main]
pub async fn populate_offense(year: u32) -> surrealdb::Result<()> {

    let data = task::spawn_blocking(move || {
        crate::web::teams::get_league_offense(year).expect("ERROR IN STATS")

    }).await;

    match data {
        Ok(offense_summary_map) => {
            // Iterate over the HashMap<String, offense::Summary>
            for (team_name, summary) in offense_summary_map.iter() {
                println!("Team: {}", team_name);
                
                super::insert("offense", team_name, summary).await?;
            }
        },
        Err(e) => {
            eprintln!("Error fetching league offense data: {}", e);
            // Handle the error as needed
        }
    }

    Ok(())
}


#[tokio::main]
pub async fn populate_defense(year: u32) -> surrealdb::Result<()> {

    let data = task::spawn_blocking(move || {
        crate::web::teams::get_league_defense(year).expect("ERROR IN STATS")

    }).await;

    match data {
        Ok(defense_summary_map) => {
            // Iterate over the HashMap<String, offense::Summary>
            for (team_name, summary) in defense_summary_map.iter() {
                println!("Team: {}", team_name);
                
                super::insert("defense", team_name, summary).await?;
            }
        },
        Err(e) => {
            eprintln!("Error fetching league offense data: {}", e);
            // Handle the error as needed
        }
    }

    Ok(())
}


#[tokio::main]
pub async fn populate_players(year: u32) -> surrealdb::Result<()> {

    let data = task::spawn_blocking(move || {
        crate::web::players::get_league_players(year).expect("ERROR IN STATS")

    }).await;

    match data {
        Ok(player_summary_map) => {
            // Iterate over the HashMap<String, offense::Summary>
            for (player_name, summary) in player_summary_map.iter() {
                println!("Player: {}", player_name);
                
                super::insert("players", player_name, summary).await?;
            }
        },
        Err(e) => {
            eprintln!("Error fetching league offense data: {}", e);
            // Handle the error as needed
        }
    }

    Ok(())
}