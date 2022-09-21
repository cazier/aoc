package main

import (
	"fmt"

	utils "main/utils"
)

func PartOne(input string) int {
	var depths []int64 = utils.StringToInt(utils.SplitLine(input))

	var increases int = 0

	for i := 1; i < len(depths); i++ {
		if depths[i-1] < depths[i] {
			increases++
		}
	}
	return increases
}

func PartTwo(input string) int {
	var depths []int64 = utils.StringToInt(utils.SplitLine(input))

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

	fmt.Println("Part One:", PartOne(input))
	fmt.Println("Part Two:", PartTwo(input))
}
