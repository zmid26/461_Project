use std::env; //rust stdlib function to get command line args
//use std::fs; //rust file library
use std::process::Command; //library to run processes in rust

fn main(){

    //save the command line argument
    let cli_input: Vec<String> = env::args().collect(); 

    //save off the argument passed to the CLI
    let arg = &cli_input[1]; 

    if arg.eq("install") == true { //CLI argument was "install"

        //PUT THE COMMANDS NEEDED TO INSTALL DEPENDENCIES IN HERE _____________________________________________________


        //_____________________________________________________________________________________________________________
    
    }
    else if arg.eq("build") == true { //CLI argument was "build"

        //COMPILATION AND BUILD COMMANDS GO HERE IN HERE _______________________________________________________________

        //these commands compile the local cloning code
        let _clone_build_command = Command::new("rustc").arg("local_cloning/clone.rs").spawn(); //compiles the rust script called clone.rs

        //______________________________________________________________________________________________________________

    }
    else if arg.eq("test") == true { //CLI argument was "test"
        println!("CLI input was: test");
    }
    else { //CLI argument was an input file

        //COMMANDS TO RUN CODE GO HERE______________________________________________________________________

        //run the local cloning executable
        let _run_clone_script = Command::new("./clone").arg(&cli_input[1]).spawn(); //runs the rust executable "clone" with the CLI input file

        //______________________________________________________________________________________________________________
    }
}
