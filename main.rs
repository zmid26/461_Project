use std::env; //rust stdlib function to get command line args
//use std::fs; //rust file library
use std::process::Command; //library to run processes in rust

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //run the rampup calculation (calculate_RampUp)
    let _run_rampup = Command::new("./target/debug/calculate_ramp_up").arg(&cli_input[1]).status(); //runs the rust executable "calculate_RampUp" with the CLI input file

    //run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3").arg("graphql_api/calculate_Correctness.py").arg(&cli_input[1]).status();

    //run the responsive maintainer calculation (calculate_ResponsiveMaintainer.py)
    let _run_responsivemaintainer = Command::new("python3").arg("rest_api/calculate_ResponsiveMaintainer.py").arg(&cli_input[1]).status();

}