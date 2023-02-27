// Calculate bus factor score based on the bus factor and number of contributors
use octocrab::Octocrab;
use serde::Deserialize;
use std::fs::File; //rust file library
use std::io::BufWriter;
use std::io::Write;
use std::sync::Arc; //rust write library
use std::fs;


pub fn bus_factor_score(filepath: &str) {
    //simple_log::info!("Calculating Bus Factor Score.)");

    let token = std::env::var("GITHUB_TOKEN");
    let octocrab = match token {
        Ok(t) => {
            //simple_log::debug!("BF Score: Used Github token.)");
            Arc::new(Octocrab::builder().personal_token(t).build().unwrap())
        }
        Err(_e) => {
            //simple_log::debug!("BF Score: Did not use Github token.");
            octocrab::instance()
        }
    };

    let urls = get_urls(filepath);
    let mut out_file =
        BufWriter::new(File::create("output/bus_factor_out.txt").expect("Error creating output file!"));

    for url in &urls {
        let git_url;
        if &url[0..22] == "https://www.npmjs.com/" {
         git_url = get_github_url_for_npm(&url).unwrap();
        }
        else {
            git_url = url.to_string();
        }
        let keywords = get_keywords(&git_url);
        let score = find_bf_score(&octocrab, keywords);
        write!(out_file, "{0}\n", score).expect("Error writing rampup to output");
    }

}

fn get_urls(filepath: &str) -> Vec<String> {
    let data = match fs::read_to_string(filepath) {
        Ok(data) => data,
        Err(..) => {
            println!("Error reading the input file!\n");
            std::process::exit(1);
        }
    };

    let urls: Vec<&str> = data.split('\n').collect();
    let mut url_vec = Vec::new();
    for url in urls {
        url_vec.push(url.to_string());
    }
    url_vec
}

#[tokio::main]
async fn find_bf_score(octocrab: &Octocrab, (owner, repo): (&str, &str)) -> f32 {
    let repo = octocrab.repos(owner, repo).get().await.unwrap();

    let url = repo.contributors_url.unwrap();
    let path = url.path();

    let user_info: Vec<Contributor> = octocrab.get(path, None::<&str>).await.unwrap();
    //simple_log::debug!("contents = {:?}", user_info);
    let num_contributors = user_info.len() as f32;

    let mut total_contributions = 0;
    for structure in &user_info {
        total_contributions += structure.contributions;
    }

    let mut contributions = 0;
    let mut bus_factor = 0;
    while contributions < (total_contributions / 2) {
        contributions += user_info[bus_factor].contributions;
        bus_factor += 1;
    }
    //simple_log::info!("bus factor = {}", bus_factor);
    normalize_score(num_contributors, (bus_factor + 1) as f32)
}

fn normalize_score(num_contributors: f32, bus_factor: f32) -> f32 {
    let bus_factor_norm = f32::exp(-0.25 * bus_factor);
    let length_norm = f32::exp(-0.1 * num_contributors);
    bus_factor_norm * 0.8 + length_norm * 0.3
}
fn get_keywords(_url: &str) -> (&str, &str) {
    let part_str = &_url[19..];
    let divisionidx = part_str.find("/").expect("Error getting keywords");
    let owner = &part_str[..divisionidx];
    let repo = &part_str[divisionidx + 1..];

    (owner, repo)
}

fn get_github_url_for_npm(npm_url: &str) -> Result<String, ureq::Error> {
    let url = format!("https://registry.npmjs.org/{}", &npm_url[30..]);
    let json: serde_json::Value = ureq::get(&url).call()?.into_json()?;
    let repo_info = &json["repository"];

    if repo_info["type"] == "git" {
        let mut github_url = repo_info["url"].as_str().unwrap()[4..].to_string();
        if &github_url[..10] == "ssh://git@" {
            github_url = github_url[10..].to_string();
            github_url = format!("https://{github_url}");
        }
        else if &github_url[..2] == "//" {
            github_url = format!("https:{github_url}");
        }
        for _i in 1..5 {
            github_url.pop();
        }
        return Ok(github_url);
    } else {
        return Ok("".to_string());
    }
}

#[allow(unused)]
#[derive(Deserialize, Debug)]
struct Contributor {
    login: String,
    id: i32,
    node_id: String,
    avatar_url: String,
    gravatar_id: String,
    url: String,
    html_url: String,
    followers_url: String,
    following_url: String,
    gists_url: String,
    starred_url: String,
    subscriptions_url: String,
    organizations_url: String,
    repos_url: String,
    events_url: String,
    received_events_url: String,
    #[serde(rename = "type")]
    contributor_type: String,
    site_admin: bool,
    contributions: i32,
}
