// Calculate bus factor score based on the bus factor and number of contributors
use octocrab::Octocrab;
use serde::Deserialize;
use std::fs;
use std::fs::File; //rust file library
use std::io::BufWriter;
use std::io::Write;
use std::sync::Arc; //rust write library

pub fn bus_factor_score(filepath: &str) {
    simple_log::info!("Calculating Bus Factor Score.)");

    let token = std::env::var("GITHUB_TOKEN");
    let octocrab = match token {
        Ok(t) => {
            simple_log::debug!("BF Score: Used Github token.)");
            Arc::new(Octocrab::builder().personal_token(t).build().unwrap())
        }
        Err(_e) => {
            simple_log::debug!("BF Score: Did not use Github token.");
            octocrab::instance()
        }
    };

    // Get the urls from the input file
    let urls = get_urls(filepath);

    // Create the output file
    let mut out_file = BufWriter::new(
        File::create("output/bus_factor_out.txt").expect("Error creating output file!"),
    );

    // Iterate through the urls and calculate the bus factor score
    for url in &urls {
        let git_url;

        // If the url is from npm, get the github url
        //log url
        simple_log::info!("url = {}", url);
        if &url[0..22] == "https://www.npmjs.com/" {
            git_url = get_github_url_for_npm(&url).unwrap();
        } else {
            git_url = url.to_string();
        }

        // Get the keywords from the url in the form (owner, repo)
        let keywords = get_keywords(&git_url);

        // Calculate the bus factor score
        let score = find_bf_score(&octocrab, keywords);

        // Write the score to the output file
        write!(out_file, "{0}\n", score).expect("Error writing bus factor to output");
    }
}

