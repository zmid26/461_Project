use std::env; //rust stdlib function to get command line args
//use std::fs; //rust file library
use std::process::Command; //library to run processes in rust

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //save off the argument passed to the CLI
    let arg = &cli_input[1]; 

    if arg.eq("install") == true { //CLI argument was "install"

        //run script to install necessary stuff for rust (rust_installer.py)
        let _rust_install_command = Command::new("python3").arg("install/localclone_install.py").output();
    
    }
    else if arg.eq("build") == true { //CLI argument was "build"

        //build the rammpup calculation code (calculate_RampUp.rs)
        //let _rampup_build_command = Command::new("rustc").arg("local_cloning/calculate_RampUp.rs").arg("--out-dir").arg("local_cloning/").spawn(); //compiles the rust script called calculate_RampUp.rs

    }
    else if arg.eq("test") == true { //CLI argument was "test"
        println!("CLI input was: test");
    }
    else { //CLI argument was an input file

        //run the rampup calculation (calculate_RampUp)
        let _run_rampup = Command::new("./target/debug/calculate_ramp_up").arg(&cli_input[1]).status(); //runs the rust executable "calculate_RampUp" with the CLI input file

    }
}
