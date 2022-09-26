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

	assert.Equal(t, output, expected)
}

func TestRemove(t *testing.T) {
	var input []string = []string{"a", "b", "c", "d", "e"}
	var expected []string = []string{"a", "b", "d", "e"}

	var output []string = Remove(input, 2)
	sort.SliceStable(output, func(i, j int) bool { return output[i] < output[j] })
	sort.SliceStable(expected, func(i, j int) bool { return expected[i] < expected[j] })

	assert.Equal(t, output, expected)
}

func TestRemoveSlow(t *testing.T) {
	var input []int = []int{2, 2, 5, 4, 4}
	var expected []int = []int{2, 2, 4, 4}

	var output []int = RemoveSlow(input, 2)

	assert.Equal(t, output, expected)
}

func TestSum(t *testing.T) {
	var input []int = []int{1, 2, 3, 4, 5}
	var expected int = 15

	var output int = Sum(input)

	assert.Equal(t, output, expected)
}
