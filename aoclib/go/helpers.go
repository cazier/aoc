package aoclib

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/cazier/aoclib/types"
	"github.com/fatih/color"
)

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

// Min returns the minimum Numeric value in a slice of values.
func Min[T types.Numeric](values ...T) T {
	var output T = values[0]
	for _, v := range values[1:] {
		if v < output {
			output = v
		}
	}
	return output
}

// Max returns the maximum Numeric value in a slice of values.
func Max[T types.Numeric](values ...T) T {
	var output T = values[0]
	for _, v := range values[1:] {
		if v > output {
			output = v
		}
	}
	return output
}

// Abs returns an absolute value for a generic Numeric type.
func Abs[T types.Numeric](val T) T {
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
