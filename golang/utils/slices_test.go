package utils

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestStringToInt(t *testing.T) {
	var input []string = []string{"1", "2", "3", "4", "5"}
	var expected []int = []int{1, 2, 3, 4, 5}

	var output []int = StringToInt(input)

	assert.Equal(t, output, expected)
}

func TestSum(t *testing.T) {
	var input []int = []int{1, 2, 3, 4, 5}
	var expected int = 15

	var output int = Sum(input)

	assert.Equal(t, output, expected)
}
