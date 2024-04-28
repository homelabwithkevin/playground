package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/go-redis/redis/v8"
	"github.com/joho/godotenv"
)

var ctx = context.Background()

func HVals(rdb *redis.Client, key string) string {
	var values []string
	result := rdb.HVals(ctx, key)
	for _, v := range result.Val() {
		values = append(values, v)
	}

	jsonValues, err := json.Marshal(values)

	if err != nil {
		log.Fatal("Error marshaling values to JSON")
	}

	return string(jsonValues)
}

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	// Redis Client
	redis_conf := os.Getenv("redis")
	rdb := redis.NewClient(&redis.Options{
		Addr: redis_conf,
	})

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		params := r.URL.Query()
		var result string

		year := params.Get("year")
		if "year" != "" {
			result = HVals(rdb, year)

			w.Header().Set("Content-Type", "application/json")
			w.Write([]byte(fmt.Sprintf("%v", result)))

		} else {
			w.Write([]byte("hello world"))
		}
	})

	http.ListenAndServe(":3000", nil)

}
