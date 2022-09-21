package main

import (
	"fmt"
	"strconv"
	"strings"

	utils "main/utils"
)

func PartOne(input string) int64 {
	var commands []string = utils.SplitLine(input)

	var x int64 = 0
	var y int64 = 0

	for i := 0; i < len(commands); i++ {
		splits := strings.SplitN(commands[i], " ", 2)

		direction := splits[0]
		amount, _ := strconv.ParseInt(splits[1], 10, 64)

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

func PartTwo(input string) int64 {
	var commands []string = utils.SplitLine(input)

	var x int64 = 0
	var y int64 = 0
	var aim int64 = 0

	for i := 0; i < len(commands); i++ {
		splits := strings.SplitN(commands[i], " ", 2)

		direction := splits[0]
		amount, _ := strconv.ParseInt(splits[1], 10, 64)

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
	var input string = utils.LoadInput(2021, 02)

	fmt.Println("Part One:", PartOne(input))
	fmt.Println("Part Two:", PartTwo(input))
}
