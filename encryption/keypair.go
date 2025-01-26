// https://stackoverflow.com/questions/13555085/save-and-load-crypto-rsa-privatekey-to-and-from-the-disk

package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
)

func createPrivateKey() string {
	key, _ := rsa.GenerateKey(rand.Reader, 4096)
	x509_encoded := x509.MarshalPKCS1PrivateKey(key)
	pem_encoded := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509_encoded,
	},
	)
	return string(pem_encoded)
}

func main() {
	key := createPrivateKey()
	fmt.Print(key)
}
