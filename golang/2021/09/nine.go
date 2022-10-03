package main

import (
	utils "main/utils"
	"main/utils/splits"
	"sort"
)

const sample_input string = `
2199943210
3987894921
9856789892
8767896789
9899965678

`

var toggles []Coord = []Coord{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

type Coord struct {
	x int
	y int
}
type Points struct {
	coords  Coord
	value   int
	visited bool
}

func PartOne(input string) int {
	heightmap := fromGrid(input)
	var answer int

	for _, value := range checkSizes(heightmap) {
		answer += value
	}

	return answer
}

func PartTwo(input string) int {
	lows, heightmap := fromGridToPointers(input)
	basins := make(map[Coord][]*Points, len(lows))
	for basin, value := range lows {
		basins[basin] = make([]*Points, 1)
		basins[basin][0] = &Points{basin, value - 1, false}
	}

	var new_spot int = 0
	for {
		for host, spots := range basins {
			for _, spot := range spots {
				if !spot.visited {
					var counter int = 0
					basins, counter = addPointsToBasin("up", spot.coords, host, heightmap, basins)
					new_spot += counter
					basins, counter = addPointsToBasin("down", spot.coords, host, heightmap, basins)
					new_spot += counter
					basins, counter = addPointsToBasin("left", spot.coords, host, heightmap, basins)
					new_spot += counter
					basins, counter = addPointsToBasin("right", spot.coords, host, heightmap, basins)
					new_spot += counter
					spot.visited = true
				}
			}
		}
		if new_spot == 0 {
			break
		} else {
			new_spot = 0
		}
	}
	var output []int = make([]int, len(basins))

	for _, spots := range basins {
		output = append(output, -1*len(spots))
	}
	sort.Ints(output)
	return output[0] * output[1] * output[2] * -1

}

func main() {
	var input string = utils.LoadInput(2021, 9)

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}

func fromGrid(input string) map[Coord]int {
	output := make(map[Coord]int)

	for y, row := range splits.ByLine(input) {
		for x, item := range splits.ByCharacter(row) {
			num, _ := utils.ParseToInt(item, 10, 16)

			output[Coord{x, y}] = num
		}
	}
	return output
}

func checkSizes(board map[Coord]int) map[Coord]int {
	checker := func(board map[Coord]int, key Coord, value int) bool {
		for _, change := range toggles {
			if other, ok := board[Coord{key.x + change.x, key.y + change.y}]; ok {
				if other <= value {
					return false
				}
			}
		}
		return true
	}
	output := make(map[Coord]int)
	for key, value := range board {
		if checker(board, key, value) {
			output[key] = 1 + value
		}
	}

	return output
}

func fromGridToPointers(input string) (map[Coord]int, map[Coord]*Points) {
	grid := fromGrid(input)
	lows := checkSizes(grid)

	output := make(map[Coord]*Points)
	for key, value := range fromGrid(input) {
		output[key] = &Points{key, value, false}
	}
	return lows, output
}

func addPointsToBasin(dir string, start Coord, host Coord, heightmap map[Coord]*Points, basins map[Coord][]*Points) (map[Coord][]*Points, int) {
	var diff Coord
	var output int = 0
	switch dir {
	case "up":
		diff = Coord{0, -1}
	case "left":
		diff = Coord{-1, 0}
	case "down":
		diff = Coord{0, 1}
	case "right":
		diff = Coord{1, 0}
	default:
		diff = Coord{0, 0}
	}

	exist := func(current []*Points, new *Points) bool {
		for _, existing := range current {
			if existing.coords == new.coords {
				return true
			}
		}
		return false
	}

	for mul := 1; mul < len(heightmap); mul++ {
		if other, ok := heightmap[Coord{start.x + (diff.x * mul), start.y + (diff.y * mul)}]; ok {
			if other.value == 9 {
				break
			} else {
				if !exist(basins[host], other) {
					basins[host] = append(basins[host], other)
					output = 1
				}
			}
		} else {
			break
		}
	}
	return basins, output
}
