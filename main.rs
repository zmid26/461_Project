use std::env; //rust stdlib function to get command line args
use std::process::Command; //library to run processes in rust
use std::fs; //rust file library
use std::process;

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //run the rampup calculation (calculate_RampUp)
    let _run_rampup = Command::new("./target/debug/calculate_ramp_up").arg(&cli_input[1]).status().expect("Err"); //runs the rust executable "calculate_RampUp" with the CLI input file

    //if the rampup calculation failed, exit 1 (error message is handled in the calculation code)
    if _run_rampup.success() == false {
        println!("Error calculating rampup!");
        process::exit(1);
    }
    
    //run the bus factor calculation
    let _run_busfactor = Command::new("./target/debug/calculate_bus_factor").arg(&cli_input[1]).status().expect("Err"); //runs the rust executable "calculate_BusFactor" with the CLI input file
    
    if _run_busfactor.success() == false {
        println!("Error calculating bus factor!");
    	process::exit(1);
    }

    //run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3").arg("graphql_api/calculate_Correctness.py").arg(&cli_input[1]).status().expect("Err");

    //if the correctness script didnt return success, exit 1 and print error
    if _run_correctness.success() == false {
        println!("Error calculating correctness!");
        std::process::exit(1);
    }

    //run the responsive maintainer calculation (calculate_ResponsiveMaintainer.py)
    let _run_responsivemaintainer = Command::new("python3").arg("rest_api/calculate_ResponsiveMaintainer.py").arg(&cli_input[1]).status().expect("Err");

    //if the responsive maintainer script didnt return success, exit 1 and print error
    if _run_responsivemaintainer.success() == false {
        println!("Error calculating responsive maintainer!");
        std::process::exit(1);
    }

    //run the license calculation (license.py)
    let _run_license = Command::new("python3").arg("local_cloning/license.py").arg(&cli_input[1]).status().expect("Err");

    //if the license script didnt return success, exit 1 and print error
    if _run_license.success() == false {
        println!("Error calculating license!");
        std::process::exit(1);
    }

    //print the results (print_results.py)
    let _print_results = Command::new("python3").arg("output/print_results.py").arg(&cli_input[1]).status().expect("Err");

    //if printing results didnt return success, exit 1 and print error
    if _print_results.success() == false {
        println!("Error printing results!");
        std::process::exit(1);
    }
    
    //do logging 
    let _set_logs = Command::new("python3").arg("verbosity.py").arg(&cli_input[1]).status().expect("Err");

    //if verbosity didnt return success, exit 1 and print error
    if _print_results.success() == false {
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
    let _clean_old_clones = match fs::remove_dir_all("local_cloning/cloned_repos/"){
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
