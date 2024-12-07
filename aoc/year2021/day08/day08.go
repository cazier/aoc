package main

import (
	_ "embed"
	"regexp"

	aoclib "github.com/cazier/aoclib"
	"github.com/cazier/aoclib/sets"
	"github.com/cazier/aoclib/splits"
)

//go:embed input
var input string

const sample_input string = `
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
`

func PartOne(input string) int {
	displays := fromDisplay(input)
	var output int = 0

	for _, display := range displays {
		display.Resolve()
		var num int = 0
		for _, m := range display.output_match {
			if aoclib.Contains([]int{1, 4, 7, 8}, m) {
				num += 1
			}
		}
		output += num
	}
	return output
}

func PartTwo(input string) int {
	displays := fromDisplay(input)
	var output int = 0

	for _, display := range displays {
		display.Resolve()
		var num int = 0
		for _, m := range display.output_match {
			num += m
			num *= 10
		}
		output += (num / 10)
	}
	return output
}

func main() {
	aoclib.Answer("Part One: %d", PartOne(input))
	aoclib.Answer("Part Two: %d", PartTwo(input))
}

func fromDisplay(input string) []*Display {
	var lines []string = splits.ByLine(input)

	var commands []*Display
	for _, line := range lines {
		prompt := splits.ByRegexp(line, regexp.MustCompile(`\|`))
		commands = append(commands, &Display{
			signal_pattern: splits.ByRegexp(prompt[0], regexp.MustCompile(`\s`)),
			output_pattern: splits.ByRegexp(prompt[1], regexp.MustCompile(`\s`)),
		})
	}
	return commands

}

type Display struct {
	signal_pattern []string
	output_pattern []string
	output_match   []int
	wiring         map[int]sets.Set[string]
}

func (d *Display) Resolve() {
	d.output_match = make([]int, 4)
	d.wiring = make(map[int]sets.Set[string])

	for index := range d.output_match {
		d.output_match[index] = -1
	}

	var combo []string = append(d.signal_pattern, d.output_pattern...)
	for {
		for index, segments := range combo {
			if segments != "" {
				wiring := sets.New(splits.ByCharacter(segments)...)
				switch len(segments) {
				case 2:
					d.wiring[1] = wiring
					combo[index] = ""
				case 3:
					d.wiring[7] = wiring
					combo[index] = ""
				case 4:
					d.wiring[4] = wiring
					combo[index] = ""
				case 7:
					d.wiring[8] = wiring
					combo[index] = ""
				case 5:
					if d.wiring[7].Length() != 0 {
						if d.wiring[7].Intersection(wiring).Length() == 3 {
							d.wiring[3] = wiring
							combo[index] = ""
						} else {
							if d.wiring[4].Length() != 0 {
								if d.wiring[4].Intersection(wiring).Length() == 3 {
									d.wiring[5] = wiring
									combo[index] = ""
								} else {
									d.wiring[2] = wiring
									combo[index] = ""
								}
							}
						}
					}
				case 6:
					if d.wiring[4].Length() != 0 {
						if d.wiring[4].Intersection(wiring).Length() == 4 {
							d.wiring[9] = wiring
							combo[index] = ""
						} else {
							if d.wiring[7].Length() != 0 {
								if d.wiring[7].Intersection(wiring).Length() == 3 {
									d.wiring[0] = wiring
									combo[index] = ""
								} else {
									d.wiring[6] = wiring
									combo[index] = ""
								}
							}
						}
					}
				default:
					continue
				}
			}
		}

		valid := func(value string) bool {
			return value == ""
		}

		if aoclib.Each(combo, valid) {
			break
		}
	}

	for index, pattern := range d.output_pattern {
		d.output_match[index] = d.Match(splits.ByCharacter(pattern))
	}
}

func (d *Display) Match(pattern []string) int {
	other := sets.New(pattern...)

	for value, wires := range d.wiring {
		if wires.Equals(other) {
			return value
		}
	}
	return -1
}
