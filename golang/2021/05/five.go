package main

import (
	"fmt"
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
	var lines []Line = FromList(input)
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

		for _, point := range line.Crossings() {
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
	var lines []Line = FromList(input)
	var output int = 0
	crossover := make(map[Point]int)

	for _, line := range lines {
		if !line.valid {
			continue
		}

		for _, point := range line.Crossings() {
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

func PrintBoard(lines []Line) string {
	output := make([][]int, 10)
	for i := 0; i < 10; i++ {
		for j := 0; j < 10; j++ {
			output[i] = append(output[i], 0)
		}
	}

	for _, line := range lines {
		if line.valid {
			var cross []Point = line.Crossings()
			for _, point := range cross {
				output[point.y][point.x] += 1
			}
		}
	}

	var stringy string = ""

	for _, row := range output {
		for _, column := range row {
			if column == 0 {
				stringy += "."
			} else {
				stringy += fmt.Sprintf("%d", column)
			}
		}
		stringy += "\n"
	}
	return stringy
}
