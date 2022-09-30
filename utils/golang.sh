TEST_NAME="${DAY_NAME}_test.go"
RUN_NAME="${DAY_NAME}.go"

TEST_CODE=$(cat <<EOF
package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPartOne(t *testing.T) {
	var expected int =
	var output int = PartOne(sample_input)

	assert.Equal(t, output, expected)
}
func TestPartTwo(t *testing.T) {
	var expected int =
	var output int = PartTwo(sample_input)

	assert.Equal(t, output, expected)
}
EOF
)

RUN_CODE=$(cat <<EOF
package main

import (
	"fmt"

	utils "main/utils"
)

const sample_input string = \`

\`

func PartOne(input string) int {

}

func PartTwo(input string) int {

}

func main() {
	var input string = utils.LoadInput(${YEAR}, ${DAY})

	utils.Answer("Part One: %%d", PartOne(input))
	utils.Answer("Part Two: %%d", PartTwo(input))
}
EOF
)
