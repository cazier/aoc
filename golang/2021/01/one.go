package main

import (
	utils "main/utils"
	splits "main/utils/splits"
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

func PartOne(input string) (score int) {
	var depths []int = utils.StringToInt(splits.ByLine(input))

	for i := 1; i < len(depths); i++ {
		if depths[i-1] < depths[i] {
			score++
		}
	}
	return score
}

func PartTwo(input string) (score int) {
	var depths []int = utils.StringToInt(splits.ByLine(input))

	for i := 0; i < len(depths)-3; i++ {
		if utils.Sum(depths[i:i+3]) < utils.Sum(depths[i+1:i+4]) {
			score++
		}
	}
	return score
}

func main() {
	input, err := utils.LoadInput(2021, 01)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
