use std::{clone, error::Error};

use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct Player {
    pub name: String,
    pub jersey_num: u8,
    pub team: String, // Store team ID
    pub status: String,
    pub position: Position,
    pub stats: Summary,
}

#[derive(Debug, Clone, Serialize)]
pub enum Position {
    QB,
    WR,
    RB,
    TE,
    DB,
    LB,
    LS,
    P,
    H,
    CB,
    DE,
    NT,
    DT,
    K,
    S,

}

impl Position {
    pub fn from(pos: &str) -> Result<Position, Box<dyn Error>> {
        match pos {
            "QB" => Ok(Position::QB),
            "WR" => Ok(Position::WR),
            "HB" | "FB" | "RB" => Ok(Position::RB),
            "DB" => Ok(Position::DB),
            "NT" => Ok(Position::NT),
            "TE" => Ok(Position::TE),
            "DE" => Ok(Position::DE),
            "DT" => Ok(Position::DT),
            "CB" => Ok(Position::CB),
            "K" => Ok(Position::K),
            "LS" => Ok(Position::LS),
            "H" => Ok(Position::H),
            "P" => Ok(Position::P),
            "LB" | "OLB" | "MLB" | "ILB" => Ok(Position::LB),
            "FS" | "SAF" | "S" => Ok(Position::S),
            
            _ => Err(format!("No position match for '{}'", pos).into()), // Error handling for unmatched position
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Summary {
    pub passing: Passing,
    pub rushing: Rushing,
    pub receiving: Receiving,
    pub fumbles: Fumbles,
    pub tackles: Tackles,
    pub interceptions: Interceptions,
    pub field_goals: FieldGoals,
    pub kickoffs: Kickoffs,
    pub kickoff_returns: KickoffReturns,
    pub punting: Punting,
    pub punt_returns: PuntReturns,
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Passing {
    pub pass_yds: u32,
    pub yds_per_att: f32,
    pub att: u32,
    pub cmp: u32,
    pub cmp_pct: f32,
    pub td: u32,
    pub int: u32,
    pub rate: f32,
    pub first: u32,
    pub first_pct: f32,
    pub twenty_plus: u32,
    pub fourty_plus: u32,
    pub lng: u32,
    pub sck: u32,
    pub sck_yards: u32,
}

impl Passing {
    pub fn from(data: &[String]) -> Passing {
        Passing {
            pass_yds: data[0].parse().unwrap_or_default(),
            yds_per_att: data[1].parse().unwrap_or_default(),
            att: data[2].parse().unwrap_or_default(),
            cmp: data[3].parse().unwrap_or_default(),
            cmp_pct: data[4].parse().unwrap_or_default(),
            td: data[5].parse().unwrap_or_default(),
            int: data[6].parse().unwrap_or_default(),
            rate: data[7].parse().unwrap_or_default(),
            first: data[8].parse().unwrap_or_default(),
            first_pct: data[9].parse().unwrap_or_default(),
            twenty_plus: data[10].parse().unwrap_or_default(),
            fourty_plus: data[11].parse().unwrap_or_default(),
            lng: data[12].parse().unwrap_or_default(),
            sck: data[13].parse().unwrap_or_default(),
            sck_yards: data[14].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Rushing {
    pub rush_yds: u32,
    pub att: u32,
    pub td: u32,
    pub twenty_plus: u32,
    pub fourty_plus: u32,
    pub lng: u32,
    pub rush_first: u32,
    pub rush_first_pct: f32,
    pub rush_fum: u32,
}

impl Rushing {
    pub fn from(data: &[String]) -> Rushing {
        Rushing {
            rush_yds: data[0].parse().unwrap_or_default(),
            att: data[1].parse().unwrap_or_default(),
            td: data[2].parse().unwrap_or_default(),
            twenty_plus: data[3].parse().unwrap_or_default(),
            fourty_plus: data[4].parse().unwrap_or_default(),
            lng: data[5].parse().unwrap_or_default(),
            rush_first: data[6].parse().unwrap_or_default(),
            rush_first_pct: data[7].parse().unwrap_or_default(),
            rush_fum: data[8].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Receiving {
    pub rec: u32,
    pub rec_yds: u32,
    pub td: u32,
    pub twenty_plus: u32,
    pub fourty_plus: u32,
    pub lng: u32,
    pub rec_first: u32,
    pub first_pct: f32,
    pub rec_fum: u32,
    pub rec_yac_per_rec: f32,
    pub tgts: u32,
}

impl Receiving {
    pub fn from(data: &[String]) -> Receiving {
        Receiving {
            rec: data[0].parse().unwrap_or_default(),
            rec_yds: data[1].parse().unwrap_or_default(),
            td: data[2].parse().unwrap_or_default(),
            twenty_plus: data[3].parse().unwrap_or_default(),
            fourty_plus: data[4].parse().unwrap_or_default(),
            lng: data[5].parse().unwrap_or_default(),
            rec_first: data[6].parse().unwrap_or_default(),
            first_pct: data[7].parse().unwrap_or_default(),
            rec_fum: data[8].parse().unwrap_or_default(),
            rec_yac_per_rec: data[9].parse().unwrap_or_default(),
            tgts: data[10].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Fumbles {
    pub ff: u32,
    pub fr: u32,
    pub fr_td: u32,
}

impl Fumbles {
    pub fn from(data: &[String]) -> Fumbles {
        Fumbles {
            ff: data[0].parse().unwrap_or_default(),
            fr: data[1].parse().unwrap_or_default(),
            fr_td: data[2].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Tackles {
    pub comb: u32,
    pub asst: u32,
    pub solo: u32,
    pub sck: f32, // Assuming `Sck` represents sacks and could be a float
}

impl Tackles {
    pub fn from(data: &[String]) -> Tackles {
        Tackles {
            comb: data[0].parse().unwrap_or_default(),
            asst: data[1].parse().unwrap_or_default(),
            solo: data[2].parse().unwrap_or_default(),
            sck: data[3].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Interceptions {
    pub int: u32,
    pub int_td: u32,
    pub int_yds: u32,
    pub lng: u32,
}
impl Interceptions {
    pub fn from(data: &[String]) -> Interceptions {
        Interceptions {
            int: data[0].parse().unwrap_or_default(),
            int_td: data[1].parse().unwrap_or_default(),
            int_yds: data[2].parse().unwrap_or_default(),
            lng: data[3].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct A_M(u32, u32);

fn parse_a_m(data: &String) -> A_M {
    let parts: Vec<u32> = data
        .split('/')
        .map(|s| s.parse().unwrap_or_default())
        .collect();
    A_M(parts[0], parts[1])
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct FieldGoals {
    fgm: u32,
    att: u32,
    fg_pct: f32,
    fg_A: A_M,
    fg_B: A_M,
    fg_C: A_M,
    fg_D: A_M,
    fg_E: A_M,
    fg_F: A_M,
    lng: u32,
    fg_blk: u32,
}

impl FieldGoals {
    pub fn from(data: &[String]) -> FieldGoals {
        let fgm = data[0].parse().unwrap_or_default();
        let att = data[1].parse().unwrap_or_default();
        let fg_pct = data[2].parse().unwrap_or_default();
        let fg_A = parse_a_m(&data[3]);
        let fg_B = parse_a_m(&data[4]);
        let fg_C = parse_a_m(&data[5]);
        let fg_D = parse_a_m(&data[6]);
        let fg_E = parse_a_m(&data[7]);
        let fg_F = parse_a_m(&data[8]);
        let lng = data[9].parse().unwrap_or_default();
        let fg_blk = data[10].parse().unwrap_or_default();

        FieldGoals {
            fgm,
            att,
            fg_pct,
            fg_A,
            fg_B,
            fg_C,
            fg_D,
            fg_E,
            fg_F,
            lng,
            fg_blk,
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Kickoffs {
    pub ko: u32,
    pub yds: u32,
    pub ret_yds: u32,
    pub tb: u32,
    pub tb_pct: f32,
    pub ret: u32,
    pub ret_avg: f32,
    pub osk: u32,
    pub osk_rec: u32,
    pub oob: u32,
    pub td: u32,
}
impl Kickoffs {
    pub fn from(data: &[String]) -> Kickoffs {
        Kickoffs {
            ko: data[0].parse().unwrap_or_default(),
            yds: data[1].parse().unwrap_or_default(),
            ret_yds: data[2].parse().unwrap_or_default(),
            tb: data[3].parse().unwrap_or_default(),
            tb_pct: data[4].parse().unwrap_or_default(),
            ret: data[5].parse().unwrap_or_default(),
            ret_avg: data[6].parse().unwrap_or_default(),
            osk: data[7].parse().unwrap_or_default(),
            osk_rec: data[8].parse().unwrap_or_default(),
            oob: data[9].parse().unwrap_or_default(),
            td: data[10].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct KickoffReturns {
    pub avg: f32,
    pub ret: u32,
    pub yds: u32,
    pub kret_td: u32,
    pub twenty_plus: u32,
    pub forty_plus: u32,
    pub lng: u32,
    pub fc: u32,
    pub fum: u32,
}
impl KickoffReturns {
    pub fn from(data: &[String]) -> KickoffReturns {
        KickoffReturns {
            avg: data[0].parse().unwrap_or_default(),
            ret: data[1].parse().unwrap_or_default(),
            yds: data[2].parse().unwrap_or_default(),
            kret_td: data[3].parse().unwrap_or_default(),
            twenty_plus: data[4].parse().unwrap_or_default(),
            forty_plus: data[5].parse().unwrap_or_default(),
            lng: data[6].parse().unwrap_or_default(),
            fc: data[7].parse().unwrap_or_default(),
            fum: data[8].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct Punting {
    pub avg: f32,
    pub net_avg: f32,
    pub net_yds: u32,
    pub punts: u32,
    pub lng: u32,
    pub yds: u32,
    pub in_20: u32,
    pub oob: u32,
    pub dn: u32,
    pub tb: u32,
    pub fc: u32,
    pub ret: u32,
    pub ret_yds: u32,
    pub td: u32,
    pub p_blk: u32,
}
impl Punting {
    pub fn from(data: &[String]) -> Punting {
        Punting {
            avg: data[0].parse().unwrap_or_default(),
            net_avg: data[1].parse().unwrap_or_default(),
            net_yds: data[2].parse().unwrap_or_default(),
            punts: data[3].parse().unwrap_or_default(),
            lng: data[4].parse().unwrap_or_default(),
            yds: data[5].parse().unwrap_or_default(),
            in_20: data[6].parse().unwrap_or_default(),
            oob: data[7].parse().unwrap_or_default(),
            dn: data[8].parse().unwrap_or_default(),
            tb: data[9].parse().unwrap_or_default(),
            fc: data[10].parse().unwrap_or_default(),
            ret: data[11].parse().unwrap_or_default(),
            ret_yds: data[12].parse().unwrap_or_default(),
            td: data[13].parse().unwrap_or_default(),
            p_blk: data[14].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct PuntReturns {
    pub avg: f32,
    pub ret: u32,
    pub yds: u32,
    pub pret_td: u32,
    pub twenty_plus: u32,
    pub forty_plus: u32,
    pub lng: u32,
    pub fc: u32,
    pub fum: u32,
}
impl PuntReturns {
    pub fn from(data: &[String]) -> PuntReturns {
        PuntReturns {
            avg: data[0].parse().unwrap_or_default(),
            ret: data[1].parse().unwrap_or_default(),
            yds: data[2].parse().unwrap_or_default(),
            pret_td: data[3].parse().unwrap_or_default(),
            twenty_plus: data[4].parse().unwrap_or_default(),
            forty_plus: data[5].parse().unwrap_or_default(),
            lng: data[6].parse().unwrap_or_default(),
            fc: data[7].parse().unwrap_or_default(),
            fum: data[8].parse().unwrap_or_default(),
        }
    }
}
