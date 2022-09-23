package utils

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
)

// LoadInput reads the input file found at $AOC_ROOT_DIRECTORY/inputs and returns the value as a
// string.
func LoadInput(year int, day int) string {
	var root string = os.Getenv("AOC_ROOT_DIRECTORY")

	var year_string string = fmt.Sprintf("2%03d", year%2000)
	var day_string string = fmt.Sprintf("%02d.txt", day)

	path, err := filepath.Abs(filepath.Join(root, "inputs", year_string, day_string))

	if err != nil {
		panic(err)
	}

	contents, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	return string(contents)
}

// SplitLine takes a string input and breaks it into a slice of strings, split by any of the
// following newline characters: `\r`, `\n` The resulting slice is returned.
func SplitLine(input string) []string {
	pattern := regexp.MustCompile(`[\r\n]`)
	_splits := pattern.Split(input, -1)
	var output []string

	for _, v := range _splits {
		if len(v) > 0 {
			output = append(output, v)
		}
	}
	return output
}

// ParseToInt is a wrapper around strconv.ParseInt that casts the resulting integer to an `int` type
func ParseToInt(s string, base int, bitSize int) (i int, err error) {
	out, err := strconv.ParseInt(s, base, bitSize)

	return int(out), err
}
