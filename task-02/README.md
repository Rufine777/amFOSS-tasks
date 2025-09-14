# Task 02: The Cyberpunk Syndicate
***Review:***  *Easier than Task 1. The questions were mostly straightforward, but careful reading was key. Question 5 took significantly longer than the others combined*.
> I initially chose C programming by mistake, but after completing the task, I realized that implementing it in Python would have been much simpler and more efficient.
## Question 1: Codeforces contest
After reading the problem and analyzing the expected output, I realized that I only needed to check whether Chef’s rank was within the top 10. To handle multiple test cases, I used a loop. For each test case, I applied a ternary operator to check the condition (X <= 10) and directly printed "YES" or "NO" accordingly.
## Question 2: Insurance
After reading the problem and analyzing the expected output, I realized that the amount rebated is always the minimum of the repair cost and the maximum coverage. If the repair cost is less than or equal to the maximum rebate, then the entire repair cost is covered; otherwise, only the maximum rebate is given. To implement this, I used a loop to handle multiple test cases and applied a ternary operator to directly print the smaller value between X and Y.

## Question 3: Mine Gold
After reading the problem and analyzing the expected output, I understood that the total carrying capacity of the team is (N + 1) * Y, since Rohan also joins his N friends. To determine if they can carry all the gold, I needed to check whether the total gold X is less than or equal to this combined capacity. If X <= (N+1)*Y, the answer is "YES", otherwise "NO". To implement this, I used a loop to handle multiple test cases and applied a simple conditional check for each.

## Question 4: Big Hotel
After reading the problem, I realized that each room number can be converted into its floor by (room - 1)/10 + 1. Once I find the floor numbers of Raju and Ravi, the number of floors Raju needs to travel is simply the absolute difference between them. I used a loop for multiple test cases and printed the result.

## Question 5: Escape false alarm
This was the most time-consuming part. Time spent on this single question was more than the first four combined.

 - My first idea: iterate through each door, and when Ravi reaches the first closed door, activate the button and start a countdown. Once the countdown ends, the doors revert to their original state; if a closed door appears after that, print “NO” and break.

 - This approach led to a long code, so I tried to find a shorter solution — but after wasting time, I went back to my first approach with minor optimizations. The result was still relatively long,   but it worked

## Question 6: Remove card
After reading the problem and analyzing the expected output, I realized that to minimize the number of moves (removing cards), I needed to subtract the maximum frequency of any number from the total number of cards. To find this frequency, I used the array-based counting method in C, and the rest was straightforward—I simply printed N - maxFreq.
