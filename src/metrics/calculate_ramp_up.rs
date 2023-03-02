use std::fs; //rust file library
use std::fs::File; //rust file library
use std::io::BufWriter;
use std::io::Write;
use std::process::Command; //library to run processes in rust
use tokei::{Config, LanguageType, Languages};

pub fn ramp_up_score(filepath: &str) {

    //take the contents of the file and save into a single string
    let data = match fs::read_to_string(filepath) {
        Ok(data) => data,
        Err(..) => {
            println!("Error reading the input file!\n");
            std::process::exit(1);
        }
    };

    //now, chop this string into a vector at every newline since the URLS are newline delimited
    let _urls: Vec<&str> = data.split('\n').collect();

    //get number of URLS
    let num_urls = _urls.len();
    simple_log::info!("Number of URLs in the input file: {0}", num_urls);

    //loop through urls and log their corresponding clone folder numbers
    let mut url_index = 1;
    for url in _urls {
        simple_log::debug!("Folder number and url: {} / {}", url_index, url);
        url_index += 1;
    }


    //run clone function to locally clone repos (pass in the input file)
    clone_repos((&filepath).to_string());

    //open up the directory with all the cloned repos
    let cloned_folders =
        match fs::read_dir("output/cloned_repos/") {
            Ok(cloned_folders) => cloned_folders,
            Err(..) => {
                println!("Error opening up cloned repos directory!\n");
                std::process::exit(1);
            }
        };

    //initialize a counter for the current folder number
    let mut folder_num = 1;

    //open output file to write rampup scores to
    let mut out_file = BufWriter::new(
        File::create("output/rampup_out.txt").expect("Error opening output file for rampup"),
    );

    //loop through all folders in "cloned_repos"
    for folder in cloned_folders {
        //get the path of the current folder
        let _folder_path = (folder.unwrap().path().display()).to_string();

        //initialize parameters for when we use tokei to parse the folders and count code/comments
        let paths = &[_folder_path]; //folder to search
        let excluded = &[]; //folders excluded from the search
        let config = Config::default(); //configure the parser to default

        //configure the tokei language to be javascript
        let mut languages = Languages::new();
        languages.get_statistics(paths, excluded, &config);
        let js = &languages[&LanguageType::JavaScript];

        //get the number of lines of code and comments and log them
        let code_lines = js.code;
        let comment_lines = js.comments;

        simple_log::debug!("Lines of code in folder {}: {}",folder_num, code_lines);
        simple_log::debug!("Lines of comments in folder {}: {}", folder_num, comment_lines);
        
        //calculate rampup and log it
        let code_u32 = u32::try_from(code_lines).unwrap();
        let comment_u32 = u32::try_from(comment_lines).unwrap();
        let ramp_up = calculate_ramp_up(code_u32, comment_u32);
    
        simple_log::info!("RampUp score for repo {}: {:.2}",folder_num, ramp_up);

        //write the rampup score to the rampup_out.txt file in the output folder
        write!(out_file, "{0}\n", ramp_up).expect("Error writing rampup to output");

        //increment the folder counter
        folder_num += 1;
    }
}

//this function takes the number of code lines, and comment lines and calculates the rampup score
fn calculate_ramp_up(lines_of_code: u32, lines_of_comments: u32) -> f32 {
    //calculate RampUp score using our formula
    let float_code = lines_of_code as f32;
    let float_comments = lines_of_comments as f32;
    let calculated_score: f32 = 2.0 * (float_comments / float_code);

    //return 1 if the calculated score was greater than 1 and return the calculated score if it was less than 1
    if calculated_score > 1.0 {
        return 1.0;
    } else {
        return calculated_score;
    }
}

//this function runs the file "clone_repo.py"
fn clone_repos(filepath: String) {
    //run clone_repo.py
    let _run_clone_script = Command::new("python3")
        .arg("src/metric_utility_functions/clone_repo.py")
        .arg(&filepath)
        .status()
        .expect("Err");

    //if the clone script didnt return success, exit 1 and print error
    if _run_clone_script.success() == false {
        println!("Error cloning repos!");
        std::process::exit(1);
    }
}
