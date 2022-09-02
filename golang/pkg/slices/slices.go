package slices

import "strconv"

func StringToInt(input []string) []int64 {
	var output []int64

	for i := 0; i < len(input); i++ {
		val, err := strconv.ParseInt(input[i], 10, 16)

		if err != nil {
			panic(err)
		}

		output = append(output, val)
	}

	return output
}

func Sum(values []int64) int64 {
	var total int64 = 0

	for i := 0; i < len(values); i++ {
		total += values[i]
	}
	return total

}
