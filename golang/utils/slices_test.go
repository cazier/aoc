package utils

import (
	"sort"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestStringToInt(t *testing.T) {
	var input []string = []string{"1", "2", "3", "4", "5"}
	var expected []int = []int{1, 2, 3, 4, 5}

	var output []int = StringToInt(input)

	assert.Equal(t, expected, output)

	input[0] = "not int"

	assert.Panics(t, func() { StringToInt(input) })
}

func TestRemove(t *testing.T) {
	var input []string = []string{"a", "b", "c", "d", "e"}
	var expected []string = []string{"a", "b", "d", "e"}

	var output []string = Remove(input, 2)
	sort.Strings(output)
	sort.Strings(expected)

	assert.Equal(t, expected, output)
}

func TestRemoveSlow(t *testing.T) {
	var input []int = []int{2, 2, 5, 4, 4}
	var expected []int = []int{2, 2, 4, 4}

	var output []int = RemoveSlow(input, 2)

	assert.Equal(t, expected, output)
}

func TestSum(t *testing.T) {
	var input []int = []int{1, 2, 3, 4, 5}
	var expected int = 15

	var output int = Sum(input)

	assert.Equal(t, expected, output)
}

func TestIndexOf(t *testing.T) {
	var input []int = []int{5, 4, 3, 2, 1}

	assert.Equal(t, IndexOf(input, 4), 1)
	assert.Equal(t, IndexOf(input, 10), -1)
}

func TestContains(t *testing.T) {
	var input []int = []int{5, 4, 3, 2, 1}

	assert.True(t, Contains(input, 4))
	assert.False(t, Contains(input, 10))
}

func TestEach(t *testing.T) {
	assert := assert.New(t)

	positive := func(value int) bool {
		return value > 0
	}

	string_named_e := func(value string) bool {
		return value == "e"
	}

	assert.True(Each([]int{1, 2, 3}, positive))
	assert.False(Each([]string{"1", "e", "!"}, string_named_e))
}

func TestZip(t *testing.T) {
	assert := assert.New(t)

	input := [][]int{
		{1, 1, 1},
		{2, 2, 2},
		{3, 3, 3},
	}
	expected := [][]int{
		{1, 2, 3},
		{1, 2, 3},
		{1, 2, 3},
	}

	assert.ElementsMatch(Zip(input...), expected)

	input = [][]int{
		{1, 1, 1, 1},
		{2, 2, 2, 2},
		{3, 3, 3, 3},
	}
	expected = [][]int{
		{1, 2, 3},
		{1, 2, 3},
		{1, 2, 3},
		{1, 2, 3},
	}

	assert.ElementsMatch(Zip(input...), expected)

	input = [][]int{
		{1, 1, 1, 1, 1, 1, 1, 1},
		{2, 2, 2, 2, 2, 2, 2, 2},
	}
	expected = [][]int{
		{1, 2},
		{1, 2},
		{1, 2},
		{1, 2},
		{1, 2},
		{1, 2},
		{1, 2},
		{1, 2},
	}

	assert.ElementsMatch(Zip(input...), expected)
}
