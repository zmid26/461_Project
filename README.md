Current functionality:

"./run install" will run the python script called "localclone_installer.py" in the 'install' directory

    -it does this straight from the 'run.rs' file
    -right now, the only thing this file does is install GitPython


"./run build" will run the command "cargo build" 

    -this command builds "main.rs" as well as "calculate_ramp_up.rs" at the same time
    -these two executables will be located in the 'target/debug' directory 
    -this command also installs dependencies that are needed for the rust code. these are specified 'Cargo.toml' file


"./run URL_FILE" will run the command "./target/debug/main URL_FILE"

    -this command runs the executable from the "main.rs" rust file
    -as of now, this executable will only run the executable from the "calculate_ramp_up.rs" file
    -once other metrics have been implemented, "main.rs" will call all metric calculations needed
    -it will also handle CLI output when we get to it
    -NOTE: the folder 'local_cloning/cloned_repos' must NOT exist when this command is executed.
           the program will fail if this directory already exists, as it creates it at runtime.
           before running this command, make sure that directory isn't leftover from a previous run.
    -NOTE: there is no input checking in terms of the filename yet. make sure to give the full path
           to the input URL file

"./run test" just prints a message out

    -we have not implemented the test functionality yet


