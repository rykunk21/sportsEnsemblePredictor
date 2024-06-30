use std::error::Error;

use serde::Deserialize;
use surrealdb::engine::remote::ws::Ws;
use surrealdb::sql::Thing;
use surrealdb::Surreal;
use tokio::task;

use crate::nfl::offense::*;


#[derive(Debug, serde::Serialize)]
struct Entry {
    id: String,
    summary: Summary,
}

#[derive(Debug, Deserialize)]
struct Record {
    #[allow(dead_code)]
    id: Thing,
}

#[tokio::main]
pub async fn run() -> surrealdb::Result<()> {
    // Create database connection
    let db = Surreal::new::<Ws>("127.0.0.1:8000").await?;

    // Select a specific namespace / database
    db.use_ns("sports").use_db("nfl").await?;

    let data = task::spawn_blocking(|| {
        crate::web::teams::get_offense_stats("Patriots", 2023).expect("ERROR IN STATS")

    }).await.unwrap();

    // Create a new person with a random id
    let created: Vec<Record> = db
        .create("offense")
        .content(Entry {
            id: "vikings".to_string(),
            summary: data
        })
        .await?;
    dbg!(created);

    Ok(())
}


mod test {
    use super::*;

    #[test]
    fn test_run() {
        run();
    }
}