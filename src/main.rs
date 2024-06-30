mod db;
mod nfl;
mod web;

fn main() {
    db::populate::populate_players(2023);
}