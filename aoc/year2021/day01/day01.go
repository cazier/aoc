package main

import (
	_ "embed"

	aoclib "github.com/cazier/aoclib"
	"github.com/cazier/aoclib/splits"
)

//go:embed input
var input string

const sample_input string = `
199
200
208
210
200
207
240
269
260
263
`

func PartOne(input string) int {
	var depths []int = aoclib.StringToInt(splits.ByLine(input))

	var increases int = 0

	for i := 1; i < len(depths); i++ {
		if depths[i-1] < depths[i] {
			increases++
		}
	}
	return increases
}

func PartTwo(input string) int {
	var depths []int = aoclib.StringToInt(splits.ByLine(input))

	var increases int = 0

	for i := 0; i < len(depths)-3; i++ {
		if aoclib.Sum(depths[i:i+3]) < aoclib.Sum(depths[i+1:i+4]) {
			increases++
		}
	}
	return increases
}

func main() {
	aoclib.Answer("Part One: %d", PartOne(input))
	aoclib.Answer("Part Two: %d", PartTwo(input))
}
