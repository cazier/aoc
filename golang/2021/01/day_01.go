package main

import (
	"fmt"
	"os"

	utils "main/utils"
)

func PartOne() int {
	cwd, _ := os.Getwd()
	var data string = utils.LoadInput(cwd, 2021, 01)
	var depths []int64 = utils.StringToInt(utils.SplitLine(data))

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
	var data string = utils.LoadInput(cwd, 2021, 01)
	var depths []int64 = utils.StringToInt(utils.SplitLine(data))

	var increases int = 0

	for i := 0; i < len(depths)-3; i++ {
		if utils.Sum(depths[i:i+3]) < utils.Sum(depths[i+1:i+4]) {
			increases++
		}
	}
	return increases
}

func main() {
	fmt.Println("Part One:", PartOne())
	fmt.Println("Part Two:", PartTwo())
}
