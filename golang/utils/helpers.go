package utils

import (
	"fmt"
	"os"
	"path/filepath"
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
	_splits := strings.Split(input, "\n")
	var output []string

	for _, v := range _splits {
		if len(v) > 0 {
			output = append(output, v)
		}
	}
	return output
}
