package splits

import (
	"regexp"
)

// ByRegexp takes an arbitrary string and splits it by a regular expression pattern. The
// resulting slice is returned.
func ByRegexp(input string, pattern *regexp.Regexp) []string {
	_splits := pattern.Split(input, -1)
	var output []string

	for _, v := range _splits {
		if len(v) > 0 {
			output = append(output, v)
		}
	}
	return output
}

// ByLine takes a string input and breaks it into a slice of strings, split by any of the
// following newline characters: `\r`, `\n`. The resulting slice is returned.
func ByLine(input string) []string {
	var pattern *regexp.Regexp = regexp.MustCompile(`[\r\n]`)
	return ByRegexp(input, pattern)
}

// ByComma takes a string input and breaks it into a slice of strings, split by any a comma.
// The resulting slice is returned.
func ByComma(input string) []string {
	var pattern *regexp.Regexp = regexp.MustCompile(`,`)
	return ByRegexp(input, pattern)
}

// ByCharacter takes a string input breaks into a slice with an element for each character,
// which is then returned
func ByCharacter(input string) []string {
	var pattern *regexp.Regexp = regexp.MustCompile(``)
	return ByRegexp(input, pattern)
}
