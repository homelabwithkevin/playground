package main

import (
	"fmt"
	"time"

	"golang.org/x/crypto/scrypt"
)

func create(speed int) {
	start := time.Now()
	scrypt.Key([]byte("password"), []byte("salt"), speed, 8, 1, 32)
	duration := time.Since(start)
	fmt.Printf("%v,%d\n", duration, speed)
}

func main() {
	speeds := []int{1024, 2048, 4096, 8192, 16384, 32768, 65536}
	for _, speed := range speeds {
		create(speed)
	}
}
