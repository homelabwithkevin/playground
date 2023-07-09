package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
	"time"
)

var fileName string = "journal.csv"

func createHeaders() {
	_, err := os.Stat(fileName)
	if err != nil {
		fmt.Println("File does not exist:", fileName)
	}
	f, _ := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	header := []string{"start", "stop", "elapsed", "day", "entry"}
	joined := strings.Join(header, ";")
	joined += "\n"
	f.WriteString(joined)
}

func main() {
	createHeaders()
	nowStart := time.Now()
	day := fmt.Sprint(nowStart.Weekday())
	start := fmt.Sprint(nowStart.UnixMilli())
	wordPtr := flag.String("word", "foo", "a string")
	journalPtr := flag.String("j", "journal", "a string")
	numbPtr := flag.Int("numb", 42, "an int")
	forkPtr := flag.Bool("fork", false, "a bool")

	var svar string

	flag.StringVar(&svar, "svar", "bar", "a string var")
	flag.Parse()

	fmt.Println("word:", *wordPtr)
	fmt.Println("journal:", *journalPtr)
	fmt.Println("number:", *numbPtr)
	fmt.Println("fork:", *forkPtr)
	fmt.Println("svar:", svar)
	fmt.Println("tail:", flag.Args())

	now := time.Now()
	fmt.Println(now.UnixMilli())
	fmt.Println(now.Format(time.RFC3339))
	fmt.Println(now.Format(time.RFC3339Nano))
	// This is what I like
	fmt.Println(now.Format(time.RFC1123))
	fmt.Println(now.Format(time.RFC1123Z))
	fmt.Println(now.Format(time.RFC822))
	fmt.Println(now.Format(time.RFC850))

	var project string
	fmt.Println("Project: ")
	fmt.Scanln(&project)

	var entry string
	fmt.Println("Entry: ")
	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		entry = scanner.Text()
	}

	fmt.Println("Hit enter to complete task")
	fmt.Scanln()

	f, _ := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	unixTime := fmt.Sprint(time.Now().UnixMilli())
	elapsed := time.Since(nowStart)
	jString := []string{start, unixTime, elapsed.String(), day, entry}
	joined := strings.Join(jString, ";")
	joined += "\n"

	f.WriteString(joined)
	f.Close()
}
