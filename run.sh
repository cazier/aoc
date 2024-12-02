#! /bin/bash
source system/shared.sh

RUN=0
TEST=0

usage() {
        echo "Usage: run.sh [option]..."
        echo "Run a particular day, from within a directory, written in the"
        echo "specified programming language."
        echo ""
        echo "Real Arguments (can be passed into the CLI with short or long forms,"
        echo " or as environment variables):"
        echo "-d, --day, DAY              aoc puzzle day (required)"
        echo "-y, --year, YEAR            aoc puzzle year (required)"
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

do_thing() {
        case "$LANGUAGE_DIRECTORY" in
        "golang")
                source system/golang.sh
                _change_directory

                if [[ $RUN -eq 1 ]]; then
                    _cmd "go run ."
                fi
                if [[ $TEST -eq 1 ]]; then
                    _cmd "go test ."
                fi
                ;;
        "python")
                export PYTHONPATH="${AOC_ROOT_DIRECTORY}/python"
                source system/python.sh
                _change_directory

                if [[ $RUN -eq 1 ]]; then
                    _cmd "python main.py"
                fi
                if [[ $TEST -eq 1 ]]; then
                    _cmd "ward test -p test_main.py"
                fi
                ;;
        *)
                _log_panic "Internal error"
                ;;
        esac
}

CLI=$(getopt -o rthl:ad:y:vV --long run,test,help,language:,auto,day:,year:,verbose,version,dry-run -- "$@")
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
        -a | --auto)
                AUTO=1
                shift
                ;;
        -d | --day)
                DAY=$2
                shift 2
                ;;
        -y | --year)
                YEAR=$2
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
                _check_args
                shift
                break
                ;;
        *)
                usage
                exit 1
                ;;
        esac
done

_debug_messages "  VERBOSE: ${BOOL_MAP[${VERBOSE}]}\n  DRY RUN: ${BOOL_MAP[${DRY_RUN}]}"

# Checking for necessary variables
_check_args

# Do the thing!
do_thing
