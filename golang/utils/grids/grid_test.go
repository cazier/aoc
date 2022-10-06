package grid

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCoordNeighbors(t *testing.T) {
	input := Coord{3, 3}
	expected := []Coord{
		{2, 2}, {2, 3}, {2, 4},
		{3, 2}, {3, 4},
		{4, 2}, {4, 3}, {4, 4},
	}
	output := make([]Coord, 0)

	for value := range input.Neighbors() {
		output = append(output, value)
	}

	assert.Equal(t, expected, output)
}

func TestCoordAdd(t *testing.T) {
	input := Coord{3, 3}

	assert.Equal(t, input.Add(input), Coord{6, 6})
}

func TestCoordOk(t *testing.T) {
	assert.True(t, Coord{1, 1}.Ok())
	assert.False(t, Coord{-1, -1}.Ok())
	assert.False(t, Coord{1, -1}.Ok())
	assert.False(t, Coord{-1, 1}.Ok())
}
