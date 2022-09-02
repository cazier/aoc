package helpers

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func LoadInput(cwd string, year int, day int) string {
	path := filepath.Join(cwd, "../inputs", fmt.Sprint(year), fmt.Sprintf("%02d.txt", day))

	contents, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}
	return string(contents)
}

func SplitLine(input string) []string {
	return strings.Split(input, "\n")
}

func SliceStringToInt(input []string) []int64 {
	var output []int64

	for i := 0; i < len(input); i++ {
		if len(input[i]) == 0 {
			continue
		}

		val, err := strconv.ParseInt(input[i], 10, 16)

		if err != nil {
			panic(err)
		}

		output = append(output, val)
	}

	return output
}
