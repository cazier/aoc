package utils

import (
	"bytes"
	"io"
	"math"
	"os"
	"path/filepath"
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

	output, err := LoadInput(2020, 15)
	assert.Equal(t, expected, output)
	assert.Nil(t, err)

	os.Unsetenv("AOC_ROOT_DIRECTORY")
	_, err = LoadInput(2020, 15)
	assert.Error(t, err)
}

func TestParseToInt(t *testing.T) {
	assert := assert.New(t)

	var input string = "123"
	var expected int = 123

	output, _ := ParseToInt(input, 10, 16)

	assert.Equal(expected, output)

	input = "10101"
	expected = 21

	output, _ = ParseToInt(input, 2, 16)

	assert.Equal(expected, output)
}
func TestB10toI(t *testing.T) {
	assert := assert.New(t)

	var input string = "123"
	var expected int = 123

	assert.Equal(expected, B10toI(input))
	assert.Panics(func() { B10toI("abcd") })
}

func TestAnswer(t *testing.T) {
	// This is mostly just going to check the output TEXT matches what it should be. I'm expecting
	// the library maintainer to ensure the stdout text is properly colored. Plus that's easier for
	// me.

	r, w, _ := os.Pipe()

	stdout := os.Stdout
	os.Stdout = w

	defer func() {
		os.Stdout = stdout
	}()

	Answer("Colored text")
	w.Close()

	var output bytes.Buffer
	io.Copy(&output, r)

	os := output.String()

	assert.Equal(t, "Colored text\n", os)
}

func TestMin(t *testing.T) {
	assert := assert.New(t)

	assert.Equal(1, Min(1))

	assert.Equal(1, Min(1, 2, 3, 4, 5))
	assert.Equal(-5, Min(-5, -4, -3, -2, -1, 0))

	assert.Equal(1.1, Min(1.1, 1.2, 1.3, 5.1))
	assert.Equal(math.Inf(-1), Min(math.Inf(1), math.Inf(-1)))
}
func TestMax(t *testing.T) {
	assert := assert.New(t)

	assert.Equal(1, Max(1))

	assert.Equal(5, Max(1, 2, 3, 4, 5))
	assert.Equal(0, Max(-5, -4, -3, -2, -1, 0))

	assert.Equal(5.1, Max(1.1, 1.2, 1.3, 5.1))
	assert.Equal(math.Inf(1), Max(math.Inf(1), math.Inf(-1)))
}

func TestAbs(t *testing.T) {
	assert := assert.New(t)

	assert.Equal(1, Abs(-1))
	assert.Equal(50, Abs(50))

	assert.Equal(5.1, Abs(-5.1))
	assert.Equal(math.Inf(1), Abs(math.Inf(-1)))
}

func TestStrip(t *testing.T) {
	assert := assert.New(t)

	assert.Equal("assert", Strip("assert "))
	assert.Equal("assert", Strip(" assert"))
	assert.Equal("assert", Strip(`

	assert`))
}
