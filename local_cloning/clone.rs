use std::env; //rust stdlib function to get command line args

fn main(){

    //PLAN
    //1. clone a github repo into local directory
        //1.2. clone a npm repo into local directory
    //2. find the readme file
    //3. count characters in that file
    
    let args: Vec<String> = env::args().collect(); //take the command line arguments and creates a vector out of them

    let url = &args[1]; //create a variable and save the first command line argument into it
    
    println!("URL passed in from the command line: {}", url); //print the url we saved from the command line

    

}

