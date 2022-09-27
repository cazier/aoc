package main

import (
	utils "main/utils"
	arrays2d "main/utils/arrays"
	"regexp"
)

type BingoBoard struct {
	input  arrays2d.Array2D[int]
	marked arrays2d.Array2D[int]
}

func FromBoard(input string) BingoBoard {
	b := BingoBoard{}
	var a arrays2d.Array2D[int] = arrays2d.Construct(5, 5, -1)

	for y, row := range utils.SplitByLine(input) {
		for x, value := range utils.StringToInt(utils.SplitStringByPattern(row, regexp.MustCompile(`[\s]`))) {
			a.Set(x, y, value)
		}
	}

	b.input = a
	b.marked = arrays2d.Construct(5, 5, -1)

	return b
}

func (b BingoBoard) AddToMarked(value int) {
	x, y := b.input.Find(value)
	if x == -1 || y == -1 {
		panic("Could not find the value in the input board")
	}
	b.marked.Set(x, y, value)
}

func (b BingoBoard) CheckReturn() (row_num, column_num int) {
	for index, row := range b.marked.Elements {
		if index == 0 {
			for column_index := range row {
				if utils.IndexOf(b.marked.Column(column_index), -1) == -1 {
					return -1, column_index
				}
			}
		}
		if utils.IndexOf(b.marked.Row(index), -1) == -1 {
			return index, -1
		}
	}

	return -1, -1
}

func (b BingoBoard) AddToMarkedWithRemoval(value int) int {
	x, y := b.input.Find(value)
	if x == -1 || y == -1 {
		return -1
	}
	b.marked.Set(x, y, value)
	b.input.Set(x, y, 0)

	return value
}
