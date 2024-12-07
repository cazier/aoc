package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPartOne(t *testing.T) {
	var expected int = 5
	var output int = PartOne(sample_input)

	assert.Equal(t, expected, output)
}

func TestPartTwo(t *testing.T) {
	var expected int = 12
	var output int = PartTwo(sample_input)

	assert.Equal(t, expected, output)
}
