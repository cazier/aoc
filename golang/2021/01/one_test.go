package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const input string = `
199
200
208
210
200
207
240
269
260
263
`

func TestPartOne(t *testing.T) {
	var expected int = 7
	var output int = PartOne(input)

	assert.Equal(t, output, expected)
}
func TestPartTwo(t *testing.T) {
	var expected int = 5
	var output int = PartTwo(input)

	assert.Equal(t, output, expected)
}
