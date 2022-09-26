package main

import (
	utils "main/utils"
)

const sample_input string = `
199
200
208
210
200
207
240
269
260
263
`

func PartOne(input string) int {
	var depths []int = utils.StringToInt(utils.SplitByLine(input))

	var increases int = 0

	for i := 1; i < len(depths); i++ {
		if depths[i-1] < depths[i] {
			increases++
		}
	}
	return increases
}

func PartTwo(input string) int {
	var depths []int = utils.StringToInt(utils.SplitByLine(input))

	var increases int = 0

	for i := 0; i < len(depths)-3; i++ {
		if utils.Sum(depths[i:i+3]) < utils.Sum(depths[i+1:i+4]) {
			increases++
		}
	}
	return increases
}

func main() {
	var input string = utils.LoadInput(2021, 01)

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
