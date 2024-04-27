package main

import (
	"time"
)

func get_date() (string, string, string, int) {
	now := time.Now()
	full_date := now.Format("2006-01-02 15:04 Monday")
	date := now.Format("2006-01-02")
	weekday := now.Format("Monday")
	_, week_number := now.ISOWeek()

	return full_date, date, weekday, week_number
}
