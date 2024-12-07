package main

import (
	_ "embed"
	"regexp"
	"sort"

	aoclib "github.com/cazier/aoclib"
	"github.com/cazier/aoclib/splits"
)

//go:embed input
var input string

const sample_input string = `
3   4
4   3
2   5
1   3
3   9
3   3
`

func parse(inputs string) [][]int {
	var output [][]int

	for _, line := range splits.ByLine(inputs) {
		values := splits.ByRegexp(line, regexp.MustCompile(`[\s+]`))
		output = append(output, aoclib.StringToInt(values))
	}
	return output
}

func PartOne(input string) int {
	result := 0
	columns := aoclib.Zip(parse(input)...)

	left := columns[0]
	right := columns[1]

	sort.Ints(left)
	sort.Ints(right)

	for row, value := range left {
		result += aoclib.Abs(value - right[row])
	}

	return result
}

func PartTwo(input string) int {
	result := 0
	columns := aoclib.Zip(parse(input)...)

	left := columns[0]
	right := columns[1]

	for _, value := range left {
		result += (value * aoclib.Count(right, value))
	}

	return result
}

func main() {
	aoclib.Answer("Part One: %d", PartOne(input))
	aoclib.Answer("Part Two: %d", PartTwo(input))
}
