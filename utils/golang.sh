TEST_NAME="${DAY_NAME}_test.go"
RUN_NAME="${DAY_NAME}.go"

TEST_CODE=$(cat <<EOF
package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const input string = \`

\`

func TestPartOne(t *testing.T) {
	var expected int =
	var output int = PartOne(input)

	assert.Equal(t, output, expected)
}
func TestPartTwo(t *testing.T) {
	var expected int =
	var output int = PartTwo(input)

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

func PartOne(input string) int {

}

func PartTwo(input string) int {

}

func main() {
	var input string = utils.LoadInput(${YEAR}, ${DAY})

	fmt.Println("Part One:", PartOne(input))
	fmt.Println("Part Two:", PartTwo(input))
}
EOF
)
