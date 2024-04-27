package utils

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func ReadFile(week_number int) []string {
	file, _ := os.Open("timesheet.csv")

	defer file.Close()

	reader := csv.NewReader(file)
	records, _ := reader.ReadAll()

	fmt.Printf("%s\n", records[0])

	var results []string
	var uniqueResults []string

	for _, record := range records {
		local := record[0]

		if local == strconv.Itoa(week_number) {
			fmt.Printf("%s\n", record)
			results = append(results, record[len(record)-1])
		}
	}

	for idx, result := range results {
		skip := false
		for _, u := range uniqueResults {
			if result == u {
				skip = true
				break
			}
		}

		if !skip {
			fmt.Printf("%d: %s\n", idx, result)
			uniqueResults = append(uniqueResults, result)
		}
	}

	return uniqueResults
}
