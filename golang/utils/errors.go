package utils

type AocError struct {
	Msg string
}

func (e *AocError) Error() string {
	return e.Msg
}
