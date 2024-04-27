package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func read_file(week_number int) {
	file, _ := os.Open("timesheet.csv")

	defer file.Close()

	reader := csv.NewReader(file)
	records, _ := reader.ReadAll()

	fmt.Printf("%s\n", records[0])
	for _, record := range records {
		local := record[0]

		if local == strconv.Itoa(week_number) {
			fmt.Printf("%s\n", record)
		}
	}
}
