package grid

import (
	"testing"

	aoclib "github.com/cazier/aoclib"
	"github.com/stretchr/testify/assert"
)

func TestNewGrid(t *testing.T) {
	assert := assert.New(t)

	input := New[int](3)
	assert.Equal(make(map[Coord]int), input.contents)
	assert.Equal([][]int{(nil), (nil), (nil)}, input.viewer)
}

func TestGridFromString(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	assert.Equal(t, map[Coord]int{
		{0, 0}: 1, {1, 0}: 2, {2, 0}: 3,
		{0, 1}: 4, {1, 1}: 5, {2, 1}: 6,
		{0, 2}: 7, {1, 2}: 8, {2, 2}: 9,
	}, grid.contents)
	assert.Equal(t, [][]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}, grid.viewer)
}

func TestGridGet(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	assert.Equal(t, 6, grid.Get(Coord{2, 1}))
	assert.Equal(t, 0, grid.Get(Coord{10, 10}))
}

func TestGridGetSafe(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	output, err := grid.GetSafe(Coord{2, 1})
	assert.Equal(t, 6, output)
	assert.Nil(t, err)

	_, err = grid.GetSafe(Coord{10, 10})
	assert.Error(t, err)
	assert.Equal(t, coordError(Coord{10, 10}), err)
}

func TestGridSet(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	assert.Equal(t, 5, grid.Get(Coord{1, 1}))
	assert.Equal(t, 5, grid.viewer[1][1])

	grid.Set(Coord{1, 1}, 9)
	assert.Equal(t, 9, grid.Get(Coord{1, 1}))
	assert.Equal(t, 9, grid.viewer[1][1])
}

func TestGridIAdd(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	assert.Equal(t, 5, grid.Get(Coord{1, 1}))
	assert.Equal(t, [][]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}, grid.viewer)

	grid.IAdd(Coord{1, 1}, 9)
	assert.Equal(t, 14, grid.Get(Coord{1, 1}))

	grid.IAdd(Coord{9, 9}, 9)
	assert.Equal(t, [][]int{
		{1, 2, 3},
		{4, 14, 6},
		{7, 8, 9},
	}, grid.viewer)
}

func TestGridIter(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	output := make([]Coord, 0)

	for value := range grid.Iter() {
		output = append(output, value)
	}

	assert.ElementsMatch(t, []Coord{
		{0, 0}, {0, 1}, {0, 2}, {1, 0}, {1, 1}, {1, 2}, {2, 0}, {2, 1}, {2, 2},
	}, output)
}
func TestGridOrderedIter(t *testing.T) {
	input := "123\n456\n789"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	output := make([]Coord, 0)

	for value := range grid.OrderedIter(0, 3, 0, 3) {
		output = append(output, value)
	}

	assert.Equal(t, []Coord{
		{0, 0}, {1, 0}, {2, 0}, {0, 1}, {1, 1}, {2, 1}, {0, 2}, {1, 2}, {2, 2},
	}, output)
}

func TestGridPrint(t *testing.T) {
	input := "123\n456\n789\n"
	grid := FromString(input, func(value string) int { return aoclib.B10toI(value) })

	assert.Equal(t, input, grid.Print(0, 3, 0, 3))
}
