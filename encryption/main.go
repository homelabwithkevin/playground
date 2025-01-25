package main

import (
	"crypto/sha256"
	"fmt"
	"golang.org/x/crypto/pbkdf2"
)

func main() {
	salt := make([]byte, 16)
	dk := pbkdf2.Key([]byte("password"), salt, 4096, 32, sha256.New)
	fmt.Printf("%x\n", dk)
}
