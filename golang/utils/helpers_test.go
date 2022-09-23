package utils

import (
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

func TestLoadInput(t *testing.T) {
	var input []byte = []byte("hello\nline\ntwo\nfour")
	var expected string = "hello\nline\ntwo\nfour"

	// Setup
	var tmpdir string = t.TempDir()
	os.Setenv("AOC_ROOT_DIRECTORY", tmpdir)

	var testFile string = filepath.Join(tmpdir, "inputs", "2020")
	os.MkdirAll(testFile, os.ModePerm)

	os.WriteFile(filepath.Join(testFile, "15.txt"), input, os.ModePerm)

	// Test
	var output string = LoadInput(2020, 15)

	if output != expected {
		panic("Not equal!")
	}

}

func TestSplitLine(t *testing.T) {
	var input string = "hello\nline\ntwo\nfour"
	var expected []string = []string{"hello", "line", "two", "four"}

	var output []string = SplitLine(input)

	if !reflect.DeepEqual(expected, output) {
		panic("Not equal!")
	}

}
