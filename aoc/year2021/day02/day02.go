package main

import (
	_ "embed"
	"fmt"
	"strings"

	"github.com/cazier/aoclib"
	"github.com/cazier/aoclib/splits"
)

//go:embed input
var input string

const sample_input string = `
forward 5
down 5
forward 8
up 3
down 8
forward 2
`

func PartOne(input string) int {
	var commands []string = splits.ByLine(input)

	var x int = 0
	var y int = 0

	for _, v := range commands {
		splits := strings.SplitN(v, " ", 2)

		direction := splits[0]
		amount, _ := aoclib.ParseToInt(splits[1], 10, 64)

		switch direction {
		case "forward":
			x += amount
		case "up":
			y -= amount
		case "down":
			y += amount
		default:
			panic("Something went wrong sorry")
		}
	}
	return x * y
}

func PartTwo(input string) int {
	var commands []string = splits.ByLine(input)

	var x int = 0
	var y int = 0
	var aim int = 0

	for _, v := range commands {
		splits := strings.SplitN(v, " ", 2)

		direction := splits[0]
		amount, _ := aoclib.ParseToInt(splits[1], 10, 64)

		switch direction {
		case "forward":
			x += amount
			y += aim * amount
		case "up":
			aim -= amount
		case "down":
			aim += amount
		default:
			panic("Something went wrong sorry")
		}
		fmt.Print()
	}
	return x * y
}

func main() {
	aoclib.Answer("Part One: %d", PartOne(input))
	aoclib.Answer("Part Two: %d", PartTwo(input))
}
