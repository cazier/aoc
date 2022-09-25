# Using values from envars or defaults
DAY=${DAY}
YEAR=${YEAR}
LANGUAGE=${LANGUAGE:-"go"}
VERBOSE=${VERBOSE:-0}
VERSION="1.0.0"
DRY_RUN=0

_CWD=$(cd $(dirname "$0") && pwd)

declare -A LANGUAGE_MAP=(
        ["go"]="golang"
        ["golang"]="golang"
        ["py"]="python"
        ["python"]="python"
)

declare -A DAY_NAME_MAP=(
        ["01"]="one"
        ["02"]="two"
        ["03"]="three"
        ["04"]="four"
        ["05"]="five"
        ["06"]="six"
        ["07"]="seven"
        ["08"]="eight"
        ["09"]="nine"
        ["10"]="ten"
        ["11"]="eleven"
        ["12"]="twelve"
        ["13"]="thirteen"
        ["14"]="fourteen"
        ["15"]="fifteen"
        ["16"]="sixteen"
        ["17"]="seventeen"
        ["18"]="eighteen"
        ["19"]="nineteen"
        ["20"]="twenty"
        ["21"]="twentyone"
        ["22"]="twentytwo"
        ["23"]="twentythree"
        ["24"]="twentyfour"
)

declare -A BOOL_MAP=(
        ["0"]=false
        ["1"]=true
)

_log_panic() {
        printf "\033[31m${*}"
        printf "\033[0m\n"
}

_log_debug() {
        if [[ $VERBOSE -eq 1 || $DRY_RUN -eq 1 || $2 == "force" ]]; then
                printf "\033[32m${1}"
                printf "\033[0m\n"
        fi
}

_days() {
        if [[ "$DAY" =~ [^0-9] || $DAY -gt 25 || $DAY -lt 1 ]]; then
                _log_panic "The day must be an integer between 1 and 25. (Got: ${DAY:-"null"})"

                return 1
        fi

        DAY=$(printf '%02d' "${DAY}")
        DAY_NAME=${DAY_NAME_MAP[$DAY]}

        return 0
}

_years() {
        if [[ "$YEAR" =~ [^0-9] || $YEAR -lt 2015 ]]; then
                _log_panic "The year must be an integer greater than 2015. (Got: ${YEAR:-"null"})"

                return 1
        fi

        _MOD=$(expr $YEAR % 2000)
        YEAR=$(printf '2%03d' ${_MOD})

        return 0
}

_languages() {
        LANGUAGE_DIRECTORY=${LANGUAGE_MAP[$LANGUAGE]}
        if [[ -z $LANGUAGE_DIRECTORY ]]; then
                _log_panic "The language must be one of go, golang, py, or python. (Got: ${LANGUAGE})"

                return 1
        fi

        return 0
}

_check_args() {
        if ! _days || ! _languages || ! _years; then
                usage
                exit 1
        fi
}

_change_directory() {
        _cmd "cd ${_CWD}/${LANGUAGE_DIRECTORY}/${YEAR}/${DAY}"
}

_cmd() {
        _log_debug "$ ${1}"
        if [[ $DRY_RUN -eq 0 ]]; then
                eval "${1}"
        fi
}

_debug_messages() {
        if [[ $VERBOSE -eq 1 || $DRY_RUN -eq 1 ]]; then
                printf "\033[33m"
                echo "Debug Messages:"
                echo -e "  DAY: $DAY"
                echo -e "  DAY_NAME: $DAY_NAME"
                echo -e "  LANGUAGE: $LANGUAGE"
                echo -e "  LANGUAGE_DIRECTORY: ${LANGUAGE_MAP[${LANGUAGE}]}"
                echo -e "  VERBOSE: ${BOOL_MAP[${VERBOSE}]}"
                echo -e "  DRY RUN: ${BOOL_MAP[${DRY_RUN}]}"
                echo -e "  CWD: ${_CWD}"

                if [[ -n "$1" ]]; then
                        echo -e "${1}"
                fi

                printf "\033[0m\n"
        fi
}
