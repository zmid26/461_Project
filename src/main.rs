use std::env; // Rust stdlib function to get command line args
use std::fs; // Rust file library
use std::process;
use std::process::Command; // Library to run processes in rust
mod metrics;

fn main()->Result<(), String> {
    // Save the command line argument
    let cli_input: Vec<String> = env::args().collect();

    //Set up logging for rust scripts
    logging()?;

    // Run the rampup calculation (calculate_RampUp)
    metrics::calculate_ramp_up::ramp_up_score(&cli_input[1]);

    // Run the bus factor calculation (calculate_BusFactor)
    metrics::calculate_bus_factor::bus_factor_score(&cli_input[1]);

    //Set up logging for python scripts (verbosity.py)
    let _set_logs = Command::new("python3")
        .arg("src/metrics/verbosity.py")
        .arg(&cli_input[1])
        .status()
        .expect("Err");

    // If verbosity didnt return success, exit 1 and print error
    if _set_logs.success() == false {
        println!("Error in verbosity script!");
        clean_up();
        std::process::exit(1);
    }

    // Run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3")
        .arg("src/metrics/calculate_correctness.py")
        .arg(&cli_input[1])
        .status()
        .expect("Err");

    // If the correctness script didnt return success, exit 1 and print error
    if _run_correctness.success() == false {
        println!("Error calculating correctness!");
        //clean_up();
        std::process::exit(1);
    }

    // Run the responsive maintainer calculation (calculate_ResponsiveMaintainer.py)
    let _run_responsivemaintainer = Command::new("python3")
        .arg("src/metrics/calculate_responsive_maintainer.py")
        .arg(&cli_input[1])
        .status()
        .expect("Err");

    // If the responsive maintainer script didnt return success, exit 1 and print error
    if _run_responsivemaintainer.success() == false {
        println!("Error calculating responsive maintainer!");
        clean_up();
        std::process::exit(1);
    }

    // Run the license calculation (license.py)
    let _run_license = Command::new("python3")
        .arg("src/metrics/calculate_license.py")
        .arg(&cli_input[1])
        .status()
        .expect("Err");

    // If the license script didnt return success, exit 1 and print error
    if _run_license.success() == false {
        println!("Error calculating license!");
        clean_up();
        std::process::exit(1);
    }

    // Print the results (print_results.py)
    let _print_results = Command::new("python3")
        .arg("src/metric_utility_functions/print_results.py")
        .arg(&cli_input[1])
        .status()
        .expect("Err");

    // If printing results didnt return success, exit 1 and print error
    if _print_results.success() == false {
        println!("Error printing results!");
        clean_up();
        std::process::exit(1);
    }

    // This will remove output files and locally cloned repos
    clean_up();

    // Exit 0 on success
    process::exit(0);
}

// This function removes locally cloned repos and output files
fn clean_up() {
    // Clean output folder
    let _clean_output = match fs::remove_dir_all("output") {
        Ok(_clean_output) => _clean_output,
        Err(..) => {
            println!("Error cleaning output folder!\n");
            std::process::exit(1);
        }
    };
}


fn logging()->Result<(), String>{
    let log_file = env::var("LOG_FILE").unwrap();
    let level = env::var("LOG_LEVEL");
    let log_level = match &level {
        Ok(t) => &t,
        Err(_e) => "0", //default level = 0
    };
    let level = match log_level{
        "0" => "trace",
        "1" => "info",
        "2" => "debug",
        _ => "error"
    };

    let config = simple_log::LogConfigBuilder::builder()
        .path(log_file)
        .level(level)
        .output_file()
        .build();
    simple_log::new(config)?;
    simple_log::info!("Sucessfully created log file");

    Ok(())
}