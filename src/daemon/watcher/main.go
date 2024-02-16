package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
	"time"

	"github.com/streadway/amqp"
)

const rabbitMQURL = "amqp://is:is@rabbitmq:5672/is"

var trackedFiles = make(map[string]struct{})

func listXMLFiles() []string {
	files, err := ioutil.ReadDir("/xml")
	if err != nil {
		fmt.Printf("Error accessing /xml: %s\n", err)
		return nil
	}

	xmlFiles := []string{}
	for _, f := range files {
		if strings.HasSuffix(f.Name(), ".xml") {
			xmlFiles = append(xmlFiles, f.Name())
		}
	}

	return xmlFiles
}

func sendMessageToRabbitMQ(message string) error {
	conn, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		return fmt.Errorf("Failed to connect to RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		return fmt.Errorf("Failed to open a channel: %s", err)
	}
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"migrator",
		true,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		return fmt.Errorf("Failed to declare a queue: %s", err)
	}

	err = ch.Publish(
		"",
		q.Name,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(message),
		})
	if err != nil {
		return fmt.Errorf("Failed to publish a message: %s", err)
	}

	return nil
}

func watchDirectory() {
	for {
		xmlFiles := listXMLFiles()

		newFiles := []string{}
		for _, file := range xmlFiles {
			if _, tracked := trackedFiles[file]; !tracked {
				newFiles = append(newFiles, file)
				trackedFiles[file] = struct{}{}

				message := fmt.Sprintf("%s", file)
				fmt.Println(message)

				err := sendMessageToRabbitMQ(message)
				if err != nil {
					log.Printf("Error sending message to RabbitMQ: %s", err)
				}
			}
		}

		time.Sleep(5 * time.Second)
	}
}

func main() {
	watchDirectory()
}
