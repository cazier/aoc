package arrays2d

import (
	"fmt"

	utils "main/utils"
)

type Array2D[T utils.Numeric] struct {
	Elements      [][]T
	width, height int
}

func Construct[T utils.Numeric](width, height int, defaults T) Array2D[T] {
	b := Array2D[T]{width: width, height: height}
	b.Elements = make([][]T, width)

	for index := range b.Elements {
		b.Elements[index] = make([]T, width)
		b.Elements[index] = []T{defaults, defaults, defaults, defaults, defaults}
	}

	return b
}

func (a Array2D[T]) Get(x, y int) T {
	return a.Elements[y][x]
}

func (a Array2D[T]) Set(x, y int, value T) T {
	a.Elements[y][x] = value

	return value
}

func (a Array2D[T]) Print(format string) string {
	var output string = ""

	for _, row := range a.Elements {
		for _, cell := range row {
			output += fmt.Sprintf(format, cell)
		}
		output += "\n"
	}
	return output
}

func (a Array2D[T]) Column(index int) []T {
	var output []T = make([]T, a.height)

	for _index, row := range a.Elements {
		output[_index] = row[index]
	}

	return output
}

func (a Array2D[T]) Row(index int) []T {
	return a.Elements[index]
}

func (a Array2D[T]) Find(value T) (x, y int) {
	for y, row := range a.Elements {
		for x := range row {
			if a.Get(x, y) == value {
				return x, y
			}
		}
	}
	return -1, -1
}

func (a Array2D[T]) Total() T {
	var output T
	for _, row := range a.Elements {
		for _, column := range row {
			output += column
		}
	}

	return output
}
