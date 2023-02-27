use std::env; //rust stdlib function to get command line args
use std::process::Command; //library to run processes in rust
use std::fs; //rust file library
use std::process;
mod metrics;

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //run the rampup calculation (calculate_RampUp)
    metrics::calculate_ramp_up::ramp_up_score(&cli_input[1]);

    //run the bus factor calculation (calculate_BusFactor)
    metrics::calculate_bus_factor::bus_factor_score(&cli_input[1]);

    //run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3").arg("src/metrics/calculate_correctness.py").arg(&cli_input[1]).status().expect("Err");

    //if the correctness script didnt return success, exit 1 and print error
    if _run_correctness.success() == false {
        println!("Error calculating correctness!");
        std::process::exit(1);
    }

    //run the responsive maintainer calculation (calculate_ResponsiveMaintainer.py)
    let _run_responsivemaintainer = Command::new("python3").arg("src/metrics/calculate_responsive_maintainer.py").arg(&cli_input[1]).status().expect("Err");

    //if the responsive maintainer script didnt return success, exit 1 and print error
    if _run_responsivemaintainer.success() == false {
        println!("Error calculating responsive maintainer!");
        std::process::exit(1);
    }

    //run the license calculation (license.py)
    let _run_license = Command::new("python3").arg("src/metrics/calculate_license.py").arg(&cli_input[1]).status().expect("Err");

    //if the license script didnt return success, exit 1 and print error
    if _run_license.success() == false {
        println!("Error calculating license!");
        std::process::exit(1);
    }

    //print the results (print_results.py)
    let _print_results = Command::new("python3").arg("src/metric_utility_functions/print_results.py").arg(&cli_input[1]).status().expect("Err");

    //if printing results didnt return success, exit 1 and print error
    if _print_results.success() == false {
        println!("Error printing results!");
        std::process::exit(1);
    }
    
    //do logging 
    let _set_logs = Command::new("python3").arg("src/verbosity.py").arg(&cli_input[1]).status().expect("Err");

    //if verbosity didnt return success, exit 1 and print error
    if _set_logs.success() == false {
        println!("Error in verbosity script!");
        std::process::exit(1);
    }

    //this will remove output files and locally cloned repos
    clean_up();

    //exit 0 on success
    process::exit(0);
}

//this function removes locally cloned repos and output files
fn clean_up(){

    //remove local clone repos
    let _clean_old_clones = match fs::remove_dir_all("output/cloned_repos/"){
        Ok(_clean_old_clones) => _clean_old_clones,
        Err(..) => {
            println!("Error cleaning old cloned repos!\n");
            std::process::exit(1);
        }
    };

    //clean output files for each metric
    let _clean_correctness = match fs::remove_file("output/correctness_out.txt"){
        Ok(_clean_correctness) => _clean_correctness,
        Err(..) => {
            println!("Error cleaning correctness output!\n");
            std::process::exit(1);
        }
    };

    let _clean_license = match fs::remove_file("output/license_out.txt"){
        Ok(_clean_license) => _clean_license,
        Err(..) => {
            println!("Error cleaning license output!\n");
            std::process::exit(1);
        }
    };

    let _clean_rampup = match fs::remove_file("output/rampup_out.txt"){
        Ok(_clean_rampup) => _clean_rampup,
        Err(..) => {
            println!("Error cleaning rampup output!\n");
            std::process::exit(1);
        }
    };

    let _clean_respmain = match fs::remove_file("output/resp_maintain_out.txt"){
        Ok(_clean_respmain) => _clean_respmain,
        Err(..) => {
            println!("Error cleaning responsive maintainer output!\n");
            std::process::exit(1);
        }
    };

}