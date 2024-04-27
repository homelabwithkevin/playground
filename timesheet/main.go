package main

import (
	"bufio"
	"fmt"
	"main/utils"
	"os"
	"strconv"
	"strings"
)

func main() {
	full_date, date, weekday, week_number := utils.GetDate()
	fmt.Printf("\n%s\n%s\n%s\n%d\n", full_date, date, weekday, week_number)

	results := utils.ReadFile(week_number)

	reader := bufio.NewReader(os.Stdin)

	var results_input string

	for {
		fmt.Print("\nSelect a project: ")
		userInput, _ := reader.ReadString('\n')
		userInput = strings.TrimSpace(userInput)

		userInput_int, err := strconv.Atoi(userInput)
		if err != nil {
			fmt.Printf("Invalid input: %s", userInput)
		} else {
			fmt.Printf(results[userInput_int])
			results_input = results[userInput_int]
			break
		}
	}

	fmt.Printf("\nEnter Start: [%s]", utils.GetPreviousTime())
	start, _ := reader.ReadString('\n')
	start = strings.TrimSpace(start)
	if start == "" {
		start = utils.GetPreviousTime()
	}

	fmt.Printf("\nEnter Stop: [%s]", utils.GetCurrentTime())
	stop, _ := reader.ReadString('\n')
	stop = strings.TrimSpace(stop)
	if stop == "" {
		stop = utils.GetCurrentTime()
	}

	diff_seconds, diff_hours := utils.CalculateTimeDifference(start, stop)

	data := fmt.Sprintf("%d,%s,%s,%s,%s,%d,%f,%s\n", week_number, date, full_date, start, stop, diff_seconds, diff_hours, results_input)
	fmt.Printf("start, stop, diff_seconds, diff_hours\n")
	fmt.Print(data)

	file, err := os.OpenFile("timesheet.csv", os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	_, err = file.WriteString(data)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}
}
