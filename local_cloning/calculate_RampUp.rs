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

    //get number of URLS
    let num_urls = _urls.len();
    println!("number of urls passed in: {}", num_urls);

    //loop through urls and print their corresponding clone folder numbers
    let mut url_index = 1;
    for url in _urls {
        println!("folder number / url     :     {} / {}", url_index, url);
        url_index += 1;
    }
    
    //run clone function to locally clone repos
    clone_repos((&filepath).to_string());
}

//this function simply runs the file "clone_repo.py" which is located instide of the "461_project/local_cloning" directory
fn clone_repos(filepath: String){

    //run clone_repo.py
    let _run_clone_script = Command::new("python3").arg("local_cloning/clone_repo.py").arg(&filepath).output();
}

