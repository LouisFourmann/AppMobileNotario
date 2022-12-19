#!/bin/bash
PYTHON_FILE=./notario/manage.py
RED='\033[1;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN="\e[32m"
BOLD='\033[1m'
argv=$#
version_req="3.8"
checkPY=$(which python)
pyver=$(python -c 'import sys; print(".".join(map(str, sys.version_info[0:2])))')

function install_dependencies_python() {
    printf "${YELLOW} [INSTALLING DEPENDENCIES]${NC}\n"
    pip install -r requirements.txt | grep -v 'already satisfied'
    pip install pipenv
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt | grep -v 'already satisfied'
    printf "${GREEN} [REQUIREMENTS INSTALLED]${NC}\n"
}

function install_dependencies_python_3() {
    printf "${YELLOW} [INSTALLING DEPENDENCIES]${NC}\n"
    pip install -r requirements.txt | grep -v 'already satisfied'
    pip install pipenv
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt | grep -v 'already satisfied'
    printf "${GREEN} [REQUIREMENTS INSTALLED]${NC}\n"
}

function check_python3_version() {
    install_dependencies_python_3
    if [ -f "$PYTHON_FILE" ]; then
        python3 $PYTHON_FILE makemigrations
        python3 $PYTHON_FILE migrate
        printf "${GREEN} [SERVER MIGRATIONS DONE]${NC}\n"
        python3 $PYTHON_FILE runserver
    else
        printf "${RED}ERROR: ${NC}File $PYTHON_FILE does not exist."
    fi
}

function check_python_version() {
    if [ $checkPY >/dev/null ]; then
        if (( $(echo "$pyver < $version_req" | bc -l) )); then
            printf "${RED}ERROR: ${NC}Python is not on the right version.\n"
            printf "Please update python or run the following command to install all requirements with python3:\n ${BOLD}
            ${GREEN}./build.sh python3${NC}\n"
            exit 1
        else
            install_dependencies_python
            if [ -f "$PYTHON_FILE" ]; then
                python $PYTHON_FILE makemigrations
                python $PYTHON_FILE migrate
                printf "${GREEN} [SERVER MIGRATIONS DONE]${NC}\n"
                python $PYTHON_FILE runserver
            else
                printf "${RED}ERROR: ${NC}File $PYTHON_FILE does not exist."
            fi
        fi
    else
        printf "${RED} [PYTHON IS NOT INSTALLED]${NC}\n"
        printf "${RED} Try running ./build.sh python3${NC}\n"
    fi
}

if [ "$argv" -eq 0 ]; then
    printf "Your python version is: ${BOLD}python $pyver${NC}\n"
    check_python_version
fi
if [[ "$1" = "python3" ]]; then
    printf "Your python3 version is: ${BOLD} $pyver3${NC}\n"
    check_python3_version
fi