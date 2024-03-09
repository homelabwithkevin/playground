package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

func ListTables(client *dynamodb.Client) {
	tables, err := client.ListTables(context.TODO(), nil)

	if err != nil {
		log.Fatal(err)
	}

	for _, table := range tables.TableNames {
		fmt.Println(table)
	}
}

func ScanTable(client *dynamodb.Client, tableName string) {
	items, err := client.Scan(context.TODO(), &dynamodb.ScanInput{
		TableName: &tableName,
	})

	if err != nil {
		log.Fatal(err)
	}

	for _, i := range items.Items {
		fmt.Println("------------")
		for k, v := range i {
			if k != "description" {
				fmt.Println(k, v)
			}
		}
		break
	}
}

func main() {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-east-2"))
	client := dynamodb.NewFromConfig(cfg)

	if err != nil {
		log.Fatal(err)
	}

	tableName := "youtube-ChannelTable-DB39B0CXJZLL"
	ScanTable(client, tableName)
}
