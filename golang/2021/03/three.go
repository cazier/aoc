package main

import (
	utils "main/utils"
	"main/utils/splits"
)

const sample_input string = `
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
`

func PartOne(input string) int {
	var report []string = splits.ByLine(input)
	var commands int = len(report)

	var width int = len(report[0])

	var values []int = make([]int, width)

	for _, command := range report {
		for index, value := range splits.ByCharacter(command) {
			if value == "1" {
				values[index] += 1
			}
		}
	}

	var gamma int = 0
	var epsilon int = 0

	for _, value := range values {
		if value >= commands/2 {
			gamma += 1
		} else {
			epsilon += 1
		}
		gamma <<= 1
		epsilon <<= 1
	}
	gamma >>= 1
	epsilon >>= 1
	return gamma * epsilon
}

func PartTwo(input string) int {
	var report []string = splits.ByLine(input)

	o2_func := func(i, j int) bool { return i >= j }
	o2_rating, _ := repeatPartTwo(report, o2_func)

	co2_func := func(i, j int) bool { return i < j }
	co2_rating, _ := repeatPartTwo(report, co2_func)

	return o2_rating * co2_rating
}

func repeatPartTwo(input []string, lookup func(int, int) bool) (int, error) {
	var slice []string = make([]string, len(input))
	copy(slice, input)
	var match string
	for index := 0; index < len(slice[0]); index++ {
		var count int = getValuesOfSliceAtIndex(slice, index)
		if lookup(count*2, len(slice)) {
			match = "1"
		} else {
			match = "0"
		}

		var slice_index int = 0

		for {
			if len(slice) == 1 {
				break
			}
			if slice_index >= len(slice) {
				break
			}

			var char string = string([]rune(slice[slice_index])[index])
			if char != match {
				slice = utils.RemoveSlow(slice, slice_index)
				slice_index -= 1
			}

			slice_index += 1
		}
	}
	return utils.ParseToInt(slice[0], 2, 16)
}
func getValuesOfSliceAtIndex(slice []string, index int) int {
	var count int = 0

	for _, command := range slice {
		if splits.ByCharacter(command)[index] == "1" {
			count += 1
		}
	}

	return count
}

func main() {
	input, err := utils.LoadInput(2021, 03)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
