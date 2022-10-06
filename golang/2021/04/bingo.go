// TODO: This probably can be updated to use a grids.Grid rather than the Array2D
package main

import (
	"regexp"

	utils "main/utils"
	arrays2d "main/utils/arrays"
	splits "main/utils/splits"
)

type BingoBoard struct {
	input  arrays2d.Array2D[int]
	marked arrays2d.Array2D[int]
}

func fromBoard(input string) BingoBoard {
	b := BingoBoard{}
	var a arrays2d.Array2D[int] = arrays2d.Construct(5, 5, -1)

	for y, row := range splits.ByLine(input) {
		for x, value := range utils.StringToInt(splits.ByRegexp(row, regexp.MustCompile(`[\s]`))) {
			a.Set(x, y, value)
		}
	}

	b.input = a
	b.marked = arrays2d.Construct(5, 5, -1)

	return b
}

func (b BingoBoard) checkReturn() (row_num, column_num int) {
	for index, row := range b.marked.Elements {
		if index == 0 {
			for column_index := range row {
				if !utils.Contains(b.marked.Column(column_index), -1) {
					return -1, column_index
				}
			}
		}
		if !utils.Contains(b.marked.Row(index), -1) {
			return index, -1
		}
	}

	return -1, -1
}

func (b BingoBoard) addToMarkedWithRemoval(value int) int {
	x, y := b.input.Find(value)
	if x == -1 || y == -1 {
		return -1
	}
	b.marked.Set(x, y, value)
	b.input.Set(x, y, -1)

	return value
}

func (b BingoBoard) total() int {
	var output int
	for _, row := range b.input.Elements {
		for _, column := range row {
			if column != -1 {
				output += column
			}
		}
	}

	return output
}
