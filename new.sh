#! /bin/bash
source utils/shared.sh

usage() {
        echo "Usage: new.sh [option]..."
        echo "Create the files for a new day (and directory for a new year)."
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
        echo "-v, --version               print the package version and exit"
        echo "-V, --verbose               run in verbose mode, with more... logging?"
        echo "                             (Default: ${BOOL_MAP[${VERBOSE}]})"
}

debug_messages() {
        _debug_messages
}

do_thing() {
        source utils/system.sh

        case "$LANGUAGE_DIRECTORY" in
        "golang")
                source utils/golang.sh;;
        "python")
                source utils/python.sh;;
        *)
                _log_panic "Internal error"
                ;;
        esac

        _log_debug "Creating input and readme directories and files"
        _cmd "python ${_CWD}/utils/readme.py --year ${YEAR} --day ${DAY} --cookie ${_CWD}/.session_cookie --aoc-path ${_CWD} --log-level ERROR"

        DIR="${_CWD}/${LANGUAGE_DIRECTORY}/${YEAR}/${DAY}"
        _cmd "mkdir -p ${DIR}"

        README="${DIR}/README.md"

        if ! [[ -e "${README}" ]]; then
                _log_info "Adding a new readme file for ${YEAR}"
                _cmd "printf '${ANNUAL_README}' > ${README}"
        fi

        _log_debug "Creating code directories and files"
        _cmd "mkdir -p ${DIR}"
        if ! [[ -e "${DIR}/${TEST_NAME}" ]]; then
                _cmd "printf '${TEST_CODE}' > ${DIR}/${TEST_NAME}"
                _cmd "printf '${RUN_CODE}' > ${DIR}/${RUN_NAME}"
        else
                _log_panic "The files for '${LANGUAGE_DIRECTORY} ${YEAR}-${DAY}' already exist and will not be overwritten"
                exit 1
        fi

        _log_info "Succesfully created all the files. Get to work!"
}

CLI=$(getopt -o rthl:d:y:vV --long run,test,help,language:,day:,year:,verbose,version,dry-run -- "$@")
eval set -- "$CLI"
while true; do
        case "$1" in
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

_debug_messages

# Checking for necessary variables
_check_args

# Do the thing!
do_thing
