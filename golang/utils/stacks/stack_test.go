package stacks

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNew(t *testing.T) {
	var input Stack[int] = New[int](3)

	assert.Equal(t, -1, input.pc)
	assert.Equal(t, []int{0, 0, 0}, input.content)
}

func TestPush(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)

	assert.Equal([]string{"", "", ""}, input.content)

	input.Push("four")
	input.Push("five")
	assert.Equal([]string{"four", "five", ""}, input.content)

	input.Push("six")
	assert.Equal([]string{"four", "five", "six"}, input.content)

	assert.Panics(func() { input.Push("seven") })
}

func TestPop(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)
	input.Push("four")
	input.Push("five")
	input.Push("six")

	assert.Equal([]string{"four", "five", "six"}, input.content)

	assert.Equal("six", input.Pop())
	assert.Equal([]string{"four", "five", ""}, input.content)

	input.Pop()
	input.Pop()
	assert.Equal([]string{"", "", ""}, input.content)

	assert.Panics(func() { input.Pop() })
}

func TestPeek(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)
	input.Push("four")

	assert.Equal("four", input.Peek())
	input.Pop()

	assert.Panics(func() { input.Peek() })
}

func TestClear(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)
	input.Push("four")
	input.Push("five")
	input.Push("six")

	assert.Equal([]string{"four", "five", "six"}, input.content)

	input.Clear()
	assert.Equal([]string{"", "", ""}, input.content)

	assert.NotPanics(func() { input.Clear() })
}

func TestPending(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)

	assert.False(input.Pending())

	input.Push("four")
	assert.True(input.Pending())
}
