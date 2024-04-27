package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	full_date, date, weekday, week_number := get_date()
	fmt.Printf("\n%s\n%s\n%s\n%d\n", full_date, date, weekday, week_number)

	results := read_file(week_number)

	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print("\nSelect a project: ")
		userInput, _ := reader.ReadString('\n')
		userInput = strings.TrimSpace(userInput)

		userInput_int, err := strconv.Atoi(userInput)
		if err != nil {
			fmt.Printf("Invalid input: %s", userInput)
		} else {
			fmt.Printf(results[userInput_int])
			break
		}
	}

	fmt.Printf("\nEnter Start: [%s]", get_previous_time())
	start, _ := reader.ReadString('\n')
	start = strings.TrimSpace(start)
	if start == "" {
		start = get_previous_time()
	}

	fmt.Printf("\nEnter Stop: [%s]", get_current_time())
	stop, _ := reader.ReadString('\n')
	stop = strings.TrimSpace(stop)
	if stop == "" {
		stop = get_current_time()
	}

	diff_seconds, diff_hours := calculate_time_difference(start, stop)
	fmt.Printf("start, stop, diff_seconds, diff_hours\n")

	fmt.Printf("%s %s %d %f", start, stop, diff_seconds, diff_hours)
}
