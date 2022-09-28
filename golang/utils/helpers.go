package utils

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"

	"github.com/fatih/color"
)

// LoadInput reads the input file found at $AOC_ROOT_DIRECTORY/inputs and returns the value as a
// string.
func LoadInput(year int, day int) string {
	var root string = os.Getenv("AOC_ROOT_DIRECTORY")

	if root == "" {
		color.Red("Could not determine the proper $AOC_ROOT_DIRECTORY environment variable.")
		os.Exit(1)
	}

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

// SplitByLine takes a string input and breaks it into a slice of strings, split by any of the
// following newline characters: `\r`, `\n` The resulting slice is returned.
func SplitByLine(input string) []string {
	var pattern *regexp.Regexp = regexp.MustCompile(`[\r\n]`)
	return SplitStringByPattern(input, pattern)
}

// SplitByCharacter takes a string input breaks into a slice with an element for each character,
// which is then returned
func SplitByCharacter(input string) []string {
	var pattern *regexp.Regexp = regexp.MustCompile(``)
	return SplitStringByPattern(input, pattern)
}

// SplitStringByPattern takes an arbitrary string and splits it by a regular expression pattern. The
// resulting slice is returned.
func SplitStringByPattern(input string, pattern *regexp.Regexp) []string {
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

// Answer wraps the answer from a regular section just so that it can get printed in pretty blue
func Answer(s string, a ...any) {
	fmt.Println(color.BlueString(s, a...))
}

// NumRange creates a slice with the integer values listed from start to stop, with a step size of
// one. The range can be ascending or descending, and positive/negative, depending on the input
// parameters.
func NumRange(start, stop int) []int {
	var step, num int

	if stop > start {
		step = 1
		num = stop - start
	} else {
		step = -1
		num = start - stop
	}

	var output []int = make([]int, num)
	for i := 0; i < num; i++ {
		output[i] = start + (step * i)
	}

	return output
}
