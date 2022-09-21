#! /bin/bash
# Using values from envars or defaults
DAY=${DAY}
LANGUAGE=${LANGUAGE:-"go"}
RUN=0
TEST=0
VERBOSE=${VERBOSE:-0}
VERSION="1.0.0"
DRY_RUN=1

_CWD=$(pwd)

declare -A LANGUAGE_MAP=(
        ["go"]="golang"
        ["golang"]="golang"
        ["py"]="python"
        ["python"]="python"
)

declare -A BOOL_MAP=(
        ["0"]=false
        ["1"]=true
)

usage() {
        echo "Usage: run.sh [option]..."
        echo "Run a particular day, from within a directory, written in the"
        echo "specified programming language."
        echo ""
        echo "Real Arguments (can be passed into the CLI with short or long forms,"
        echo " or as environment variables):"
        echo "-d, --day, DAY              aoc puzzle day (required)"
        echo "-l, --language, LANGUAGE    programming language (Default: go)"
        echo ""
        echo "Other Arguments"
        echo "--dry-run                   only do a dry-run without actually executing"
        echo "                             anything (Default: ${BOOL_MAP[${DRY_RUN}]})"
        echo "-h, --help                  print this usage message and exit"
        echo "-r, --run                   run the day for submittal/with input data"
        echo "                             (Default: ${BOOL_MAP[${RUN}]})"
        echo "-t, --test                  run the day with the sample values to test"
        echo "                             (Default: ${BOOL_MAP[${TEST}]})"
        echo "-v, --version               print the package version and exit"
        echo "-V, --verbose               run in verbose mode, with more... logging?"
        echo "                             (Default: ${BOOL_MAP[${VERBOSE}]})"
}

debug_messages() {
        if [[ $VERBOSE -eq 1 || $DRY_RUN -eq 1 ]]; then
                echo "Debug Messages:"
                echo -e "  DAY: $DAY"
                echo -e "  LANGUAGE: $LANGUAGE"
                echo -e "  LANGUAGE_DIRECTORY: ${LANGUAGE_MAP[${LANGUAGE}]}"
                echo -e "  RUN: ${BOOL_MAP[${RUN}]}"
                echo -e "  TEST: ${BOOL_MAP[${TEST}]}"
                echo -e "  VERBOSE: ${BOOL_MAP[${VERBOSE}]}"
                echo -e "  DRY RUN: ${BOOL_MAP[${DRY_RUN}]}"
                echo -e "  CWD: ${_CWD}"
        fi
}

log_panic() {
        printf "\033[31m${*}"
        printf "\033[0m\n"
}

log_debug() {
        if [[ $VERBOSE -eq 1 || $DRY_RUN -eq 1 ]]; then
                printf "\033[32m${*}"
                printf "\033[0m\n"
        fi
}

days() {
        if [[ "$DAY" =~ [^0-9] || $DAY -gt 25 || $DAY -lt 1 ]]; then
                log_panic "The day must be an integer between 1 and 25. (Got: ${DAY:-"null"})"

                return 1
        fi

        DAY=$(printf '%02d' "${DAY}")

        return 0
}
languages() {
        LANGUAGE_DIRECTORY=${LANGUAGE_MAP[$LANGUAGE]}
        if [[ -z $LANGUAGE_DIRECTORY ]]; then
                log_panic "The language must be one of go, golang, py, or python. (Got: ${LANGUAGE})"

                return 1
        fi

        return 0
}

check_args() {
        if ! days || ! languages; then
                usage
                exit 1
        fi
}

change_directory() {
        cmd "cd ${_CWD}/${LANGUAGE_DIRECTORY}/${DAY}"
}

cmd() {
        log_debug "$ ${1}"
        if [[ $DRY_RUN -eq 0 ]]; then
                eval $1
        fi
}

do_thing() {
        case "$LANGUAGE_DIRECTORY" in
        "golang")
                cmd "go test ."
                ;;
        "python")
                cmd "python -m unittest ."
                ;;
        *)
                log_panic "Internal error"
                ;;
        esac
}

CLI=$(getopt -o rthl:d:vV --long run,test,help,language:,day:,verbose,version,dry-run -- "$@")
eval set -- "$CLI"
while true; do
        case "$1" in
        -r | --run)
                RUN=1
                shift
                ;;
        -t | --test)
                TEST=1
                shift
                ;;
        -h | --help)
                usage
                exit 0
                ;;
        -l | --language)
                LANGUAGE=$2
                shift 2
                ;;
        -d | --day)
                DAY=$2
                shift 2
                ;;
        -v | --verbose)
                VERBOSE=1
                shift
                ;;
        -V | --version)
                echo "Version: ${VERSION}"
                exit 0
                ;;
        --dry-run)
                DRY_RUN=1
                shift
                ;;
        --)
                check_args
                shift
                break
                ;;
        *)
                usage
                exit 1
                ;;
        esac
done

debug_messages

# Checking for necessary variables
check_args

# Switching into proper directory
change_directory

# Do the thing!
do_thing
