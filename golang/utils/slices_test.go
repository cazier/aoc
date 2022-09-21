package utils

import (
	"testing"
)

func TestSum(t *testing.T) {
	var input []int64 = []int64{1, 2, 3, 4, 5}
	var expected int64 = 15

	var actual int64 = Sum(input)

	if expected != actual {
		t.Errorf("Expected value %d, but received %d", expected, actual)
	}
}
