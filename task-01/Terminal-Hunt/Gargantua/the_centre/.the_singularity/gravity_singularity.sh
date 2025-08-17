read -s -p "Enter password to execute script: " USER_PASSWOR:D
echo

if [ "$USER_PASSWORD" == "$LOCA_LOCA" ]; then

	username=$(git config user.name)
	clear
	echo "Initializing final transmission..."
	sleep 1
	echo "Decrypting gravitational data from Gargantua..."
	sleep 1.5
	echo "Wormhole navigation logs verified."
	sleep 1
	echo "Mission status: ✅ SUCCESS"
	sleep 1
	echo
	echo "Time is relative, but your achievement is absolute."
	echo "After journeying through dust storms, wormholes, and habitable thresholds..."
	sleep 1
	echo "You've solved the final riddle, aligned the gravity equation, and made contact with Earth."
	sleep 1
	echo
	echo "🌌 A new chapter begins..."
	sleep 1.5
	echo
	typewriter() {
	    text="$1"
	    delay="${2:-0.04}"
	    for ((i=0; i<${#text}; i++)); do
		echo -n "${text:$i:1}"
		sleep "$delay"
	    done
	    echo
	}
	typewriter "🎉 Congratulations, $username!"
	sleep 1
	echo
	echo "You've successfully completed the Terminal Hunt and proved you're ready to explore the universe with"
	echo "
		                               .+++++++++===-     ...  ...          :=++=:       :=+=-
		                               .@@@@@@@@@@@@*    .---. ---:.     .%@@@@@@@@@: :@@@@@@@@@@
	    .:*%@@@%#=.   =***-.=#%#=..:+##+:. .@@@%==++++++-  .---:.   .---:.  .@@@@:  -%+. .@@@@: .=@=
	   :@@@@@##@@@@#  *@@@@@@@@@@@@@@@@@@% .@@@@***+++:  .---:.       .---:..%@@@@#=.    .%@@@%*=
		 .=%@@@@  *@@@@:  @@@@@. +@@@@:.@@@@@@@@@@- :---.           .---. =@@@@@@@@.   +@@@@@@@%
	   .#@@@@@%#@@@@  *@@@%   @@@@.  =@@@@-.@@@%======:  :---:.       .----.      :+@@@@.      :*@@@@
	   %@@@%    @@@@  *@@@%   @@@@.  =@@@@-.@@@%           .---:.   .----..  -@@*-.:%@@@. .@@*:.:@@@%
	   %@@@%    @@@@  *@@@%   @@@@.  =@@@@-.@@@%             .---. :---.     :@@@@@@@@@@. -@@@@@@@@@#
	   +@@@@@@@@@@@@  *@@@%  .@@@@.  =@@@@-.@@@%               .:. .:.          .:---.       .:--:.
	"
	sleep 2
	echo "This is just the beginning of your voyage. The stars await, but so does the codebase."
	sleep 2
	echo "Keep exploring, keep building — your journey with amFOSS has just begun  🚀"
	echo
	echo "Press 'q' to quit..."

	# Wait until user presses 'q'
	while true; do
	    read -n1 -s key
	    if [[ $key == "q" ]]; then
		break
	    fi
	done
else
    echo "Incorrect password"
    exit 1
fi
