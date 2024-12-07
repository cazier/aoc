package aoclib

import (
	"strconv"

	"github.com/cazier/aoclib/pkg/types"
)

// StringToInt takes a slice of strings and converts each of them to an int value,
// and returns a new slice with those values.
func StringToInt(slice []string) []int {
	var output []int

	for _, v := range slice {
		val, err := strconv.ParseInt(v, 10, 64)

		if err != nil {
			panic(err)
		}

		output = append(output, int(val))
	}

	return output
}

// Remove will remove an item at index i from a slice, and return the new (shortened) value. Note,
// this specific function should only be used when order does NOT matter, as the slice will get
// rearranged.
func Remove[T comparable](slice []T, i int) []T {
	slice[i] = slice[len(slice)-1]
	return slice[:len(slice)-1]
}

// RemoveSlow will remove an item at index i from a slice, and return the new (shortened) value.
func RemoveSlow[T comparable](slice []T, i int) []T {
	return append(slice[:i], slice[i+1:]...)
}

// Sum returns the total value of all the elements in a slice added together. This will return the
// same type as the input values.
func Sum[T types.Numeric](slice []T) T {
	var total T = 0

	for _, v := range slice {
		total += v
	}

	return total
}

// Count returns the total count of a value in a slice. This will return an integer value
func Count[T types.Numeric](slice []T, value T) int {
	var total int = 0

	for _, v := range slice {
		if v == value {
			total++
		}
	}

	return total
}

// IndexOf returns the index where a value can be found inside a slice. If the value is not found in
// the slice, return -1.
func IndexOf[T comparable](slice []T, value T) int {
	for index, element := range slice {
		if value == element {
			return index
		}
	}
	return -1
}

// Contains returns true if the slice has the value indicated, else returns false.
func Contains[T comparable](slice []T, value T) bool {
	return IndexOf(slice, value) != -1
}

// Each returns a boolean for the output of passing each element in the slice to the supplied
// predicate argument function.
func Each[T comparable](slice []T, predicate func(T) bool) bool {
	for _, element := range slice {
		if !predicate(element) {
			return false
		}
	}
	return true
}

// Iterate through a slice of nested slices and zip-star each item (i.e., python's `zip(*lists)`)
func Zip[T any](slices ...[]T) [][]T {
	output := make([][]T, len(slices[0]))

	for column := range slices[0] {
		output[column] = make([]T, len(slices))

		for index, row := range slices {
			output[column][index] = row[column]
		}
	}

	return output
}
