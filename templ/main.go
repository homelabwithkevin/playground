package main

import (
	"net/http"
	"time"
	"github.com/a-h/templ"
)

func main() {
	http.Handle("/", templ.Handler(hello()))
	http.Handle("/time", templ.Handler(timeComponent(time.Now())))
	http.Handle("/404", templ.Handler(notFoundComponent(), templ.WithStatus(http.StatusNotFound)))
	http.ListenAndServe(":3000", nil)
}