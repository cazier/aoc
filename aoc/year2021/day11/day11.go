package main

import (
	_ "embed"

	aoclib "github.com/cazier/aoclib"
	grid "github.com/cazier/aoclib/grids"
	"github.com/cazier/aoclib/sets"
)

//go:embed input
var input string

const sample_input string = `
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
`

func PartOne(input string) (score int) {
	board := grid.FromString(input, func(value string) int { return aoclib.B10toI(value) })

	for num := 0; num < 100; num++ {
		score += step(board)
	}
	return score
}

func PartTwo(input string) (score int) {
	board := grid.FromString(input, func(value string) int { return aoclib.B10toI(value) })

	for {
		score += 1

		if step(board) == 100 {
			break
		}
	}
	return score
}

func main() {
	aoclib.Answer("Part One: %d", PartOne(input))
	aoclib.Answer("Part Two: %d", PartTwo(input))
}

func step(board grid.Grid[int]) int {
	flash := sets.New(grid.Coord{})
	flash.Remove(grid.Coord{})

	for key := range board.OrderedIter(0, 10, 0, 10) {
		board.IAdd(key, 1)
	}
	var changed bool = true
	for changed {
		changed = false
		for key := range board.OrderedIter(0, 10, 0, 10) {
			if board.Get(key) > 9 && !flash.Contains(key) {
				flash.Add(key)
				board.Set(key, 0)
				changed = true
				for neighbor := range key.Neighbors() {
					if !neighbor.Ok() || board.Get(neighbor) == 0 {
						continue
					}
					board.IAdd(neighbor, 1)
				}
			}
		}
	}
	return flash.Length()
}
