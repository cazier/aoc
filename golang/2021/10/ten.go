package main

import (
	utils "main/utils"
	"main/utils/splits"
	stacks "main/utils/stacks"
	"sort"
)

const sample_input string = `
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
`

func PartOne(input string) (score int) {
	systems := splits.ByLine(input)
	history := stacks.New[string](len(systems[0]))

	var scores = map[string]int{
		")": 3, "(": 3,
		"]": 57, "[": 57,
		"}": 1197, "{": 1197,
		">": 25137, "<": 25137,
	}

	for _, system := range systems {
		line := splits.ByCharacter(system)
		history.Push(line[0])
		for _, character := range line[1:] {
			if open(character) {
				history.Push(character)
				continue
			} else if match(history.Peek(), character) {
				history.Pop()
				continue
			} else {
				history.Pop()
				score += scores[character]
			}
		}
		history.Clear()
	}
	return score
}

func PartTwo(input string) int {
	systems := splits.ByLine(input)
	history := stacks.New[string](len(systems[0]))
	score := make([]int, 0)

	var scores = map[string]int{
		"(": 1,
		"[": 2,
		"{": 3,
		"<": 4,
	}

	for _, system := range systems {
		line := splits.ByCharacter(system)
		history.Push(line[0])
		for _, character := range line[1:] {
			if open(character) {
				history.Push(character)
				continue
			} else if match(history.Peek(), character) {
				history.Pop()
				continue
			} else {
				history.Clear()
				break
			}
		}
		var interim int = 0

		for history.Pending() {
			interim *= 5
			interim += scores[history.Pop()]
		}
		if interim != 0 {
			score = append(score, interim)
		}
	}
	sort.Ints(score)
	return score[len(score)/2]
}

func main() {
	input, err := utils.LoadInput(2021, 10)

	if err != nil {
		panic(err)
	}

	utils.Answer("Part One: %d", PartOne(input))
	utils.Answer("Part Two: %d", PartTwo(input))
}

func open(character string) bool {
	if character == "(" || character == "[" || character == "{" || character == "<" {
		return true
	}
	return false
}

func match(first, second string) bool {
	switch second {
	case ")":
		return first == "("
	case "]":
		return first == "["
	case "}":
		return first == "{"
	case ">":
		return first == "<"
	default:
		panic("No valid character found")
	}
}
