package utils

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"

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

	path, _ := filepath.Abs(filepath.Join(root, "inputs", year_string, day_string))

	contents, _ := os.ReadFile(path)

	return string(contents)
}

// ParseToInt is a wrapper around strconv.ParseInt that casts the resulting integer to an `int` type
func ParseToInt(s string, base int, bitSize int) (i int, err error) {
	out, err := strconv.ParseInt(s, base, bitSize)

	return int(out), err
}

// B10toI is a further wrapper around strconv.ParseInt that casts the resulting integer to an `int`
// type, assumes the string is base-10, and panics on errors.
func B10toI(s string) (i int) {
	out, err := strconv.ParseInt(s, 10, 32)

	if err != nil {
		panic(err)
	}

	return int(out)
}

// Answer wraps the answer from a regular section just so that it can get printed in pretty blue
func Answer(s string, a ...any) {
	fmt.Println(color.BlueString(s, a...))
}

// NumRange creates an iterator with the integer values listed from start to stop, with a step size of
// one. The range can be ascending or descending, and positive/negative, depending on the input
// parameters.
func NumRange(start, stop int) <-chan int {
	var step int

	if stop > start {
		step = 1
	} else {
		step = -1
	}

	channel := make(chan int)

	go func() {
		for i := start; i < stop; i += step {
			channel <- i
		}
	}()

	return channel
}

// Min returns the minimum Numeric value in a slice of values.
func Min[T Numeric](values ...T) T {
	var output T = values[0]
	for _, v := range values[1:] {
		if v < output {
			output = v
		}
	}
	return output
}

// Max returns the maximum Numeric value in a slice of values.
func Max[T Numeric](values ...T) T {
	var output T = values[0]
	for _, v := range values[1:] {
		if v > output {
			output = v
		}
	}
	return output
}

// Abs returns an absolute value for a generic Numeric type.
func Abs[T Numeric](val T) T {
	var output T
	var zero T

	if val < zero {
		output = zero - val
	} else {
		output = val
	}

	return output
}

// Strip removes any whitespace (including newlines) at the beginning or end of a string
func Strip(input string) string {
	return strings.TrimSpace(input)
}
