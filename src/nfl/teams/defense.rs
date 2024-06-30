use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct Summary {
    pub passing: Passing,
    pub receiving: Receiving,
    pub rushing: Rushing,
    pub scoring: Scoring,
    pub tackles: Tackles,
    pub downs: Downs,
    pub fumbles: Fumbles,
    pub interceptions: Interceptions,
}

#[derive(Debug, Clone, Serialize)]
pub struct Passing {
    att: u32,
    cmp: u32,
    cmp_pct: f32,
    yds_per_att: f32,
    yds: u32,
    td: u32,
    int: u32,
    rate: f32,
    first: u32,
    first_pct: f32,
    twenty_plus: u32,
    fourty_plus: u32,
    lng: u32,
    sck: u32,
}

impl Passing {
    pub fn from(data: &[String]) -> Passing {
        Passing {
            att: data[0].parse().unwrap_or_default(),
            cmp: data[1].parse().unwrap_or_default(),
            cmp_pct: data[2].parse().unwrap_or_default(),
            yds_per_att: data[3].parse().unwrap_or_default(),
            yds: data[4].parse().unwrap_or_default(),
            td: data[5].parse().unwrap_or_default(),
            int: data[6].parse().unwrap_or_default(),
            rate: data[7].parse().unwrap_or_default(),
            first: data[8].parse().unwrap_or_default(),
            first_pct: data[9].parse().unwrap_or_default(),
            twenty_plus: data[10].parse().unwrap_or_default(),
            fourty_plus: data[11].parse().unwrap_or_default(),
            lng: data[12].parse().unwrap_or_default(),
            sck: data[13].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Rushing {
    att: u32,
    yds: u32,
    yards_per_carry: f32,
    td: u32,
    twenty_plus: u32,
    fourty_plus: u32,
    lng: u32,
    rush_first: u32,
    rush_first_pct: f32,
    fum: u32,
}

impl Rushing {
    pub fn from(data: &[String]) -> Rushing {
        Rushing {
            att: data[0].parse().unwrap_or_default(),
            yds: data[1].parse().unwrap_or_default(),
            yards_per_carry: data[2].parse().unwrap_or_default(),
            td: data[3].parse().unwrap_or_default(),
            twenty_plus: data[4].parse().unwrap_or_default(),
            fourty_plus: data[5].parse().unwrap_or_default(),
            lng: data[6].parse().unwrap_or_default(),
            rush_first: data[7].parse().unwrap_or_default(),
            rush_first_pct: data[8].parse().unwrap_or_default(),
            fum: data[9].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Receiving {
    rec: u32,
    yds: u32,
    yds_per_rec: f32,
    td: u32,
    twenty_plus: u32,
    fourty_plus: u32,
    lng: u32,
    rec_first: u32,
    rec_first_pct: f32,
    fum: u32,
    pdef: u32,
}

impl Receiving {
    pub fn from(data: &[String]) -> Receiving {
        Receiving {
            rec: data[0].parse().unwrap_or_default(),
            yds: data[1].parse().unwrap_or_default(),
            yds_per_rec: data[2].parse().unwrap_or_default(),
            td: data[3].parse().unwrap_or_default(),
            twenty_plus: data[4].parse().unwrap_or_default(),
            fourty_plus: data[5].parse().unwrap_or_default(),
            lng: data[6].parse().unwrap_or_default(),
            rec_first: data[7].parse().unwrap_or_default(),
            rec_first_pct: data[8].parse().unwrap_or_default(),
            fum: data[9].parse().unwrap_or_default(),
            pdef: data[10].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Scoring {
    fr_td: u32,
    safety: u32,
    int_td: u32,
}

impl Scoring {
    pub fn from(data: &[String]) -> Scoring {
        Scoring {
            fr_td: data[0].parse().unwrap_or_default(),
            safety: data[1].parse().unwrap_or_default(),
            int_td: data[2].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Tackles {
    sck: u32,
    comb: u32,
    asst: u32,
    solo: u32,
}

impl Tackles {
    pub fn from(data: &[String]) -> Tackles {
        Tackles {
            sck: data[0].parse().unwrap_or_default(),
            comb: data[1].parse().unwrap_or_default(),
            asst: data[2].parse().unwrap_or_default(),
            solo: data[3].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Downs {
    third_att: u32,
    third_md: u32,
    fourth_att: u32,
    fourth_md: u32,
    rec_first: u32,
    rec_first_pct: f32,
    rush_first: u32,
    rush_first_pct: f32,
    scrm_plays: u32,
}

impl Downs {
    pub fn from(data: &[String]) -> Downs {
        Downs {
            third_att: data[0].parse().unwrap_or_default(),
            third_md: data[1].parse().unwrap_or_default(),
            fourth_att: data[2].parse().unwrap_or_default(),
            fourth_md: data[3].parse().unwrap_or_default(),
            rec_first: data[4].parse().unwrap_or_default(),
            rec_first_pct: data[5].parse().unwrap_or_default(),
            rush_first: data[6].parse().unwrap_or_default(),
            rush_first_pct: data[7].parse().unwrap_or_default(),
            scrm_plays: data[8].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Fumbles {
    ff: u32,
    fr: u32,
    fr_td: u32,
    rec_fum: u32,
    rush_fum: u32,
}

impl Fumbles {
    pub fn from(data: &[String]) -> Fumbles {
        Fumbles {
            ff: data[0].parse().unwrap_or_default(),
            fr: data[1].parse().unwrap_or_default(),
            fr_td: data[2].parse().unwrap_or_default(),
            rec_fum: data[3].parse().unwrap_or_default(),
            rush_fum: data[4].parse().unwrap_or_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Interceptions {
    int: u32,
    int_td: u32,
    int_yds: u32,
    lng: u32,
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
