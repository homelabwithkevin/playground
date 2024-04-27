package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func read_file(week_number int) []string {
	file, _ := os.Open("timesheet.csv")

	defer file.Close()

	reader := csv.NewReader(file)
	records, _ := reader.ReadAll()

	fmt.Printf("%s\n", records[0])

	var results []string

	for _, record := range records {
		local := record[0]

		if local == strconv.Itoa(week_number) {
			fmt.Printf("%s\n", record)
			results = append(results, record[len(record)-1])
		}
	}

	for idx, result := range results {
		fmt.Printf("%d: %s\n", idx, result)
	}

	return results
}
