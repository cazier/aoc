package main

import (
	utils "main/utils"
)

const sample_input string = `
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
`

func PartOne(input string) int {
	var lines []Line = fromList(input)
	var output int = 0
	crossover := make(map[Point]int)

	for index, line := range lines {
		if line.start.x != line.stop.x && line.start.y != line.stop.y {
			lines[index].valid = false
		}
	}

	for _, line := range lines {
		if !line.valid {
			continue
		}

		for _, point := range line.crossings() {
			crossover[point] += 1
		}
	}

	for _, point := range crossover {
		if point >= 2 {
			output += 1
		}
	}

	return output
}

func PartTwo(input string) int {
	var lines []Line = fromList(input)
	var output int = 0
	crossover := make(map[Point]int)

	for _, line := range lines {
		if !line.valid {
			continue
		}

		for _, point := range line.crossings() {
			crossover[point] += 1
		}
	}

	for _, point := range crossover {
		if point >= 2 {
			output += 1
		}
	}

	return output
}

func main() {
	input, err := utils.LoadInput(2021, 05)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
