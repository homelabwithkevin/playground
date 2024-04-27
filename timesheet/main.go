package main

import (
	"fmt"
	"strconv"
)

func main() {
	fmt.Printf("Hello, World!")
	full_date, date, weekday, week_number := get_date()
	fmt.Printf("\n%s\n%s\n%s\n%d\n", full_date, date, weekday, week_number)

	results := read_file(week_number)

	var userInput string

	for {
		fmt.Print("\nSelect a project: ")
		fmt.Scanln(&userInput)
		userInput_int, err := strconv.Atoi(userInput)
		if err != nil {
			fmt.Printf("Invalid input: %s", userInput)
		} else {
			fmt.Printf(results[userInput_int])
			break
		}
	}
}
