use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct Summary {
    pub passing: Passing,
    pub rushing: Rushing,
    pub receiving: Receiving,
    pub scoring: Scoring,
}

#[derive(Debug, Clone, Serialize)]
pub struct Passing {
    // relevant fields for a particular nfl teams offensive stats
    pub att: u32,
    pub cmp: u32,
    pub cmp_pct: f32,
    pub yds_per_att: f32,
    pub yds: u32,
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
        let att = data[0].parse().unwrap_or_default();
        let cmp = data[1].parse().unwrap_or_default();
        let cmp_pct = data[2].parse().unwrap_or_default();
        let yds_per_att = data[3].parse().unwrap_or_default();
        let yds = data[4].parse().unwrap_or_default();
        let td = data[5].parse().unwrap_or_default();
        let int = data[6].parse().unwrap_or_default();
        let rate = data[7].parse().unwrap_or_default();
        let first = data[8].parse().unwrap_or_default();
        let first_pct = data[9].parse().unwrap_or_default();
        let twenty_plus = data[10].parse().unwrap_or_default();
        let fourty_plus = data[11].parse().unwrap_or_default();
        let lng = data[12].parse().unwrap_or_default();
        let sck = data[13].parse().unwrap_or_default();
        let sck_yards = data[14].parse().unwrap_or_default();

        // Create a Passing struct instance
        Passing {
            att,
            cmp,
            cmp_pct,
            yds_per_att,
            yds,
            td,
            int,
            rate,
            first,
            first_pct,
            twenty_plus,
            fourty_plus,
            lng,
            sck,
            sck_yards,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Rushing {
    pub att: u32,
    pub yds: u32,
    pub yards_per_carry: f32,
    pub td: u32,
    pub twenty_plus: u32,
    pub fourty_plus: u32,
    pub lng: u32,
    pub rush_first: u32,
    pub rush_first_pct: f32,
    pub fum: u32,
}

impl Rushing {
    pub fn from(data: &[String]) -> Rushing {
        let att = data[0].parse().unwrap_or_default();
        let yds = data[1].parse().unwrap_or_default();
        let yards_per_carry = data[2].parse().unwrap_or_default();
        let td = data[3].parse().unwrap_or_default();
        let twenty_plus = data[4].parse().unwrap_or_default();
        let fourty_plus = data[5].parse().unwrap_or_default();
        let lng = data[6].parse().unwrap_or_default();
        let rush_first = data[7].parse().unwrap_or_default();
        let rush_first_pct = data[8].parse().unwrap_or_default();
        let fum = data[9].parse().unwrap_or_default();

        Rushing {
            att,
            yds,
            yards_per_carry,
            td,
            twenty_plus,
            fourty_plus,
            lng,
            rush_first,
            rush_first_pct,
            fum,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Receiving {
    pub rec: u32,
    pub yds: u32,
    pub yds_per_rec: f32,
    pub td: u32,
    pub twenty_plus: u32,
    pub fourty_plus: u32,
    pub lng: u32,
    pub rec_first: u32,
    pub rec_first_pct: f32,
    pub fum: u32,
}

impl Receiving {
    pub fn from(data: &[String]) -> Receiving {
        let rec = data[0].parse().unwrap_or_default();
        let yds = data[1].parse().unwrap_or_default();
        let yds_per_rec = data[2].parse().unwrap_or_default();
        let td = data[3].parse().unwrap_or_default();
        let twenty_plus = data[4].parse().unwrap_or_default();
        let fourty_plus = data[5].parse().unwrap_or_default();
        let lng = data[6].parse().unwrap_or_default();
        let rec_first = data[7].parse().unwrap_or_default();
        let rec_first_pct = data[8].parse().unwrap_or_default();
        let fum = data[9].parse().unwrap_or_default();

        Receiving {
            rec,
            yds,
            yds_per_rec,
            td,
            twenty_plus,
            fourty_plus,
            lng,
            rec_first,
            rec_first_pct,
            fum,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Scoring {
    pub rsh_td: u32,
    pub rec_td: u32,
    pub total_td: u32,
    pub two_pt: u32,
}

impl Scoring {
    pub fn from(data: &[String]) -> Scoring {
        let rsh_td = data[0].parse().unwrap_or_default();
        let rec_td = data[1].parse().unwrap_or_default();
        let total_td = data[2].parse().unwrap_or_default();
        let two_pt = data[3].parse().unwrap_or_default();

        Scoring {
            rsh_td,
            rec_td,
            total_td,
            two_pt,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Downs {
    pub third_att: u32,
    pub third_md: u32,
    pub fourth_att: u32,
    pub fourth_md: u32,
    pub rec_first: u32,
    pub rec_first_pct: f32,
    pub rush_first: u32,
    pub rush_first_pct: f32,
    pub scrm_plays: u32,
}

impl Downs {
    pub fn from(data: &[String]) -> Downs {
        let third_att = data[0].parse().unwrap_or_default();
        let third_md = data[1].parse().unwrap_or_default();
        let fourth_att = data[2].parse().unwrap_or_default();
        let fourth_md = data[3].parse().unwrap_or_default();
        let rec_first = data[4].parse().unwrap_or_default();
        let rec_first_pct = data[5].parse().unwrap_or_default();
        let rush_first = data[6].parse().unwrap_or_default();
        let rush_first_pct = data[7].parse().unwrap_or_default();
        let scrm_plays = data[8].parse().unwrap_or_default();

        Downs {
            third_att,
            third_md,
            fourth_att,
            fourth_md,
            rec_first,
            rec_first_pct,
            rush_first,
            rush_first_pct,
            scrm_plays,
        }
    }
}
