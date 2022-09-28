package main

import (
	"regexp"
	"strings"

	utils "main/utils"
)

const sample_input string = `
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
`

func PartOne(input string) int {
	commands, boards := gameData(input)

	for _, command := range utils.SplitStringByPattern(commands, regexp.MustCompile(`,`)) {
		for _, board := range boards {
			num, _ := utils.ParseToInt(command, 10, 16)
			board.AddToMarkedWithRemoval(num)

			row, column := board.CheckReturn()

			if row != -1 || column != -1 {
				return board.Total() * num
			}
		}
	}

	return -1
}

func PartTwo(input string) int {
	commands, boards := gameData(input)

	for _, command := range utils.SplitStringByPattern(commands, regexp.MustCompile(`,`)) {
		num, _ := utils.ParseToInt(command, 10, 16)

		for index, board := range boards {
			var out int = board.AddToMarkedWithRemoval(num)

			if out == -1 {
				continue
			}

			row, column := board.CheckReturn()

			if row != -1 || column != -1 {
				if len(boards) == 1 {
					return board.Total() * num
				}

				delete(boards, index)
			}
		}
	}

	return -1
}

func gameData(input string) (string, map[int]BingoBoard) {
	data := utils.SplitStringByPattern(input, regexp.MustCompile(`\n\n`))

	boards := make(map[int]BingoBoard)

	for index, board_string := range data[1:] {
		boards[index] = FromBoard(board_string)
	}

	return strings.Replace(data[0], "\n", "", -1), boards
}

func main() {
	var input string = utils.LoadInput(2021, 04)

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}
