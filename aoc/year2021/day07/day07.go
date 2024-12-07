package main

import (
	_ "embed"
	"math"

	aoclib "github.com/cazier/aoclib"
	"github.com/cazier/aoclib/splits"
)

//go:embed input
var input string

const sample_input string = `
16,1,2,0,4,2,7,1,2,14
`

func PartOne(input string) int {
	crabs := aoclib.StringToInt(splits.ByComma(aoclib.Strip(input)))
	min, max := aoclib.Min(crabs...), aoclib.Max(crabs...)

	var output int = math.MaxInt

	for start := min; start <= max; start++ {
		var fuel int = 0

		for _, crab := range crabs {
			var diff = aoclib.Abs(crab - start)
			fuel += diff
		}

		if fuel < output {
			output = fuel
		}
	}
	return output
}

func PartTwo(input string) int {
	crabs := aoclib.StringToInt(splits.ByComma(aoclib.Strip(input)))
	min, max := aoclib.Min(crabs...), aoclib.Max(crabs...)

	var output int = math.MaxInt

	for start := min; start <= max; start++ {
		var fuel int = 0

		for _, crab := range crabs {
			var diff = aoclib.Abs(crab - start)
			fuel += cumulative_sum(diff)
		}

		if fuel < output {
			output = fuel
		}
	}
	return output
}

func cumulative_sum(num int) int {
	return (num + 1) * num / 2
}

func main() {
	aoclib.Answer("Part One: %d", PartOne(input))
	aoclib.Answer("Part Two: %d", PartTwo(input))
}
