package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPartOne(t *testing.T) {
	var expected int = 1656
	var output int = PartOne(sample_input)

	assert.Equal(t, output, expected)
}
func TestPartTwo(t *testing.T) {
	var expected int = 195
	var output int = PartTwo(sample_input)

	assert.Equal(t, output, expected)
}
