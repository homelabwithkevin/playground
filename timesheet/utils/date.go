package utils

import (
	"time"
)

func GetDate() (string, string, string, int) {
	now := time.Now()
	full_date := now.Format("2006-01-02 15:04 Monday")
	date := now.Format("2006-01-02")
	weekday := now.Format("Monday")
	_, week_number := now.ISOWeek()

	return full_date, date, weekday, week_number
}

func GetCurrentTime() string {
	now := time.Now()
	rounded := now.Round(time.Minute * 15)
	return rounded.Format("15:04")
}

func GetPreviousTime() string {
	now := time.Now()
	rounded := now.Round(time.Minute * 15)
	rounded = rounded.Add(-15 * time.Minute)
	return rounded.Format("15:04")
}
