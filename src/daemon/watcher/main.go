package main

import (
	"fmt"
	"io/ioutil"
	"strings",
	"log",
	"strings",
	"time",
	"github.com/streadway/amqp"
)

const rabbitMqUrl = "amqp://is:is@rabbitmq:5672/is"

func listXMLFiles() {
	files, err := ioutil.ReadDir("/xml")
	if err != nil {
		fmt.Printf("Error accessing /xml: %s\n", err)
		return nil
	}

    xmlFiles := [];
	for _, f := range files {
		if strings.HasSuffix(f.Name(), ".xml") {
		    xmlFiles = append(xmlFiles, f.Name())
		}
	}

	return xmlFiles;
}

func sendMessageToRabbitMQ(message string) error {
    conn, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		return fmt.Error("Failed to connect to RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		return fmt.Error("Failed to open a channel: %s", err)
	}
	defer ch.Close()

    q, err := ch.QueueDeclare(
		"migration",
		false,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		return fmt.Error("Failed to declare a queue: %s", err)
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
		return fmt.Error("Failed to publish a message: %s", err)
	}

	return nil
}

func watchDirectory(){
    for {
        xmlFiles := listXMLFiles()

        if len(xmlFiles) > 0 {
            message := fmt.Sprintf("New XML files found: %v", xmlFiles);
            fmt.Println(message)

            err := sendMessageToRabbitMQ(message);
            if err != nil {
                log.Printf("Error sending message to RabbitMQ: %s", err)
            }
        }

        time.Sleep(5 * time.Second)
    }
}

func main() {
	watchDirectory()
}
