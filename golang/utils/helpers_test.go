package utils

import (
	"bytes"
	"io"
	"math"
	"os"
	"os/exec"
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

	// Test
	var output string = LoadInput(2020, 15)

	assert.Equal(t, output, expected)
}

func TestLoadInputFailure(t *testing.T) {
	if os.Getenv("CAPTURE_CRASH_OUTPUT") == "1" {
		os.Unsetenv("AOC_ROOT_DIRECTORY")

		LoadInput(2020, 15)
		return
	}

	command := exec.Command(os.Args[0], "-test.run=TestLoadInputFailure")
	command.Env = append(os.Environ(), "CAPTURE_CRASH_OUTPUT=1")

	err := command.Run()

	if e, ok := err.(*exec.ExitError); ok && !e.Success() {
		assert.True(t, ok && !e.Success())
	}
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

	assert.Equal(t, os, "Colored text\n")
}

func TestNumRange(t *testing.T) {
	assert := assert.New(t)

	assert.Equal([]int{0, 1, 2, 3, 4}, NumRange(0, 5))
	assert.Equal([]int{-5, -4, -3, -2, -1}, NumRange(-5, 0))
	assert.Equal([]int{5, 4, 3, 2, 1}, NumRange(5, 0))
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
