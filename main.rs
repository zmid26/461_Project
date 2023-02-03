use std::env; //rust stdlib function to get command line args
//use std::fs; //rust file library
use std::process::Command; //library to run processes in rust

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //run the rampup calculation (calculate_RampUp)
    let _run_rampup = Command::new("./target/debug/calculate_ramp_up").arg(&cli_input[1]).status(); //runs the rust executable "calculate_RampUp" with the CLI input file

}