// Function to get the urls from the input file
pub fn get_urls(filepath: &str) -> Vec<String> {
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

// Function to calculate the bus factor score
#[tokio::main]
async fn find_bf_score(octocrab: &Octocrab, (owner, repo): (&str, &str)) -> f32 {
    // Get the repo information using octocrab
    let repo = octocrab.repos(owner, repo).get().await.unwrap();

    let url = repo.contributors_url.unwrap();
    let path = url.path();

    // Get the contributor information using http request (through octocrab)
    let user_info: Vec<Contributor> = octocrab.get(path, None::<&str>).await.unwrap();
    simple_log::debug!("contents = {:?}", user_info);

    // Get the number of contributors
    let num_contributors = user_info.len() as f32;

    // Calculate the bus factor
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
    simple_log::info!("bus factor = {}", bus_factor);
    // Normalize the bus factor score
    normalize_score(num_contributors, (bus_factor + 1) as f32)
}

// Function to normalize the bus factor score
fn normalize_score(num_contributors: f32, bus_factor: f32) -> f32 {
    let bus_factor_norm = f32::exp(-0.25 * bus_factor);
    let length_norm = f32::exp(-0.1 * num_contributors);
    bus_factor_norm * 0.8 + length_norm * 0.3
}

// Function to get the keywords from the url
pub fn get_keywords(_url: &str) -> (&str, &str) {
    let part_str = &_url[19..];
    let divisionidx = part_str.find("/").expect("Error getting keywords");
    let owner = &part_str[..divisionidx];
    let repo = &part_str[divisionidx + 1..];

    (owner, repo)
}

// Function to get the github url from the npm url
pub fn get_github_url_for_npm(npm_url: &str) -> Result<String, ureq::Error> {
    let url = format!("https://registry.npmjs.org/{}", &npm_url[30..]);
    let json: serde_json::Value = ureq::get(&url).call()?.into_json()?;
    let repo_info = &json["repository"];

    if repo_info["type"] == "git" {
        let mut github_url = repo_info["url"].as_str().unwrap()[4..].to_string();
        if &github_url[..10] == "ssh://git@" {
            github_url = github_url[10..].to_string();
            github_url = format!("https://{github_url}");
        } else if &github_url[..2] == "//" {
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

// Struct to hold the contributor information
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


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_normalize_score() {
        let result = normalize_score(1.0, 1.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.89);

        let result = normalize_score(1.0, 2.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.76);

        let result = normalize_score(0.0, 0.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 1.1);

        let result = normalize_score(0.0, 1.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.92);

        let result = normalize_score(0.0, 2.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.79);

        let result = normalize_score(1.0, 0.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 1.07);

        let result = normalize_score(2.0, 0.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 1.05);

        let result = normalize_score(3.0, 0.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 1.02);
    }

    #[test]
    fn test_normalize_score2() {
        let result = normalize_score(5.0, 5.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.41);

        let result = normalize_score(0.0, 1000000.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.3);

        let result = normalize_score(1000000.0, 0.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.8);

        let result = normalize_score(1000000.0, 1000000.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.0);

        let result = normalize_score(100000000.0,10000.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.0);

        let result = normalize_score(2.0,1.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.87);

        let result = normalize_score(1.234,5.678);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 0.46);

        let result = normalize_score(1.234,0.0);
        let round_res = (result * 100.0).round() / 100.0;
        assert_eq!(round_res, 1.07);

    }

    #[test]
    fn test_get_urls_1() {
        let path = "./test/npm_urls_1.txt";
        let url_list: Vec<String> = get_urls(&path);

        assert_eq!(url_list.len(), 5);
        assert_eq!(url_list[0], "https://www.npmjs.com/package/express\r");
        assert_eq!(url_list[1], "https://www.npmjs.com/package/vue\r");
        assert_eq!(url_list[2], "https://www.npmjs.com/package/react\r");
        assert_eq!(url_list[3], "https://www.npmjs.com/package/svelte\r");
        assert_eq!(url_list[4], "https://www.npmjs.com/package/next");
        
    }

    #[test]
    fn test_get_urls_2() {
        let path = "./test/npm_urls_2.txt";
        let url_list: Vec<String> = get_urls(&path);

        assert_eq!(url_list.len(), 5);
        assert_eq!(url_list[0], "https://www.npmjs.com/package/axios\r");
        assert_eq!(url_list[1], "https://www.npmjs.com/package/webpack\r");
        assert_eq!(url_list[2], "https://www.npmjs.com/package/lodash\r");
        assert_eq!(url_list[3], "https://www.npmjs.com/package/fastify\r");
        assert_eq!(url_list[4], "https://www.npmjs.com/package/async");
    }

    #[test]
    fn test_get_urls_3() {
        let path = "./test/npm_urls_3.txt";
        let url_list: Vec<String> = get_urls(&path);

        assert_eq!(url_list.len(), 5);
        assert_eq!(url_list[0], "https://www.npmjs.com/package/aws-sdk\r");
        assert_eq!(url_list[1], "https://www.npmjs.com/package/bcrypt\r");
        assert_eq!(url_list[2], "https://www.npmjs.com/package/cors\r");
        assert_eq!(url_list[3], "https://www.npmjs.com/package/deep-equal\r");
        assert_eq!(url_list[4], "https://www.npmjs.com/package/eslint");
    }

    #[test]
    fn test_get_urls_4() {
        let path = "./test/bad_urls.txt";

        let url_list: Vec<String> = get_urls(&path);
        assert_eq!(url_list.len(), 10);
        assert_eq!(url_list[0], "https://github.com/phonegap/phonegap-app-anyconference");
        assert_eq!(url_list[1], "https://github.com/ReversedK/LocateAnything");
        assert_eq!(url_list[2], "https://github.com/l3lackcurtains/graphql-boilerplate");
        assert_eq!(url_list[3], "https://github.com/vbaicu/mMusicCast");
        assert_eq!(url_list[4], "https://github.com/anychart-solutions/anystock-drawing-tools-and-annotations-demo");
        assert_eq!(url_list[5], "https://www.npmjs.com/package/url-inspector");
        assert_eq!(url_list[6], "https://www.npmjs.com/package/sharebutton");
        assert_eq!(url_list[7], "https://www.npmjs.com/package/anycontrol");
        assert_eq!(url_list[8], "https://www.npmjs.com/package/pan-zoom");
        assert_eq!(url_list[9], "https://www.npmjs.com/package/opentok-screen-sharing");
    }

    #[test]
    fn test_get_urls_5() {
        let path = "./test/good_urls.txt";
        let url_list: Vec<String> = get_urls(&path);

        assert_eq!(url_list.len(), 10);
        assert_eq!(url_list[0], "https://github.com/ramda/ramda");
        assert_eq!(url_list[1], "https://github.com/debug-js/debug");
        assert_eq!(url_list[2], "https://github.com/josephg/ShareJS");
        assert_eq!(url_list[3], "https://github.com/jashkenas/underscore");
        assert_eq!(url_list[4], "https://github.com/Automattic/mongoose");
        assert_eq!(url_list[5], "https://www.npmjs.com/package/express");
        assert_eq!(url_list[6], "https://www.npmjs.com/package/async");
        assert_eq!(url_list[7], "https://www.npmjs.com/package/lodash");
        assert_eq!(url_list[8], "https://www.npmjs.com/package/axios");
        assert_eq!(url_list[9], "https://www.npmjs.com/package/mocha");
    }

    #[test]
    fn test_empty_file() {
        let path = "./test/empty_file.txt";
        let url_list: Vec<String> = get_urls(&path);
        assert_eq!(url_list.len(), 1);
        assert_eq!(url_list[0], "");
    }

    #[test]
    fn test_get_github_url_for_npm() {
        let npm_url = "https://www.npmjs.com/package/axios";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/axios/axios");
        assert_ne!(github_url, "");

        let npm_url = "https://www.npmjs.com/package/lodash";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/lodash/lodash");
        assert_ne!(github_url, "");

        let npm_url = "https://www.npmjs.com/package/react";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/facebook/react");
        assert_ne!(github_url, "");

        let npm_url = "https://www.npmjs.com/package/svelte";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/sveltejs/svelte");
        assert_ne!(github_url, "");

        let npm_url = "https://www.npmjs.com/package/next";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/vercel/next.js");
        assert_ne!(github_url, "");

        let npm_url = "https://www.npmjs.com/package/express";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/expressjs/express");
        assert_ne!(github_url, "");

        let npm_url = "https://www.npmjs.com/package/vue";
        let github_url = get_github_url_for_npm(npm_url).unwrap();
        assert_eq!(github_url, "https://github.com/vuejs/core");
        assert_ne!(github_url, "");
    }

        
}