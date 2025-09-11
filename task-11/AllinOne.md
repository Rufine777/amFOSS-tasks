### Level 0 → 1  

**Commands:**  
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
ls
cat readme
Password: ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If


### Level 1 → 2  

**Commands:**  
```bash
ssh bandit1@bandit.labs.overthewire.org -p 2220
ls -a
cat ./-
Password: 263JGJPfgU6LtdEvgfWU1XP5yac29mFx

### Level 2 → 3  

**Commands:**  
```bash
ssh bandit2@bandit.labs.overthewire.org -p 2220
ls -a
cat ./--spaces\ in\ this\ filename--
password: MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx


### Level 3 → 4  

**Commands:**  
```bash
ls -a
cd inhere
ls -a
cat ...Hiding-From-You
Password: 2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ

### Level 4 → 5  

**Commands:**  
```bash
ssh bandit4@bandit.labs.overthewire.org -p 2220
ls -a
cd inhere
file ./*
cat ./-file07
Password: 4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw

### Level 5 → 6

**Commands:**

find . -type f -size 1033c
cat ./inhere/maybehere07/.file2


Password: HWasnPhtq9AVKe0dmk45nxy20cvUa6EG

### Level 6 → 7

**Commands:**

find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password


Password: morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj

### Level 7 → 8

**Commands:**

grep millionth data.txt


Password: dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc

### Level 8 → 9

**Commands:**

sort data.txt | uniq -u


Password: 4CKMh1JI91bUIZZPXDqGanal4xvAg0JM

### Level 9 → 10

**Commands:**

strings data.txt


Password: FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey

### Level 10 → 11

**Commands:**

base64 -d data.txt


Password: dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr


### Level 11 → 12

**Commands:**

cat data.txt 
Gur cnffjbeq vf 7k16JArUVv5LxVuJfsSVdbbtaHGlw9D4

used https://cryptii.com/pipes/rot13-decoder

The password is 7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4

### Level 12 → 13
**Commands:**
```bash
tmpdir=$(mktemp -d)
cd $tmpdir
cp ~/data.txt .
xxd -r data.txt data.bin
gzip -dc data.bin > data2.bin
bzip2 -dc data2.bin > data3.bin
gzip -dc data3.bin > data4.bin
tar -xf data4.bin
tar -xf data5.bin
bzip2 -dc data6.bin > data7.bin
tar -xf data7.bin
gzip -dc data8.bin > data9.bin
cat data9.bin'''

### Level 13 → 14  

**Commands:**  
```bash
chmod 600 sshkey.private
ssh -i sshkey.private -p 2220 bandit14@localhost'''
Password: (SSH key used, no password)

### Level 14 → 15

**Commands:**

cat /etc/bandit_pass/bandit14 | nc localhost 30000


Password: 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo
