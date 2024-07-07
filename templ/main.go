package main

import (
	"net/http"
	"time"
	"github.com/a-h/templ"
	"fmt"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
			fmt.Println(r.Context())
			hello().Render(r.Context(), w)
	})

	http.Handle("/time", templ.Handler(timeComponent(time.Now())))
	http.Handle("/404", templ.Handler(notFoundComponent(), templ.WithStatus(http.StatusNotFound)))
	http.ListenAndServe(":3000", nil)
}