package grid

import (
	"fmt"
	"main/utils"
	"main/utils/splits"
)

// Coord is used primarily as the keys to a map
type Coord struct {
	x int
	y int
}

func (c Coord) Neighbors() <-chan Coord {
	channel := make(chan Coord)

	go func() {
		for x := -1; x <= 1; x++ {
			for y := -1; y <= 1; y++ {
				if !(x == 0 && y == 0) {
					channel <- Coord{c.x + x, c.y + y}
				}
			}
		}
		close(channel)
	}()

	return channel
}

func (c Coord) Add(other Coord) Coord {
	return Coord{c.x + other.x, c.y + other.y}
}

func (c Coord) Ok() bool {
	return c.x >= 0 && c.y >= 0
}

type Grid[T utils.Numeric] struct {
	contents map[Coord]T
	viewer   [][]T
}

func New[T utils.Numeric](defaults T, size int) Grid[T] {
	return Grid[T]{make(map[Coord]T), make([][]T, size)}
}

func FromString[T utils.Numeric](input string, cast func(value string) T) Grid[T] {
	lines := splits.ByLine(input)
	g := Grid[T]{make(map[Coord]T), make([][]T, len(lines))}

	for y, row := range lines {
		line := splits.ByCharacter(row)
		g.viewer[y] = make([]T, len(line))
		for x, value := range splits.ByCharacter(row) {
			g.Set(Coord{x, y}, cast(value))
			g.viewer[y][x] = cast(value)
		}
	}

	return g
}

func (g *Grid[T]) Get(spot Coord) T {
	var def T
	if out, ok := g.contents[spot]; ok {
		return out
	}
	return def
}

func (g *Grid[T]) Set(spot Coord, value T) {
	g.contents[spot] = value
	g.viewer[spot.y][spot.x] = value
}

func (g *Grid[T]) IAdd(spot Coord, addition T) {
	if _, ok := g.contents[spot]; ok {
		g.contents[spot] += addition
		g.viewer[spot.y][spot.x] += addition
	}
}

func (g *Grid[T]) Iter() <-chan Coord {
	channel := make(chan Coord)

	go func() {
		for value := range g.contents {
			channel <- value
		}
		close(channel)
	}()

	return channel

}

func (g *Grid[T]) OrderedIter(x0, xn, y0, yn int) <-chan Coord {
	channel := make(chan Coord)

	go func() {
		for y := y0; y < yn; y++ {
			for x := x0; x < xn; x++ {
				channel <- Coord{x, y}
			}
		}
		close(channel)
	}()

	return channel

}

func (g *Grid[T]) Print(x0, xn, y0, yn int) (output string) {
	for y := y0; y < yn; y++ {
		for x := x0; x < xn; x++ {
			output += fmt.Sprint(g.Get(Coord{x, y}))
		}
		output += "\n"
	}
	return output
}
