use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
pub struct Summary {
    pub field_goals: FieldGoals,
    pub scoring: Scoring,
    pub kickoffs: Kickoffs,
    pub kickoff_returns: KickoffReturns,
    pub punting: Punting,
    pub punt_returns: PuntReturns,
}

#[derive(Debug, Clone, Serialize)]
struct A_M(u32, u32);

fn parse_a_m(data: &String) -> A_M {
    let parts: Vec<u32> = data
        .split('_')
        .map(|s| s.parse().unwrap_or_default())
        .collect();
    A_M(parts[0], parts[1])
}

#[derive(Debug, Clone, Serialize)]
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

#[derive(Debug, Clone, Serialize)]
pub struct Scoring {
    fgm: u32,
    fg_pct: f32,
    xpm: u32,
    xp_pct: f32,
    kret_td: u32,
    pret_t: u32,
}

impl Scoring {
    pub fn from(data: &[String]) -> Scoring {
        let fgm = data[0].parse().unwrap_or_default();
        let fg_pct = data[1].parse().unwrap_or_default();
        let xpm = data[2].parse().unwrap_or_default();
        let xp_pct = data[3].parse().unwrap_or_default();
        let kret_td = data[4].parse().unwrap_or_default();
        let pret_t = data[5].parse().unwrap_or_default();

        Scoring {
            fgm,
            fg_pct,
            xpm,
            xp_pct,
            kret_td,
            pret_t,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Kickoffs {
    ko: u32,
    yds: u32,
    tb: u32,
    tb_pct: f32,
    ret: u32,
    ret_avg: f32,
    osk: u32,
    osk_rec: u32,
    oob: u32,
    td: u32,
}

impl Kickoffs {
    pub fn from(data: &[String]) -> Kickoffs {
        let ko = data[0].parse().unwrap_or_default();
        let yds = data[1].parse().unwrap_or_default();
        let tb = data[2].parse().unwrap_or_default();
        let tb_pct = data[3].parse().unwrap_or_default();
        let ret = data[4].parse().unwrap_or_default();
        let ret_avg = data[5].parse().unwrap_or_default();
        let osk = data[6].parse().unwrap_or_default();
        let osk_rec = data[7].parse().unwrap_or_default();
        let oob = data[8].parse().unwrap_or_default();
        let td = data[9].parse().unwrap_or_default();

        Kickoffs {
            ko,
            yds,
            tb,
            tb_pct,
            ret,
            ret_avg,
            osk,
            osk_rec,
            oob,
            td,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct KickoffReturns {
    avg: f32,
    ret: u32,
    yds: u32,
    ret_td: u32,
    twenty_plus: u32,
    fourty_plus: u32,
    lng: u32,
    fc: u32,
    fum: u32,
    fg_blk: u32,
    xp_blk: u32,
}

impl KickoffReturns {
    pub fn from(data: &[String]) -> KickoffReturns {
        let avg = data[0].parse().unwrap_or_default();
        let ret = data[1].parse().unwrap_or_default();
        let yds = data[2].parse().unwrap_or_default();
        let ret_td = data[3].parse().unwrap_or_default();
        let twenty_plus = data[4].parse().unwrap_or_default();
        let fourty_plus = data[5].parse().unwrap_or_default();
        let lng = data[6].parse().unwrap_or_default();
        let fc = data[7].parse().unwrap_or_default();
        let fum = data[8].parse().unwrap_or_default();
        let fg_blk = data[9].parse().unwrap_or_default();
        let xp_blk = data[10].parse().unwrap_or_default();

        KickoffReturns {
            avg,
            ret,
            yds,
            ret_td,
            twenty_plus,
            fourty_plus,
            lng,
            fc,
            fum,
            fg_blk,
            xp_blk,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Punting {
    net_avg: f32,
    net_yds: u32,
    punts: u32,
    avg: f32,
    lng: u32,
    yds: u32,
    in_twenty: u32,
    oob: u32,
    dn: u32,
    tb: u32,
    fc: u32,
    ret: u32,
    ret_yds: u32,
    td: u32,
    p_blk: u32,
}

impl Punting {
    pub fn from(data: &[String]) -> Punting {
        let net_avg = data[0].parse().unwrap_or_default();
        let net_yds = data[1].parse().unwrap_or_default();
        let punts = data[2].parse().unwrap_or_default();
        let avg = data[3].parse().unwrap_or_default();
        let lng = data[4].parse().unwrap_or_default();
        let yds = data[5].parse().unwrap_or_default();
        let in_twenty = data[6].parse().unwrap_or_default();
        let oob = data[7].parse().unwrap_or_default();
        let dn = data[8].parse().unwrap_or_default();
        let tb = data[9].parse().unwrap_or_default();
        let fc = data[10].parse().unwrap_or_default();
        let ret = data[11].parse().unwrap_or_default();
        let ret_yds = data[12].parse().unwrap_or_default();
        let td = data[13].parse().unwrap_or_default();
        let p_blk = data[14].parse().unwrap_or_default();

        Punting {
            net_avg,
            net_yds,
            punts,
            avg,
            lng,
            yds,
            in_twenty,
            oob,
            dn,
            tb,
            fc,
            ret,
            ret_yds,
            td,
            p_blk,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct PuntReturns {
    avg: f32,
    ret: u32,
    yds: u32,
    pret_tot: u32,
    twenty_plus: u32,
    fourty_plus: u32,
    lng: u32,
    fc: u32,
    fum: u32,
    p_blk: u32,
}

impl PuntReturns {
    pub fn from(data: &[String]) -> PuntReturns {
        let avg = data[0].parse().unwrap_or_default();
        let ret = data[1].parse().unwrap_or_default();
        let yds = data[2].parse().unwrap_or_default();
        let pret_tot = data[3].parse().unwrap_or_default();
        let twenty_plus = data[4].parse().unwrap_or_default();
        let fourty_plus = data[5].parse().unwrap_or_default();
        let lng = data[6].parse().unwrap_or_default();
        let fc = data[7].parse().unwrap_or_default();
        let fum = data[8].parse().unwrap_or_default();
        let p_blk = data[9].parse().unwrap_or_default();

        PuntReturns {
            avg,
            ret,
            yds,
            pret_tot,
            twenty_plus,
            fourty_plus,
            lng,
            fc,
            fum,
            p_blk,
        }
    }
}
