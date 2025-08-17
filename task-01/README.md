# Task 01: Terminal Hunt

***Review on the task:***  *More difficult than expected, but was definetly fun and got to learn very valuable things*



# Part 1:
The clue said to find a **"facility"** inside Earth. I first tried using the *find* command to search for files or folders with **"facility"** in their name, but this returned nothing because the target was hidden. I then switched to the *grep* command to search for the word **"facility"** inside all files under the Earth directory. This revealed a hidden directory in ***Russia/Vladimir_Oblast*** containing a file called **gravity_equation.txt**. Using the *cat* command to read the file gave me the first key for Part 2.

# Part 2:
The clue indicated that I needed to reach a wormhole near Saturn's ring. I searched for hidden files in the Saturn directory using the *find* command and discovered a hidden script named **.wormhole.sh** inside **Saturn/Ring**. I made the script executable using *chmod +x* and then ran it, which revealed the second key. The output also instructed me to copy **solutions.md** to a safe location, but I could not locate this file at the time. After thinking for a while, I assumed it might be referring to creating my own file to store passwords and commands — something I had already done (though under a different name) — so I decided to proceed.

# Part 3:
To begin Part 3, I switched from the Solar_System branch to the GargantuaSystem branch using the command:

"***git checkout GargantuaSystem***"


I then used the find command to search for hidden directories, which returned approximately 8–9 paths. I navigated into each of these directories one by one.

During this process, I discovered the final congratulatory message before obtaining the key to Part 4. Since the instructions specified creating a separate file to store the passwords for each part, I saved the path in a notepad and continued searching for the Part 4 key.

Eventually, I located it in the file:

"***./Edmunds_Planet/Desert5/.hidden_cave/.hidden_branch/HABITABLE.txt***"


At that point, I realized that the keys I had been collecting were not random strings of letters, but Base64-encoded values.

# Part 4:
As mentioned earlier, I encountered the final key and congratulatory message even before obtaining the key to Part 4. I navigated back to the same path and used the cat command to read the binary code in the hidden file message_from_Them.txt. I then converted this binary code into a Base64 string.

The task instructions specified creating a solve.sh script to decode the Base64 string into human-readable text. For this, I referred to online resources. After creating solve.sh, I combined all the decoded Base64 strings to reveal the final message, which instructed me to run the gravity.sh file—a file I had already executed while searching for the Part 4 key.

I then navigated back to the path:

Terminal-Hunt/Gargantua/the_centre/.the_singularity


and used the ls -a command to list hidden files. This revealed the gravity_singularity.sh file, whose contents I read using cat without applying chmod +x.


# Commands Learned


## Linux / Ubuntu Terminal:

- cd <directory_path> – Change the current working directory to the specified path.
- ls – List files and directories in the current directory.
- ls -la – List all files, including hidden ones, with detailed permissions and info.
- find <path> -type f -name "<pattern>" – Search for files matching a name pattern.
- grep -Ri "<keyword>" <directory> – Search recursively (case-insensitive) for a keyword inside files.
- cat <file_name> – Display the contents of a file.
- chmod +x <file> – Make a file executable.

## Git:

- git init – Initialize a directory as a Git repository.
- git clone <url> – Clone a repository from a remote URL.
- git add <file> – Stage a specific file for commit.
- git add . – Stage all modified files for commit.
- git status – Show the current state of the working directory and staging area.
- git commit -m "<message>" – Commit staged changes with a message.
- git push – Push committed changes to the remote repository.

