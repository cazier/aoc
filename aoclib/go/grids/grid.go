package grid

import (
	"fmt"

	"github.com/cazier/aoclib/splits"
	"github.com/cazier/aoclib/types"
)

func New[T types.Numeric](rows int) Grid[T] {
	return Grid[T]{make(map[Coord]T), make([][]T, rows)}
}

func FromString[T types.Numeric](input string, cast func(value string) T) Grid[T] {
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
	out, _ := g.GetSafe(spot)
	return out
}

func (g *Grid[T]) GetSafe(spot Coord) (T, error) {
	var def T
	if out, ok := g.contents[spot]; ok {
		return out, nil
	}

	return def, coordError(spot)
}

func (g *Grid[T]) Set(spot Coord, value T) {
	g.contents[spot] = value
	g.viewer[spot.y][spot.x] = value
}

func (g *Grid[T]) IAdd(spot Coord, addition T) {
	if _, ok := g.contents[spot]; ok {
		g.Set(spot, g.Get(spot)+addition)
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
