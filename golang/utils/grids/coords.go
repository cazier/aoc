package grids

func (c Coord) Neighbors() <-chan Coord {
	channel := make(chan Coord)

	go func() {
		for x := -1; x <= 1; x++ {
			for y := -1; y <= 1; y++ {
				if !(x == 0 && y == 0) {
					channel <- Coord{c.x + x, c.y + y}
				}
			}
		}
		close(channel)
	}()

	return channel
}

func (c Coord) Add(other Coord) Coord {
	return Coord{c.x + other.x, c.y + other.y}
}

func (c Coord) Ok() bool {
	return c.x >= 0 && c.y >= 0
}
