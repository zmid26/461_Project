//Add bcrypt = "0.14.0" to Cargo.toml

// User struct
struct User {
    username: String,
    password: String,
}
// Assume input strings "username" and "password" are provided to the function
fn new_user(username: String, password: String){
    // Create new user
    let mut user = User {
        username: username,
        password: password,
    };

    // Check if user already exists
    if user_exists(user.username) {
        // Return invalid input *******
    }

    // Sanitize username
    user.username = sanitize_user(user.username);

    // Hash password
    user.password = hash_password(user.password);

    // Store user in database
    store_user(user);
}

// Function to authenticate user (returns true if user is authenticated, false otherwise)
fn authenticate_user(username: String, password: String) -> bool {
    // Get user from database using username (let user = )

    // Check if user exists
    if user.is_none() {
        return false;
    }
    
    // Check if password is correct
    let user = user.unwrap();
    let is_correct = bcrypt::verify(password, &user.password).unwrap();
    return is_correct;
}

//-----Helper Functions-----//

// Function to check if user exists
fn user_exists(username: String) -> bool {
    // Search for username in database
    // If username exists, return true
    // Else, return false
    todo!()
}

// Function to hash the password using bcrypt
fn hash_password(password: String) -> String {
    let hashed_password = bcrypt::hash(password, bcrypt::DEFAULT_COST).unwrap();
    return hashed_password;
}

// Function to store User struct in database
fn store_user(user: User) {
    // Store user w/ hashed password in database
}
