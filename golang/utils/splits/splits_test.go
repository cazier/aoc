package splits

import (
	"regexp"
	"testing"

	assert "github.com/stretchr/testify/assert"
)

func TestByLine(t *testing.T) {
	var input string = "hello\nline\ntwo\nfour"
	var expected []string = []string{"hello", "line", "two", "four"}
	var output []string = ByLine(input)

	assert.Equal(t, expected, output)
}

func TestByComma(t *testing.T) {
	var input string = "1,2,3,4"
	var expected []string = []string{"1", "2", "3", "4"}
	var output []string = ByComma(input)

	assert.Equal(t, expected, output)
}

func TestByCharacter(t *testing.T) {
	var input string = "hello"
	var expected []string = []string{"h", "e", "l", "l", "o"}
	var output []string = ByCharacter(input)

	assert.Equal(t, expected, output)
}

func TestStringByRegexp(t *testing.T) {
	assert := assert.New(t)
	var input string = "h1e2l3l4o"
	var expected []string = []string{"h", "e", "l", "l", "o"}

	var output []string = ByRegexp(input, regexp.MustCompile(`\d`))

	assert.Equal(expected, output)

	expected = []string{"h1e2l", "l4o"}
	output = ByRegexp(input, regexp.MustCompile(`3`))

	assert.Equal(expected, output)
}
