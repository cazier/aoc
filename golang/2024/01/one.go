package main

import (
	utils "main/utils"
	"main/utils/splits"
	"regexp"
	"sort"
)

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
		output = append(output, utils.StringToInt(values))
	}
	return output
}

func PartOne(input string) int {
	result := 0
	columns := utils.Zip(parse(input)...)

	left := columns[0]
	right := columns[1]

	sort.Ints(left)
	sort.Ints(right)

	for row, value := range left {
		result += utils.Abs(value - right[row])
	}

	return result
}

func PartTwo(input string) int {
	result := 0
	columns := utils.Zip(parse(input)...)

	left := columns[0]
	right := columns[1]

	for _, value := range left {
		result += (value * utils.Count(right, value))
	}

	return result
}

func main() {
	input, err := utils.LoadInput(2024, 01)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
