package sets

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNew(t *testing.T) {
	var input []string = []string{"1", "2", "2", "3", "3", "3"}
	expected := Set[string]{values: []string{"1", "2", "3"}}

	assert.Equal(t, New(input...), expected)
}

func TestAdd(t *testing.T) {
	s := New(0)

	for index := 0; index < 5; index++ {
		for step := 0; step < index; step++ {
			s.Add(index)
		}
	}
	assert.Equal(t, s, Set[int]{values: []int{0, 1, 2, 3, 4}})
}

func TestRemove(t *testing.T) {
	s := New(1, 2, 3, 4)

	assert.Equal(t, s, Set[int]{values: []int{1, 2, 3, 4}})

	s.Remove(3)
	assert.Equal(t, s, Set[int]{values: []int{1, 2, 4}})
}
func TestExtend(t *testing.T) {
	s := New(0)
	s.Extend(1, 2, 3, 4)

	assert.Equal(t, s, Set[int]{values: []int{0, 1, 2, 3, 4}})
}

func TestContains(t *testing.T) {
	s := New(0)

	assert.True(t, s.Contains(0))
	assert.False(t, s.Contains(1))
}

func TestLength(t *testing.T) {
	s := New[int]()

	assert.Equal(t, s.Length(), 0)
	s.Add(1)
	assert.Equal(t, s.Length(), 1)
}

func TestIter(t *testing.T) {
	assert := assert.New(t)

	s := New(1, 2, 3, 4, 5)

	var index int = 0

	for value := range s.Iter() {
		index += 1
		assert.Equal(index, value)
	}
}
func TestIntersection(t *testing.T) {
	s1 := New(1, 2, 3, 4)
	s2 := New(3, 4, 5)

	assert.Equal(t, s1.Intersection(s2), New(3, 4))
}

func TestIsDisjoint(t *testing.T) {
	s1 := New(1, 2, 3, 4)
	s2 := New(5, 6, 7)

	assert.True(t, s1.IsDisjoint(s2))

	s2 = New(3, 4, 5)

	assert.False(t, s1.IsDisjoint(s2))
}
