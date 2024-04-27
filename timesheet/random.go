package main

import (
	"fmt"
	"math/rand"
)

func generate_random_numbers(count int) string {
	var numbers_str string

	for i := 0; i < count; i++ {
		numbers_str += fmt.Sprintf("%d", rand.Intn(9))
	}
	return numbers_str
}
