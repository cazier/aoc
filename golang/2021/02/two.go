package main

import (
	"fmt"
	"regexp"

	utils "main/utils"
	splits "main/utils/splits"
)

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
		splits := splits.ByRegexp(v, regexp.MustCompile(` `))

		direction := splits[0]
		amount := utils.B10toI(splits[1])

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
		splits := splits.ByRegexp(v, regexp.MustCompile(` `))

		direction := splits[0]
		amount := utils.B10toI(splits[1])

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
	input, err := utils.LoadInput(2021, 02)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
