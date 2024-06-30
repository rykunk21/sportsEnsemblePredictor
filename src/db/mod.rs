pub mod example;
pub mod populate;

use serde::{Deserialize, Serialize};
use surrealdb::engine::remote::ws::{Client, Ws};
use surrealdb::sql::Thing;
use surrealdb::Surreal;

use crate::nfl::*;

#[derive(Debug, Serialize)]
struct Entry<T> {
    id: String,
    data: T
}

#[derive(Debug, Deserialize)]
struct Record {
    #[allow(dead_code)]
    id: Thing,
}
async fn conn() -> Result<Surreal<Client>, surrealdb::Error> {
    // Create database connection
    let db = Surreal::new::<Ws>("127.0.0.1:8000").await?;

    // Select a specific namespace / database
    db.use_ns("sports").use_db("nfl").await?;
    Ok(db)
}

pub async fn insert<T>(table: &str, id: &str, data: T) -> surrealdb::Result<()>
where
    T: serde::Serialize,
{
    // Explicitly handle the error conversion
    let db = conn().await?;

    let entry = Entry{id: id.to_string(), data};

    let created: Vec<Record> = db.create(table).content(entry).await?;

    if created.is_empty() {
        panic!("Failed to insert data into table '{}'", table);
    }

    dbg!(created);

    Ok(())
}
