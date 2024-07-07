package main

import (
	"net/http"
	"time"
	"github.com/a-h/templ"
	"fmt"
	"github.com/alexedwards/scs/v2"
)

var sessionManager *scs.SessionManager

func putHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("putHandler")
	sessionManager.Put(r.Context(), "meow", "kevin")
}

func getHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("GetHandler")
	msg := sessionManager.GetString(r.Context(), "meow")
	fmt.Println(msg)
}

func main() {
	// Initialize the session.
	sessionManager = scs.New()
	sessionManager.Lifetime = 24 * time.Hour

	fmt.Println(sessionManager)

	mux := http.NewServeMux()

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		 	putHandler(w, r)
			hello().Render(r.Context(), w)
		 	getHandler(w, r)
	})

	mux.Handle("/time", templ.Handler(timeComponent(time.Now())))
	mux.Handle("/404", templ.Handler(notFoundComponent(), templ.WithStatus(http.StatusNotFound)))
	http.ListenAndServe(":3000", sessionManager.LoadAndSave(mux))
}