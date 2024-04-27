package utils

import (
	"fmt"
	"math/rand"
)

func GenerateRandomNumbers(count int) string {
	var numbers_str string

	for i := 0; i < count; i++ {
		numbers_str += fmt.Sprintf("%d", rand.Intn(9))
	}
	return numbers_str
}

func GenerateRandomProjectrs(count int) string {
	var name string

	for i := 0; i < count; i++ {
		name += fmt.Sprintf("PROJ-%s\n", GenerateRandomNumbers(8))
	}

	fmt.Print(name)
	return name
}
