use std::env; //rust stdlib function to get command line args
use std::fs; //rust file library

fn main(){

    //PLAN
    //1. clone a github repo into local directory
        //1.2. clone a npm repo into local directory
    //2. find the readme file
    //3. count characters in that file
    
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //create a variable for the file path and save the first command line argument into it
    let filepath = &cli_input[1]; 

    //take the contents of the file and save into a single string
    let data = fs::read_to_string(filepath).expect("Unable to read file");

    //now, chop this string into a vector at every newline since the URLS are newline delimited
    let urls: Vec<&str> = data.split('\n').collect();
    
    println!("URL passed in from the command line: {:?}", urls); //print the url we saved from the command line

    

}

