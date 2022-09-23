package utils

import (
	"reflect"
	"testing"
)

func TestStringToInt(t *testing.T) {
	var input []string = []string{"1", "2", "3", "4", "5"}
	var expected []int64 = []int64{1, 2, 3, 4, 5}

	var output []int64 = StringToInt(input)

	if !reflect.DeepEqual(expected, output) {
		panic("Not equal!")
	}

}
func TestSum(t *testing.T) {
	var input []int64 = []int64{1, 2, 3, 4, 5}
	var expected int64 = 15

	var actual int64 = Sum(input)

	if expected != actual {
		t.Errorf("Expected value %d, but received %d", expected, actual)
	}
}
