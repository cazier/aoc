package utils

import (
	"reflect"
	"testing"
)

func TestLoadInput(t *testing.T) {
	var input string = "hello\nline\ntwo\nfour"

	var expected []string = []string{"hello", "line", "two", "four"}
	var output []string = SplitLine(input)

	if !reflect.DeepEqual(expected, output) {
		panic("Not equal!")
	}

}
