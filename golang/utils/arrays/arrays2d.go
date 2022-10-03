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
	b.Elements = make([][]T, height)

	for index := range b.Elements {
		b.Elements[index] = make([]T, width)
		for w := 0; w < width; w++ {
			b.Elements[index][w] = defaults
		}
	}

	return b
}

func (this Array2D[T]) Get(x, y int) T {
	return this.Elements[y][x]
}

func (this Array2D[T]) Set(x, y int, value T) T {
	this.Elements[y][x] = value

	return value
}

func (this Array2D[T]) Print(format string) string {
	var output string = ""

	for _, row := range this.Elements {
		for _, cell := range row {
			output += fmt.Sprintf(format, cell)
		}
		output += "\n"
	}
	return output
}

func (this Array2D[T]) Column(index int) []T {
	var output []T = make([]T, this.height)

	for _index, row := range this.Elements {
		output[_index] = row[index]
	}

	return output
}

func (this Array2D[T]) Row(index int) []T {
	return this.Elements[index]
}

func (this Array2D[T]) Find(value T) (x, y int) {
	for y, row := range this.Elements {
		for x := range row {
			if this.Get(x, y) == value {
				return x, y
			}
		}
	}
	return -1, -1
}

func (this Array2D[T]) Sum() T {
	var output T
	for _, row := range this.Elements {
		for _, column := range row {
			output += column
		}
	}

	return output
}
