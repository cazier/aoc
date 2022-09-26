package utils

import (
	"os"
	"path/filepath"
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
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

	assert.Equal(t, output, expected)
}

func TestSplitByLine(t *testing.T) {
	var input string = "hello\nline\ntwo\nfour"
	var expected []string = []string{"hello", "line", "two", "four"}
	var output []string = SplitByLine(input)

	assert.Equal(t, output, expected)
}

func TestSplitByCharacter(t *testing.T) {
	var input string = "hello"
	var expected []string = []string{"h", "e", "l", "l", "o"}
	var output []string = SplitByCharacter(input)

	assert.Equal(t, output, expected)
}

func TestSplitStringByPattern(t *testing.T) {
	assert := assert.New(t)
	var input string = "h1e2l3l4o"
	var expected []string = []string{"h", "e", "l", "l", "o"}

	var output []string = SplitStringByPattern(input, regexp.MustCompile(`\d`))

	assert.Equal(output, expected)

	expected = []string{"h1e2l", "l4o"}
	output = SplitStringByPattern(input, regexp.MustCompile(`3`))

	assert.Equal(output, expected)
}

func TestParseToInt(t *testing.T) {
	assert := assert.New(t)

	var input string = "123"
	var expected int = 123

	output, _ := ParseToInt(input, 10, 16)

	assert.Equal(output, expected)

	input = "10101"
	expected = 21

	output, _ = ParseToInt(input, 2, 16)

	assert.Equal(output, expected)
}

func TestAnswer(t *testing.T) {}
