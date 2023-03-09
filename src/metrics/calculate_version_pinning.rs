use serde_json::Value::Null;
use regex::Regex;
use base64::{Engine as _, engine::general_purpose};
use std::str;
use crate::metrics::calculate_bus_factor;
use std::fs::File; //rust file library
use std::io::BufWriter;
use std::io::Write;

pub fn version_pinning_score(filepath: &str) {
    simple_log::info!("Calculating Version Pinning Score.)");

    // Get the urls from the input file
    let urls = calculate_bus_factor::get_urls(filepath);

    // create output file
    let mut out_file = BufWriter::new(
        File::create("output/version_pinning_out.txt").expect("Error creating output file!"),
    );

    for url in urls {
        let git_url;

        // If the url is from npm, get the github url
        if &url[0..22] == "https://www.npmjs.com/" {
            git_url = calculate_bus_factor::get_github_url_for_npm(&url).unwrap();
        } else {
            git_url = url.to_string();
        }

        let repo_full_name = &git_url[19..]; // {owner}/{repo}
        let mut score = 0.0;
        let content_json;
        let re = Regex::new(r"^[~^]?\d+\.\d+.").unwrap();
        let mut num_depends = 0.0;
        let mut num_std_depends = 0.0;
    
        // if package-lock.json exists, use that for dependencies, else use package.json
        match get_file_content_json(repo_full_name, "package-lock.json") {
            // using package-lock.json
            Ok(v) => {
                content_json = v;
                // loop thru dependencies, seeing if their version matches the standard
                for (_dependency, depend_info) in content_json["dependencies"].as_object().unwrap() {
                    // run regex on the version
                    let vers = depend_info["version"].as_str().unwrap();
                    num_depends += 1.0;
                    if re.is_match(vers) {
                        num_std_depends += 1.0;
                    }
                    score = num_std_depends / num_depends;
                }
            },
            // using package.json
            Err(..) => {
                content_json = get_file_content_json(repo_full_name, "package.json").unwrap();
                // if no dependencies, score is 0
                if content_json["dependencies"] == Null {
                    score = 0.0;
                }
                // else loop thru dependencies, seeing if their version matches the standard
                else {
                    for (_dependency, version) in content_json["dependencies"].as_object().unwrap() {
                        // run regex on the version
                        let vers = version.as_str().unwrap();
                        num_depends += 1.0;
                        if re.is_match(vers) {
                            num_std_depends += 1.0;
                        }
                    }
                    score = num_std_depends / num_depends;
                }
            },
        };

        // Write the score to the output file
        write!(out_file, "{0}\n", score).expect("Error writing code review to output");
    }
}

// given a repo and a file name, this returns the file as a json object
fn get_file_content_json(repo_full_name: &str, filename: &str) -> Result<serde_json::Value, ureq::Error> {
    let token = std::env::var("GITHUB_TOKEN").unwrap();
    let http_url = format!("https://api.github.com/repos/{}/contents/{}", &repo_full_name, &filename);
    let response: serde_json::Value = ureq::get(&http_url)
                    .set("Authorization", &token[..])
                    .call()?
                    .into_json()?;
    let mut content = response["content"].as_str().unwrap().to_string();
    content = content.replace("\n", "");
    let content_decoded = general_purpose::STANDARD.decode(content).unwrap();
    let content_decoded_str = str::from_utf8(&content_decoded).unwrap();
    let content_json: serde_json::Value = serde_json::from_str(content_decoded_str).unwrap();
    return Ok(content_json);
}