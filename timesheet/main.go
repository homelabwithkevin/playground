package main

import (
	"fmt"
)

func main() {
	fmt.Printf("Hello, World!")
	full_date, date, weekday, week_number := get_date()
	fmt.Printf("\n%s\n%s\n%s\n%d\n", full_date, date, weekday, week_number)
	generate_random_numbers(8)
}
