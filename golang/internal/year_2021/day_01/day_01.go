package main

import (
	"fmt"
	helpers "main/pkg/helpers"
	slices "main/pkg/slices"
	"os"
)

func PartOne() int {
	cwd, _ := os.Getwd()
	var data string = helpers.LoadInput(cwd, 2021, 01)
	var depths []int64 = slices.StringToInt(helpers.SplitLine(data))

	var increases int = 0

	for i := 1; i < len(depths); i++ {
		if depths[i-1] < depths[i] {
			increases++
		}
	}
	return increases
}

func PartTwo() int {
	cwd, _ := os.Getwd()
	var data string = helpers.LoadInput(cwd, 2021, 01)
	var depths []int64 = slices.StringToInt(helpers.SplitLine(data))

	var increases int = 0

	for i := 0; i < len(depths)-3; i++ {
		if slices.Sum(depths[i:i+3]) < slices.Sum(depths[i+1:i+4]) {
			increases++
		}
	}
	return increases
}

func main() {
	fmt.Println("Part One:", PartOne())
	fmt.Println("Part Two:", PartTwo())
}
