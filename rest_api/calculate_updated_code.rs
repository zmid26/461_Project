/*  Name: Matthew Nale
 *  Date of Last Edit: 3/25/2023
 *  
 *  Purpose: Calculate the amount of code introduced through pull requests compared to the overall size of the project
 *
 *  Details: Using data from the pull requests of the repo, find the fraction of new code being introduced through commits from pull requests
*/
use std::env;
use std::fs; //rust file library
use std::fs::File; //rust file library
use std::process::Command; //library to run processes in rust
use std::io::BufWriter;
use std::path::Path;
use std::io::Write;

fn main(){
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //create a variable for the file path and save the first command line argument into it
    let filepath = &cli_input[1]; 

    //take the contents of the file and save into a single string
    let data = match fs::read_to_string(filepath){
        Ok(data) => data,
        Err(..) => {
            println!("Error reading the input file!\n");
            std::process::exit(1);
        }
    };
    
    //now, chop this string into a vector at every newline since the URLS are newline delimited
    let mut _urls: Vec<&str> = data.split('\n').collect();

    //Remove last blank newline character after splitting
    _urls.pop();

    //if the logfiles exist from a previous run, delete them
    let is_logv1 = Path::new("log/logv1.txt").exists();
    if is_logv1 == true{
        
        //remove old log1 file and handle error
        let _remove_log1 = match fs::remove_file("log/logv1.txt"){
            Ok(_remove_log1) => _remove_log1,
            Err(..) => {
                println!("Error deleting old log1 file!\n");
                std::process::exit(1);
            }
        };
    }
    let is_logv2 = Path::new("log/logv2.txt").exists();
    if is_logv2 == true{

        //remove old log2 file and handle error
        let _remove_log2 = match fs::remove_file("log/logv2.txt"){
            Ok(_remove_log2) => _remove_log2,
            Err(..) => {
                println!("Error deleting old log2 file!\n");
                std::process::exit(1);
            }
        };
    }

    //open new logfiles after cleaning old ones
    let mut log2 = BufWriter::new(File::create("log/logv2.txt").expect("Error creating log2 file!"));

    //open output file to write bus factor scores to
    let mut out_file = BufWriter::new(File::create("output/updatedcode_out.txt").expect("Error opening output for updated code!"));

    //Call information with rest_api functions for each url
    for url in _urls {

        let fractionnew = Command::new("python3").arg("rest_api/pullRequests.py").arg(url).output().expect("Err");
        write!(log2, "\nFraction of code released through pull requests for url {}: {:?}\n", url, &fractionnew.stdout).expect("Error writing to log");
        
	let mut fraction_new = String::from_utf8(fractionnew.stdout).unwrap();
	fraction_new.pop();

	let updated_code : f64 = fraction_new.parse().unwrap();

        write!(log2, "UpdatedCode score for url {}: {:.2}\n\n", url, updated_code).expect("Error writing to log");
        write!(out_file, "{0}\n", updated_code).expect("Error writing updated code score to output");
    }
}
