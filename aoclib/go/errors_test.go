package aoclib

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestErrorString(t *testing.T) {
	err := AocError{"An error occurred"}

	assert.Equal(t, "An error occurred", err.Error())
}
