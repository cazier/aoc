package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPartOne(t *testing.T) {
	var expected int = 37
	var output int = PartOne(sample_input)

	assert.Equal(t, output, expected)
}
func TestPartTwo(t *testing.T) {
	var expected int = 22
	var output int = PartTwo(sample_input)

	assert.Equal(t, output, expected)
}
