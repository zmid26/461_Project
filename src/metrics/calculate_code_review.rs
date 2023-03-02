use crate::metrics::calculate_bus_factor;
use octocrab::params;
use octocrab::Octocrab;
use std::fs::File; //rust file library
use std::io::BufWriter;
use std::io::Write;
use std::sync::Arc;

pub fn code_review_score(filepath: &str) {
    simple_log::info!("Calculating Code Review Score.)");

    let token = std::env::var("GITHUB_TOKEN");
    let octocrab = match token {
        Ok(t) => {
            simple_log::info!("CR Score: Used Github token.)");
            Arc::new(Octocrab::builder().personal_token(t).build().unwrap())
        }
        Err(_e) => {
            simple_log::info!("CR Score: Did not use Github token.");
            octocrab::instance()
        }
    };

    // Create the output file
    let mut out_file = BufWriter::new(
        File::create("output/code_review_out.txt").expect("Error creating output file!"),
    );

    let urls = calculate_bus_factor::get_urls(filepath);

    for url in urls {
        let git_url;

        // If the url is from npm, get the github url
        if &url[0..22] == "https://www.npmjs.com/" {
            git_url = calculate_bus_factor::get_github_url_for_npm(&url).unwrap();
        } else {
            git_url = url.to_string();
        }

        // Get the keywords from the url in the form (owner, repo)
        let (owner, repo) = calculate_bus_factor::get_keywords(&git_url);

        // Calculate the code review score
        let score = find_cr_score(&octocrab, owner, repo);

        // Write the score to the output file
        write!(out_file, "{0}\n", score).expect("Error writing code review to output");
    }
}

#[tokio::main]
async fn find_cr_score(octocrab: &Octocrab, owner: &str, repo: &str) -> f64 {
    let num_pulls = 50;
    let page = octocrab
        .pulls(owner, repo)
        .list()
        .state(params::State::Closed)
        .head("main")
        .per_page(num_pulls)
        .send()
        .await
        .expect("Error getting pull requests");

    let mut total_reviewed = 0.0;
    for pull in page {
        // See if the pull request has been merged
        let merged = octocrab
            .pulls(owner, repo)
            .is_merged(pull.number)
            .await
            .expect("Error in is_merged");
        
        if merged {
            // Get the reviews for the pull request
            let reviews = octocrab
                .pulls(owner, repo)
                .list_reviews(pull.number)
                .await;
            let num_reviewers = match reviews{
                Ok(mut reviews) => reviews.take_items().len(),
                Err(_e) => 0
            };
            simple_log::debug!("Pull request merged with {} reviewers.", num_reviewers);

            if num_reviewers > 0 {
                total_reviewed += 1.0;
            }
        } else {
            simple_log::debug!("Pull request not merged.");
        }
    }
    let score = total_reviewed / num_pulls as f64;
    simple_log::info!("Code Review Score: {}", score);
    score
}
