package main

import (
	"fmt"
	"regexp"

	utils "main/utils"
	splits "main/utils/splits"
)

type Point struct {
	x int
	y int
}

type Line struct {
	start Point
	stop  Point
	valid bool
}

func (l Line) crossings() []Point {
	var length int = utils.Max(utils.Abs(l.start.x-l.stop.x), utils.Abs(l.start.y-l.stop.y))
	var output []Point = make([]Point, length+1)

	var x_step, y_step int = 1, 1

	if l.stop.x < l.start.x {
		x_step = -1
	} else if l.stop.x == l.start.x {
		x_step = 0
	}

	if l.stop.y < l.start.y {
		y_step = -1
	} else if l.stop.y == l.start.y {
		y_step = 0
	}

	for index := 0; index <= length; index++ {
		output[index] = Point{l.start.x + (index * x_step), l.start.y + (index * y_step)}
	}

	return output
}

func fromString(input string) Line {
	var line []string = splits.ByRegexp(input, regexp.MustCompile(` -> `))
	var start_split []int = utils.StringToInt(splits.ByRegexp(line[0], regexp.MustCompile((`,`))))
	var stop_split []int = utils.StringToInt(splits.ByRegexp(line[1], regexp.MustCompile((`,`))))

	return Line{
		Point{start_split[0], start_split[1]},
		Point{stop_split[0], stop_split[1]},
		true,
	}
}

func fromList(input string) []Line {
	var lines []string = splits.ByLine(input)
	var out []Line = make([]Line, len(lines))

	for index, line := range lines {
		out[index] = fromString(line)

	}
	return out
}

func printBoard(lines []Line) string {
	output := make([][]int, 10)
	for i := 0; i < 10; i++ {
		for j := 0; j < 10; j++ {
			output[i] = append(output[i], 0)
		}
	}

	for _, line := range lines {
		if line.valid {
			var cross []Point = line.crossings()
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
