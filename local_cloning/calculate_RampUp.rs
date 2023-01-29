use std::env; //rust stdlib function to get command line args
use std::fs; //rust file library
use std::process::Command; //library to run processes in rust

fn main(){
    
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //create a variable for the file path and save the first command line argument into it
    let filepath = &cli_input[1]; 

    //take the contents of the file and save into a single string
    let data = fs::read_to_string(filepath).expect("Unable to read file");

    //now, chop this string into a vector at every newline since the URLS are newline delimited
    let _urls: Vec<&str> = data.split('\n').collect();
    
    //runs python script to clone all the repos into directories labeled by number (first is '1')
    let _run_clone_script = Command::new("python3").arg("local_cloning/clone_repo.py").arg(&cli_input[1]).spawn();
}

