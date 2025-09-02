# Task 02: The Cyberpunk Syndicate
***Review:***  *Easier than Task 1. The questions were mostly straightforward, but careful reading was key. Question 5 took significantly longer than the others combined*.
> I initially chose C programming by mistake, but after completing the task, I realized that implementing it in Python would have been much simpler and more efficient.
## Question 1: Codeforces contest
Straightforward problem — solved using a ternary operator inside a loop.

## Question 2: Insurance
Another direct question, handled with ternary operator and loop.

## Question 3: Mine Gold
Simple in concept, but I initially made the mistake of excluding Yousuf and only counting his friends, which cost some time. Used ternary operator and loop for the final solution.

## Question 4: Big Hotel
Main challenge was figuring out the equation to find the floor number; once that was done, the rest was easy.

## Question 5: Escape false alarm
This was the most time-consuming part. Time spent on this single question was more than the first four combined.

 - My first idea: iterate through each door, and when Ravi reaches the first closed door, activate the button and start a countdown. Once the countdown ends, the doors revert to their original state; if a closed door appears after that, print “NO” and break.

 - This approach led to a long code, so I tried to find a shorter solution — but after wasting time, I went back to my first approach with minor optimizations. The result was still relatively long,   but it worked

## Question 6: Remove card
After reading the problem and analyzing the expected output, I realized that to minimize the number of moves (removing cards), I needed to subtract the maximum frequency of any number from the total number of cards. To find this frequency, I used the array-based counting method in C, and the rest was straightforward—I simply printed N - maxFreq.
