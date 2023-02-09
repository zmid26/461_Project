Current functionality:

"./run install" will run the python script called "localclone_installer.py" in the 'install' directory

    -does this straight from bash script


"./run build" will run the command "cargo build" 

    -this command builds "main.rs" as well as "calculate_ramp_up.rs" at the same time
    -these two executables will be located in the 'target/debug' directory 
    -this command also installs dependencies that are needed for the rust code. these are specified 'Cargo.toml' file


"./run URL_FILE" will run the command "./target/debug/main URL_FILE"

    -this command runs the executable from the "main.rs" rust file
    -will print formatted output that inlcudes all metrics except for license
    -scores are not rounded yet


"./run test" just prints a message out

    -we have not implemented the test functionality yet


