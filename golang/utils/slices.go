package utils

import "strconv"

// StringToInt takes a slice of strings and converts each of them to an int value,
// and returns a new slice with those values.
func StringToInt(slice []string) []int {
	var output []int

	for _, v := range slice {
		val, err := strconv.ParseInt(v, 10, 16)

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
func Sum[T Numeric](slice []T) T {
	var total T = 0

	for _, v := range slice {
		total += v
	}

	return total
}
