package main

import (
	"fmt"
	"regexp"
	"strings"

	utils "main/utils"
	"main/utils/splits"
)

const sample_input string = `
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
`

const digits *regexp.Regexp = regexp.MustCompile("\\d")

func PartOne(input string) int {
	for line := splits.ByLine(input) {
		items = digits
	}

func PartTwo(input string) int {
	return 0
}

func main() {
	input, err := utils.LoadInput(2023, 01)

	if err != nil {
		panic(err)
	}


	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
