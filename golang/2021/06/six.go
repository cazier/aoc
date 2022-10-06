package main

import (
	"regexp"

	utils "main/utils"
	"main/utils/splits"
)

const sample_input string = `
3,4,3,1,2
`

func PartOne(input string) int {
	fishes := fromString(utils.Strip(input))
	return run(fishes, 80)
}

func PartTwo(input string) int {
	fishes := fromString(utils.Strip(input))
	return run(fishes, 256)
}

func main() {
	input, err := utils.LoadInput(2021, 06)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}

func run(input map[int]int, days int) int {
	for i := 0; i < days; i++ {
		var update map[int]int = make(map[int]int)
		for age := 0; age < 9; age++ {
			var count int = input[age]
			if age == 0 {
				update[6] += count
				update[8] += count
			} else {
				update[age-1] += count
			}
		}
		input = update
	}

	var output int = 0
	for _, num := range input {
		output += num
	}
	return output
}

func fromString(input string) map[int]int {
	splits := splits.ByRegexp(input, regexp.MustCompile(`,`))
	var days []int = utils.StringToInt(splits)

	var output map[int]int = make(map[int]int)

	for _, age := range days {
		output[age] += 1
	}

	return output
}
