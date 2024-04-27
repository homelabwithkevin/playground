package utils

import (
	"time"
)

func CalculateTimeDifference(start_time string, end_time string) (int, float64) {
	start, _ := time.Parse("15:04", start_time)
	end, _ := time.Parse("15:04", end_time)

	diff := end.Sub(start)
	seconds := int(diff.Seconds())
	hours := diff.Hours()
	return seconds, hours
}
