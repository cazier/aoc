package main

import (
	"fmt"
	helpers "main/internal"
	"os"
)

func part_one() int {
	cwd, _ := os.Getwd()
	var data string = helpers.LoadInput(cwd, 2021, 01)
	var depths []int64 = helpers.SliceStringToInt(helpers.SplitLine(data))

	var increases int = 0

	for i := 1; i < len(depths); i++ {
		if depths[i-1] < depths[i] {
			increases++
		}
	}
	return increases
}

func part_two() int {
	cwd, _ := os.Getwd()
	var data string = helpers.LoadInput(cwd, 2021, 01)
	var depths []int64 = helpers.SliceStringToInt(helpers.SplitLine(data))

	var increases int = 0

	for i := 0; i < len(depths)-3; i++ {
		if sum(depths[i:i+3]) < sum(depths[i+1:i+4]) {
			increases++
		}
	}
	return increases
}

func sum(values []int64) int64 {
	var total int64 = 0

	for i := 0; i < len(values); i++ {
		total += values[i]
	}
	return total

}

func main() {
	fmt.Println("Part One:", part_one())
	fmt.Println("Part Two:", part_two())
}
