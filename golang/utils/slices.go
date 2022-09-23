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

// Sum returns the total value of all the elements in a slice added together. This will return the
// same type as the input values.
func Sum[T Numeric](slice []T) T {
	var total T = 0

	for _, v := range slice {
		total += v
	}

	return total
}
