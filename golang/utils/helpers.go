package utils

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func LoadInput(year int, day int) string {
	var root string = os.Getenv("AOC_ROOT_DIRECTORY")

	var year_string string = fmt.Sprintf("2%03d", year%2000)
	var day_string string = fmt.Sprintf("%02d.txt", day)

	path, err := filepath.Abs(filepath.Join(root, "inputs", year_string, day_string))

	if err != nil {
		panic(err)
	}

	contents, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	return string(contents)
}

func SplitLine(input string) []string {
	_splits := strings.Split(input, "\n")
	var output []string

	for _, v := range _splits {
		if len(v) > 0 {
			output = append(output, v)
		}
	}
	return output
}
