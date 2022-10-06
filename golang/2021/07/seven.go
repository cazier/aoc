package main

import (
	"math"

	utils "main/utils"
	splits "main/utils/splits"
)

const sample_input string = `
16,1,2,0,4,2,7,1,2,14
`

func PartOne(input string) int {
	crabs := utils.StringToInt(splits.ByComma(utils.Strip(input)))
	min, max := utils.Min(crabs...), utils.Max(crabs...)

	var output int = math.MaxInt

	for start := min; start <= max; start++ {
		var fuel int = 0

		for _, crab := range crabs {
			var diff = utils.Abs(crab - start)
			fuel += diff
		}

		if fuel < output {
			output = fuel
		}
	}
	return output
}

func PartTwo(input string) int {
	crabs := utils.StringToInt(splits.ByComma(utils.Strip(input)))
	min, max := utils.Min(crabs...), utils.Max(crabs...)

	var output int = math.MaxInt

	for start := min; start <= max; start++ {
		var fuel int = 0

		for _, crab := range crabs {
			var diff = utils.Abs(crab - start)
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
	input, err := utils.LoadInput(2021, 07)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
