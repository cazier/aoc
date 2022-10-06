package sets

import (
	"main/utils"
)

type Set[T comparable] struct {
	values []T
}

func New[T comparable](values ...T) Set[T] {
	s := Set[T]{values: make([]T, 0)}
	for _, value := range values {
		s.Add(value)
	}
	return s
}

func (s *Set[T]) Add(value T) {
	if s.Contains(value) {
		return
	}
	s.values = append(s.values, value)
}

func (s *Set[T]) Remove(value T) {
	for index, current := range s.values {
		if current == value {
			s.values = append(s.values[:index], s.values[index+1:]...)
			return
		}
	}
}

func (s *Set[T]) Extend(values ...T) {
	for _, value := range values {
		s.Add(value)
	}
}

func (s Set[T]) Contains(value T) bool {
	return utils.Contains(s.values, value)
}

func (s Set[T]) Length() int {
	return len(s.values)
}

func (s Set[T]) Iter() <-chan T {
	channel := make(chan T)

	go func() {
		for _, value := range s.values {
			channel <- value
		}
		close(channel)
	}()

	return channel

}

func (s Set[T]) Intersection(other Set[T]) Set[T] {
	output := New[T]()

	for value := range s.Iter() {
		if other.Contains(value) {
			output.Add(value)
		}
	}

	for value := range other.Iter() {
		if s.Contains(value) {
			output.Add(value)
		}
	}

	return output
}

func (s Set[T]) Equals(other Set[T]) bool {
	if s.Length() != other.Length() {
		return false
	}

	for value := range s.Iter() {
		if !other.Contains(value) {
			return false
		}
	}

	return true
}

func (s Set[T]) IsDisjoint(other Set[T]) bool {
	return s.Intersection(other).Length() == 0
}
