package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"io"

	"golang.org/x/crypto/scrypt"
)

func encrypt(input_password string) (string, string, string) {
	// Load your secret key from a safe place and reuse it across multiple
	// Seal/Open calls. (Obviously don't use this example key for anything
	// real.) If you want to convert a passphrase to a key, use a suitable
	// package like bcrypt or scrypt.
	// When decoded the key should be 16 bytes (AES-128) or 32 (AES-256).
	// key, _ := hex.DecodeString("")
	key, _ := hex.DecodeString(input_password)
	plaintext := []byte("exampleplaintext")

	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err.Error())
	}

	// Never use more than 2^32 random nonces with a given key because of the risk of a repeat.
	nonce := make([]byte, 12)
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		panic(err.Error())
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		panic(err.Error())
	}

	ciphertext := aesgcm.Seal(nil, nonce, plaintext, nil)
	return hex.EncodeToString(key), hex.EncodeToString(nonce), hex.EncodeToString(ciphertext)
}

func decrypt(input_key, input_nonce, input_ciphertext string) {
	// Load your secret key from a safe place and reuse it across multiple
	// Seal/Open calls. (Obviously don't use this example key for anything
	// real.) If you want to convert a passphrase to a key, use a suitable
	// package like bcrypt or scrypt.
	// When decoded the key should be 16 bytes (AES-128) or 32 (AES-256).
	// key, _ := hex.DecodeString("")
	// ciphertext, _ := hex.DecodeString("")
	// nonce, _ := hex.DecodeString("")

	key, _ := hex.DecodeString(input_key)
	ciphertext, _ := hex.DecodeString(input_ciphertext)
	nonce, _ := hex.DecodeString(input_nonce)

	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err.Error())
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		panic(err.Error())
	}

	plaintext, err := aesgcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		panic(err.Error())
	}

	fmt.Printf("%s\n", plaintext)
}

func main() {
	custom_key, _ := scrypt.Key([]byte("password"), []byte("salt"), 32768, 8, 1, 32)
	input_password := hex.EncodeToString(custom_key)
	key, nonce, ciphertext := encrypt(input_password)
	fmt.Print("Key: ", key, "\n")
	fmt.Print("nonce: ", nonce, "\n")
	fmt.Print("cipher: ", ciphertext, "\n")
	decrypt(key, nonce, ciphertext)
}
