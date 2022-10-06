package grids

import (
	"fmt"

	utils "main/utils"
)

// Coord is used primarily as the keys to a map
type Coord struct {
	x int
	y int
}

type Grid[T utils.Numeric] struct {
	contents map[Coord]T
	viewer   [][]T
}

func coordError(c Coord) error {
	var cs string = fmt.Sprintf("Coord<(%d, %d)>", c.x, c.y)
	return &utils.AocError{Msg: "the requested coordinate does not exist: " + cs}
}
