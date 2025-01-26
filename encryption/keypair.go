// https://stackoverflow.com/questions/13555085/save-and-load-crypto-rsa-privatekey-to-and-from-the-disk

package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
)

func createPrivateKey() (string, string) {
	key, _ := rsa.GenerateKey(rand.Reader, 4096)
	p_key := key.PublicKey

	private_key := x509.MarshalPKCS1PrivateKey(key)
	public_key := x509.MarshalPKCS1PublicKey(&p_key)

	private_key_encoded := pem.EncodeToMemory(
		&pem.Block{
			Type:  "RSA PRIVATE KEY",
			Bytes: private_key,
		},
	)

	public_key_encoded := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: public_key,
	})

	return string(private_key_encoded), string(public_key_encoded)
}

func main() {
	private_key, public_key := createPrivateKey()
	fmt.Print(private_key)
	fmt.Print(public_key)
}
