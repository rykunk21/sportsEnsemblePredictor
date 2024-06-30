use reqwest::blocking::get;
use select::predicate::Name;
use select::predicate::{Class, Predicate};
use select::{document::Document, node::Node};
use std::collections::HashMap;
use std::error::Error;

//                      //
//  UTILITY  FUNCTIONS  //
//                      //

pub fn parse_table<T, F>(url: &str, from_fn: F) -> Result<HashMap<String, T>, Box<dyn Error>>
where
    F: Fn(&[String]) -> T,
{
    // Get document from source
    let body = get(url)?.text()?;
    let document = Document::from(body.as_str());

    // Define output container
    let mut table_data = HashMap::new();

    // Find the table element and iterate through rows
    for table in document.find(Name("table")) {
        for row in table.find(Name("tr")) {
            let mut row_content = Vec::new();
            for cell in row.find(Name("td")) {
                row_content.push(cell.text().trim().replace("\n", "").replace("  ", " "));
            }

            // Skip empty rows
            if row_content.is_empty() {
                continue;
            }

            // Extract team name and parse stats
            if let Some(first_space_index) = row_content[0].find(' ') {
                let team_name = row_content[0][..first_space_index].trim().to_string();
                let stats: T = from_fn(&row_content[1..]);
                table_data.insert(team_name, stats);
            }
        }
    }

    Ok(table_data)
}

pub fn parse_player_table<T, F>(url: &str, from_fn: F) -> Result<HashMap<String, T>, Box<dyn Error>>
where
    F: Fn(&[String]) -> T,
{
    // Get document from source
    let mut body = get(url)?.text()?;
    let mut document = Document::from(body.as_str());

    let mut table_data = HashMap::new();

    // handle initial pass
    for row in document.find(Name("tr")) {
        // skip empty rows
        if row.find(Name("td")).next().is_none() {
            continue;
        }

        let (player, data) = get_row::<T, F>(&row, &from_fn).unwrap();
        table_data.insert(player, data);
    }

    for _ in 0..6 {
        let next_url = match get_next_page_url(&document) {
            Ok(url) => url,
            Err(_) => break, // Stop if there is no next page
        };

        body = get(&next_url)?.text()?;
        document = Document::from(body.as_str()); // Update the document

        // handle initial pass
        for row in document.find(Name("tr")) {
            // skip empty rows
            if row.find(Name("td")).next().is_none() {
                continue;
            }

            let (player, data) = get_row::<T, F>(&row, &from_fn).unwrap();
            table_data.insert(player, data);
        }
    }

    Ok(table_data)
}

fn get_next_page_url(document: &Document) -> Result<String, Box<dyn Error>> {
    // Find the <a> tag with the class "nfl-o-table-pagination__next"
    if let Some(next_page) = document.find(Class("nfl-o-table-pagination__next")).next() {
        if let Some(href) = next_page.attr("href") {
            return Ok(format!("https://www.nfl.com{}", href));
        }
    }

    Err("Next page URL not found".into())
}

pub fn get_player_team(url: &str) -> Result<Vec<String>, Box<dyn Error>> {
    // Fetch the HTML content from the URL
    // Fetch the HTML content from the URL
    let body = reqwest::blocking::get(url)?.text()?;

    // Parse the document
    let document = Document::from(body.as_str());

    let name = document.find(Class("nfl-c-player-header__title"))
        .next()
        .ok_or_else(|| {
            let err_msg = format!("Failed to find player name at URL: {}", url);
            Box::<dyn Error>::from(err_msg)
        })?
        .text()
        .trim()
        .to_string();

    let position = {
        let position_elem = document.find(Class("nfl-c-player-header__position")).next().unwrap();
        position_elem.text().trim().to_string()
    };

    let number = {
        let number_elem = document.find(Class("nfl-c-player-header__player-data")).next().unwrap();
        let jersey_number = number_elem.text().trim().to_string();
        // Extract the jersey number part (if structured predictably)
        jersey_number.split('\n').last().unwrap_or("").trim().to_string()
    };

    let team = document.find(Class("nfl-c-player-header__team")).next().unwrap().text().trim().to_string();
    let status = document.find(Class("nfl-c-player-header__roster-status")).next().unwrap().text().trim().to_string();

    Ok(vec![name, position, number, team, status])
}

fn get_row<T, F>(row: &Node, from_fn: &F) -> Result<(String, T), Box<dyn Error>>
where
    F: Fn(&[String]) -> T,
{
    // Iterate through each table row
    // get player links
    let mut row_content = Vec::new();
    for cell in row.find(Name("td")) {
        row_content.push(cell.text().trim().replace("\n", "").replace("  ", " "));
    }

    let stats: T = from_fn(&row_content[1..]);

    // Find the anchor tag with class "d3-o-player-fullname"
    if let Some(player_link) = row
        .find(Name("a").and(Class("d3-o-player-fullname")))
        .next()
    {
        // Extract the href attribute value
        if let Some(href) = player_link.attr("href") {
            let href = href
                .strip_prefix("/players/")
                .unwrap_or(href)
                .trim_end_matches('/');

            return Ok((String::from(href), stats));
        } else {
            Err("player link not found".into())
        }
    } else {
        Err("anchor tag with player not found".into())
    }
}

mod test {

    use super::*;

    #[test]
    fn test_get_player_table() {
        let url = "https://www.nfl.com/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc";
        let data = parse_player_table(&url, crate::nfl::players::Rushing::from).unwrap();

        for key in data.keys() {
            println!("{}", key)
        }
    }
}
