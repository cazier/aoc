package stacks

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNew(t *testing.T) {
	var input Stack[int] = New[int](3)

	assert.Equal(t, input.pc, -1)
	assert.Equal(t, input.content, []int{0, 0, 0})
}

func TestPush(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)

	assert.Equal(input.content, []string{"", "", ""})

	input.Push("four")
	input.Push("five")
	assert.Equal(input.content, []string{"four", "five", ""})

	input.Push("six")
	assert.Equal(input.content, []string{"four", "five", "six"})

	assert.Panics(func() { input.Push("seven") })
}

func TestPop(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)
	input.Push("four")
	input.Push("five")
	input.Push("six")

	assert.Equal(input.content, []string{"four", "five", "six"})

	assert.Equal(input.Pop(), "six")
	assert.Equal(input.content, []string{"four", "five", ""})

	input.Pop()
	input.Pop()
	assert.Equal(input.content, []string{"", "", ""})

	assert.Panics(func() { input.Pop() })
}

func TestPeek(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)
	input.Push("four")

	assert.Equal(input.Peek(), "four")
	input.Pop()

	assert.Panics(func() { input.Peek() })
}

func TestClear(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)
	input.Push("four")
	input.Push("five")
	input.Push("six")

	assert.Equal(input.content, []string{"four", "five", "six"})

	input.Clear()
	assert.Equal(input.content, []string{"", "", ""})

	assert.NotPanics(func() { input.Clear() })
}

func TestPending(t *testing.T) {
	assert := assert.New(t)
	var input Stack[string] = New[string](3)

	assert.False(input.Pending())

	input.Push("four")
	assert.True(input.Pending())
}
