# Functionality

"./run install" will run the python script called "localclone_installer.py" in the 'install' directory

    -does this straight from bash script


"./run build" will run the command "cargo build"

    -this command builds "main.rs" as well as "calculate_ramp_up.rs" at the same time 
    -this command also installs dependencies that are needed for the rust code. these are specified 'Cargo.toml' file


"./run score URL_FILE" will run the command "./target/debug/main score URL_FILE -s"

    -this command runs the executable from the "main.rs" rust file
    -will not print net score nor metric scores, but will save scores to .txt files in the /output directory

"./run showscore URL_FILE" will run the command "./target/debug/main showscore URL_FILE -p"

    -this command runs the exectuable from the "main.rs" rust file
    -will print net score and metric scores to the user, and clean up .txt files after printing
    -only should be used for personal testing of metrics and scoring

"./run test" will run the test suite

    -this command runs a test suite consisting of 20 separate test cases
    -10 good and 10 bad urls are included in this test suite
    -number of passed tests and line coverage % are printed to output
