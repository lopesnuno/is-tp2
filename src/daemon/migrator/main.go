package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/beevik/etree"
	"github.com/lib/pq"
)

const (
	pollingFreq      = 120
	nestJSEndpoint   = "http://localhost:3000"
	rabbitMQURL    = "amqp://is:is@rabbitmq:5672/is"
	queueName      = "migration"
)

type College struct {
	ID        uuid.UUID `json:"id"`
	Name      string    `json:"name"`
	Latitude  float64   `json:"latitude"`
	Longitude float64   `json:"longitude"`
	Geom      string    `json:"geom"`
	CreatedOn time.Time `json:"created_on"`
	UpdatedOn time.Time `json:"updated_on"`
}

type Season struct {
	ID   uuid.UUID `json:"id"`
	Year string    `json:"year"`
}

type Player struct {
	ID         uuid.UUID `json:"id"`
	Name       string    `json:"name"`
	Country    string    `json:"country"`
	CollegeID  uuid.UUID `json:"college_id"`
	Height     int       `json:"height"`
	Weight     int       `json:"weight"`
	DraftYear  string    `json:"draft_year"`
	DraftRound string    `json:"draft_round"`
	DraftNumber string   `json:"draft_number"`
	CreatedOn  time.Time `json:"created_on"`
	UpdatedOn  time.Time `json:"updated_on"`
}

type SeasonPlayer struct {
	ID        uuid.UUID `json:"id"`
	SeasonID  uuid.UUID `json:"season_id"`
	PlayerID  uuid.UUID `json:"player_id"`
}

type Stats struct {
	ID            uuid.UUID `json:"id"`
	SeasonPlayerID uuid.UUID `json:"season_player"`
	GP            float64   `json:"gp"`
	Pts           float64   `json:"pts"`
	Reb           float64   `json:"reb"`
	Ast           float64   `json:"ast"`
	NetRating     float64   `json:"net_rating"`
	OrebPct       float64   `json:"oreb_pct"`
	DrebPct       float64   `json:"dreb_pct"`
	UsgPct        float64   `json:"usg_pct"`
	TsPct         float64   `json:"ts_pct"`
	AstPct        float64   `json:"ast_pct"`
}


func sendDataToNestJS(endpoint string, data interface{}) error {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}

	resp, err := http.Post(endpoint, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("HTTP request failed with status: %s", resp.Status)
	}

	return nil
}

func insertCollege(name string) error {
	collegeData := College{Name: name}
	return sendDataToNestJS(nestJSEndpoint+"/insertCollege", collegeData)
}

func insertSeason(year string) error {
	seasonData := Season{Year: year}
	return sendDataToNestJS(nestJSEndpoint+"/insertSeason", seasonData)
}

func insertPlayer(player Player) error {
	return sendDataToNestJS(nestJSEndpoint+"/players/insertPlayer", player)
}

func insertPlayerStats(stats PlayerStats) error {
	return sendDataToNestJS(nestJSEndpoint+"/insertPlayerStats", stats)
}

func parseFloat(s string) float64 {
	val, err := strconv.ParseFloat(s, 64)
	if err != nil {
		log.Printf("Error parsing float: %v", err)
	}
	return val
}

func handleRabbitMQMessages(ch *amqp.Channel) {
	msgs, err := ch.Consume(
		queueName,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatal("Error consuming RabbitMQ messages:", err)
	}

	for msg := range msgs {
		xmlData := string(msg.Body)

		root := etree.NewDocument()
		if err := root.ReadFromString(xmlData); err != nil {
			log.Println("Error parsing XML data:", err)
			continue
		}

		colleges := make(map[string]bool)
		seasons := make(map[string]bool)
		players := make([]Player, 0)
		stats := make([]PlayerStats, 0)

		for _, playerElement := range root.FindElements(".//Player") {
			college := playerElement.FindElement("college/name").Text()
			season := playerElement.FindElement("season").Text()

			/* if _, exists := colleges[college]; !exists {
				colleges[college] = true
				if err := insertCollege(college); err != nil {
					log.Println("Error inserting college:", err)
				}
			}

			if _, exists := seasons[season]; !exists {
				seasons[season] = true
				if err := insertSeason(season); err != nil {
					log.Println("Error inserting season:", err)
				}
			} */

			player := Player{
				Name:       playerElement.FindElement("name").Text(),
				Country:    playerElement.FindElement("country").Text(),
				Age:        parseFloat(playerElement.FindElement("age").Text()),
				Height:     int(parseFloat(playerElement.FindElement("height").Text())),
				Weight:     int(parseFloat(playerElement.FindElement("weight").Text())),
				DraftYear:  playerElement.FindElement("draft_year").Text(),
				DraftRound: playerElement.FindElement("draft_round").Text(),
				DraftNumber: playerElement.FindElement("draft_number").Text(),
			}

			stats := PlayerStats{
				PlayerName: player.Name,
				GP:         parseFloat(playerElement.FindElement("stats/gp").Text()),
				Pts:        parseFloat(playerElement.FindElement("stats/pts").Text()),
				Reb:        parseFloat(playerElement.FindElement("stats/reb").Text()),
				Ast:        parseFloat(playerElement.FindElement("stats/ast").Text()),
				NetRating:  parseFloat(playerElement.FindElement("stats/net_rating").Text()),
				OrebPct:    parseFloat(playerElement.FindElement("stats/oreb_pct").Text()),
				DrebPct:    parseFloat(playerElement.FindElement("stats/dreb_pct").Text()),
				UsgPct:     parseFloat(playerElement.FindElement("stats/usg_pct").Text()),
				TsPct:      parseFloat(playerElement.FindElement("stats/ts_pct").Text()),
				AstPct:     parseFloat(playerElement.FindElement("stats/ast_pct").Text()),
			}

			players = append(players, player)
			stats = append(stats, stats)
		}

		for _, player := range players {
			if err := insertPlayer(player); err != nil {
				log.Println("Error inserting player:", err)
			}
		}

		/* for _, stat := range stats {
			if err := insertPlayerStats(stat); err != nil {
				log.Println("Error inserting player stats:", err)
			}
		} */
	}
}

func main() {
	conn, err := amqp.Dial(rabbitMQURL)
	if err != nil {
		log.Fatal("Error connecting to RabbitMQ:", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatal("Error creating RabbitMQ channel:", err)
	}
	defer ch.Close()

	_, err = ch.QueueDeclare(
		queueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatal("Error declaring RabbitMQ queue:", err)
	}

	handleRabbitMQMessages(ch)
}

