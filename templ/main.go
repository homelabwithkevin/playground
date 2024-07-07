package main

import (
	"net/http"
	"github.com/a-h/templ"
)

func main() {
	http.Handle("/", templ.Handler(hello()))
	http.ListenAndServe(":3000", nil)
}