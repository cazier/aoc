package stacks

type Stack[T comparable] struct {
	pc      int
	content []T
}

func New[T comparable](size int) Stack[T] {
	return Stack[T]{-1, make([]T, size)}
}

func (s *Stack[T]) Push(val T) {
	s.pc++
	s.content[s.pc] = val
}

func (s *Stack[T]) Pop() T {
	var out T = s.content[s.pc]
	var val T
	s.content[s.pc] = val
	s.pc--
	return out
}

func (s *Stack[T]) Peek() T {
	return s.content[s.pc]
}

func (s *Stack[T]) Clear() {
	var val T

	for index := 0; index < len(s.content); index++ {
		if s.content[index] == val {
			break
		}
		s.content[index] = val
	}
	s.pc = -1
}

func (s *Stack[T]) Pending() bool {
	return s.pc >= 0
}
