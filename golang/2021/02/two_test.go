package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const input string = `
forward 5
down 5
forward 8
up 3
down 8
forward 2
`

func TestPartOne(t *testing.T) {
	var expected int = 150
	var output int = PartOne(input)

	assert.Equal(t, output, expected)
}
func TestPartTwo(t *testing.T) {
	var expected int = 900
	var output int = PartTwo(input)

	assert.Equal(t, output, expected)
}
