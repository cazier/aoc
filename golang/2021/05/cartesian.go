package main

import (
	utils "main/utils"
	"main/utils/splits"
	"regexp"
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

func (l Line) Crossings() []Point {
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

func FromList(input string) []Line {
	var lines []string = splits.ByLine(input)
	var out []Line = make([]Line, len(lines))

	for index, line := range lines {
		out[index] = fromString(line)

	}
	return out
}
