use std::env; //rust stdlib function to get command line args
use std::process::Command; //library to run processes in rust
use std::fs; //rust file library
use std::process;

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //run the rampup calculation (calculate_RampUp)
    let _run_rampup = Command::new("./target/debug/calculate_ramp_up").arg(&cli_input[1]).status(); //runs the rust executable "calculate_RampUp" with the CLI input file

    //run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3").arg("graphql_api/calculate_Correctness.py").arg(&cli_input[1]).status();

    //run the responsive maintainer calculation (calculate_ResponsiveMaintainer.py)
    let _run_responsivemaintainer = Command::new("python3").arg("rest_api/calculate_ResponsiveMaintainer.py").arg(&cli_input[1]).status();

    //run the license calculation (license.py)
    let _run_license = Command::new("python3").arg("local_cloning/license.py").arg(&cli_input[1]).status();

    let _print_results = Command::new("python3").arg("output/print_results.py").arg(&cli_input[1]).status();
    
    let _set_logs = Command::new("python3").arg("verbosity.py").arg(&cli_input[1]).status();

    clean_up();

    process::exit(0);
}

//this function removes locally cloned repos and output files
fn clean_up(){

    fs::remove_dir_all("local_cloning/cloned_repos/").expect("Error deleting cloned repos directory");
    fs::remove_file("output/correctness_out.txt").expect("Error deleting cloned repos directory");
    fs::remove_file("output/license_out.txt").expect("Error deleting cloned repos directory");
    fs::remove_file("output/rampup_out.txt").expect("Error deleting cloned repos directory");
    fs::remove_file("output/resp_maintain_out.txt").expect("Error deleting cloned repos directory");

}