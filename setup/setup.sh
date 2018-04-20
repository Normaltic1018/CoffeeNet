#!/bin/bash

arch="$(uname -m)"
silent=false
os="$(awk -F '=' '/^ID=/ {print $2}' /etc/os-release 2>&-)"
version="$(awk -F '=' '/^VERSION_ID=/ {print $2}' /etc/os-release 2>&-)"
arg=""
errors=""
runuser="$(whoami)"

if [ "${os}" == "ubuntu" ] || [ "${os}" == "arch" ] || [ "${os}" == "blackarch" ] || [ "${os}" == "debian" ] || [ "${os}" == '"elementary"' ] || [ "${os}" == "deepin" ] || [ "${os}" == "linuxmint" ] ; then
  trueuser="$(who | tr -d '\n' | cut -d' ' -f1)"
else
  trueuser="$(who am i | cut -d' ' -f1)" # If this is blank, we're actually root (kali)
fi

if [ "${runuser}" == "root" ] && [ "${trueuser}" == "" ]; then
  trueuser="root"
fi

if [ "${trueuser}" != "root" ]; then
  userhomedir="$(echo /home/${trueuser})"
else
  userhomedir="${HOME}"
fi

BOLD="\033[01;01m"     # Highlight
RED="\033[01;31m"      # Issues/Errors
GREEN="\033[01;32m"    # Success
YELLOW="\033[01;33m"   # Warnings/Information
RESET="\033[00m"       # Normal

# Title function
func_title(){
  # Echo title
  echo " =========================================================================="
  echo "                  CoffeeNet (Setup Script) | [Updated]: 2018-04-20"
  echo " =========================================================================="
  echo "  [Author]: Normaltic                    | [email]: rlagkstn1426@naver.com"
  echo " =========================================================================="
  echo ""
}

# Trap
function ctrl_c() {
	echo -e "\n${RED}Exit... Bye!${RESET}\n"
	exit 2
}

# Environment Checks
func_check_env() {
  # Check sudo dependency
  which sudo >/dev/null 2>&-
  if [ "$?" -ne "0" ]; then
    echo ""
    echo -e " ${RED}[ERROR]: This setup script requires sudo!${RESET}"
    echo "          Please install and configure sudo then run this setup again."
    echo "          Example: For Debian/Ubuntu: apt-get -y install sudo"
    echo "                   For Fedora 22+: dnf -y install sudo"
    exit 1
  fi

  if [ "${silent}" == "true" ]; then
    echo -e "\n [?] ${BOLD}Are you sure you wish to install CoffeeNet?${RESET}\n"
    echo -e "     Continue with installation? ([${BOLD}y${RESET}]/[${GREEN}S${RESET}]ilent/[${BOLD}n${RESET}]o): ${GREEN}S${RESET}"
  else
    echo -e "\n [?] ${BOLD}Are you sure you wish to install CoffeeNet?${RESET}\n"
    read -p '     Continue with installation? ([y]/[s]ilent/[N]o): ' installcoffee
    if [ "${installcoffee}" == 's' ]; then
      silent=true
    elif [ "${installcoffee}" != 'y' ]; then
      echo -e "\n ${RED}[ERROR]: Installation aborted by user.${RESET}\n"
      exit 1
    fi
  fi

  if command -v python3 &> /dev/null;then
	  # Python 3 is installed
	  echo -e "\n [*] ${YELLOW}Python 3 is installed ${RESET}\n"
  else
	  # Python 3 is not installed
	  sudo apt-get -y install python3
	  tmp="$?"
	  if [ "${tmp}" -ne "0" ]; then
		  msg="Failed to install dependencies (Python3)...Exit code: ${tmp}"
		  errors="${errors}\n${msg}"
		  echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
		  exit 1
	  fi
	  echo -e "\n [*] ${YELLOW}Python 3 is installed ${RESET}\n"
  fi

  if ! [ -x "$(command -v pip3)" ]; then
	  # pip3 is not installed.
	  sudo apt-get -y install python3-pip
	  tmp="$?"
	  if [ "${tmp}" -ne "0" ]; then
		  msg="Failed to install dependencies (pip3)...Exit code: ${tmp}"
		  errors="${errors}\n${msg}"
		  echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
		  exit 1
	  fi
	  echo -e "\n [*] ${YELLOW}pip3 is installed ${RESET}\n"
  else
	  echo -e "\n [*] ${YELLOW}pip3 is installed ${RESET}\n"
  fi

  if ! [ -x "$(command -v nmap)" ]; then
	  # nmap is not installed.
	  sudo apt-get -y install nmap
	  tmp="$?"
	  if [ "${tmp}" -ne "0" ]; then
		  msg="Failed to install dependencies (nmap)...Exit code: ${tmp}"
		  errors="${errors}\n${msg}"
		  echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
		  exit 1
	  fi
	  echo -e "\n [*] ${YELLOW}nmap is installed ${RESET}\n"
  else
	  echo -e "\n [*] ${YELLOW}nmap is installed ${RESET}\n"
  fi
  func_python_deps
}

func_python_deps(){
	cat python_deps | \
	while read line
	do
		if python3 -c "import ${line}" $> /dev/null;then
	  		echo -e "\n [*] ${YELLOW}${line} is installed ${RESET}\n"
		else
			if [ "$line" == "nmap" ]; then
			       sudo pip3 install python-nmap
		        else
		 		sudo pip3 install ${line} 		
			fi
	  		tmp="$?"
	  		if [ "${tmp}" -ne "0" ]; then
		  		msg="Failed to install python dependencies (${line})...Exit code: ${tmp}"
		  		errors="${errors}\n${msg}"
		  		echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
		  		exit 1
	  		fi
	  		echo -e "\n [*] ${YELLOW}${line} is installed ${RESET}\n"
		fi
	done
}

func_title

trap ctrl_c INT

# Menu case statement
case $1 in
  # Make sure not to nag the user
  -s|--silent)
  silent=true
  func_check_env
  ;;

  # Print help menu
  -h|--help)
  echo ""
  echo "  [Usage]....: ${0} [OPTIONAL]"
  echo "  [Optional].:"
  echo "               -s|--silent   = Automates the installation"
  echo "               -h|--help     = Show this help menu"
  echo ""
  exit 0
  ;;

  # Run standard setup
  "")
  func_check_env
  ;;

*)
  echo -e "\n\n ${RED}[ERROR] Unknown option: $1${RESET}\n"
  exit 1
  ;;
esac

if [ "${errors}" != "" ]; then
  echo -e " ${RED} There was issues installing the following:${RESET}\n"
  echo -e " ${BOLD}${errors}${RESET}\n"
fi

echo -e "\n [I] ${GREEN}Done!${RESET}\n"
exit 0
