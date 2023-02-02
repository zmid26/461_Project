use std::env; //rust stdlib function to get command line args
use std::fs; //rust file library
use std::fs::File; //rust file library
use std::process::Command; //library to run processes in rust
use std::io::{BufRead, BufReader};
//use pyo3::prelude::*; //module to run python code in rust

fn main(){
    
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //create a variable for the file path and save the first command line argument into it
    let filepath = &cli_input[1]; 

    //take the contents of the file and save into a single string
    let data = fs::read_to_string(filepath).expect("Unable to read file");

    //now, chop this string into a vector at every newline since the URLS are newline delimited
    let _urls: Vec<&str> = data.split('\n').collect();

    //get number of URLS
    let num_urls = _urls.len();
    println!("number of urls passed in: {}", num_urls);

    //loop through urls and print their corresponding clone folder numbers
    let mut url_index = 1;
    for url in _urls {
        println!("folder number / url     :     {} / {}", url_index, url);
        url_index += 1;
    }
    
    //run clone function to locally clone repos (pass in the input file)
    clone_repos((&filepath).to_string());

    let filename = "local_cloning/cloned_repos/2/index.js";

    let num_lines: i64 = count_total_lines((&filename).to_string());

    println!("Total lines are: {}",num_lines);
}

//this function takes in a filename and returns the number of lines in it
fn count_total_lines(filename: String) -> i64{
    
    //open the file
    let file = File::open(filename).expect("Unable to open file");

    //open it with bufreader so that we dont have to open and close for every line read (normal read would open/close file every time)
    let buf_file = BufReader::new(file);
    
    //create a mut variable since we will be changing it
    let mut cnt  = 0;
    
    //count the lines in the file
    for _ in buf_file.lines() {
        cnt = cnt + 1;
    }

    //return the number of lines
    return cnt;
} 

//this function simply runs the file "clone_repo.py" which is located instide of the "461_project/local_cloning" directory
fn clone_repos(filepath: String){

    //run clone_repo.py
    let _run_clone_script = Command::new("python3").arg("local_cloning/clone_repo.py").arg(&filepath).status();
}

