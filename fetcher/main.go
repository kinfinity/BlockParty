package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"context"
	"fmt"
	"os"

	"github.com/gorilla/mux"
	// "github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Token struct {
	ID  int    `json:"id"`
	NAME string `json:"name"`
	IMAGE string `json:"image"`
	DESCRIPTION string `json:"description"`
	CID string `json:"cid"`
}

var db *pgxpool.Pool

func main() {
	// Replace the connection details with your RDS information
	dbHost := ""
	dbPort := ""
	dbUser :=""
	dbPassword := ""
	dbName := ""

	// Create the connection string
	// connectionString := dbUser + ":" + dbPassword + "@tcp(" + dbHost + ":" + dbPort + ")/" + dbName
	connectionString := "postgresql://" +dbUser + ":" + dbPassword + "@" + dbHost + ":" + dbPort + "/" + dbName

	// Connect to the database
	poolConfig, err := pgxpool.ParseConfig(connectionString)
	if err != nil {
		log.Fatalln("Unable to parse DATABASE_URL:", err)
	}

	db, err = pgxpool.NewWithConfig(context.Background(), poolConfig)
	if err != nil {
		log.Fatalln("Unable to create connection pool:", err)
	}
	// defer conn.Close(context.Background())

	// Initialize the router
	router := mux.NewRouter()

	// Define the API routes
	router.HandleFunc("/tokens", getAllTokens).Methods("GET")
	router.HandleFunc("/tokens/{cid}", getTokenByCID).Methods("GET")

	// Start the server
	log.Println("Server started on port 8000")
	log.Fatal(http.ListenAndServe(":8000", router))
}

func getAllTokens(w http.ResponseWriter, r *http.Request) {
	// Fetch all tokens from the database
	rows,err := db.Query(context.Background(), "SELECT * FROM public.metadata")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Query failed: %v\n", err)
		os.Exit(1)
	}
	defer rows.Close()

	// Create a slice to store the tokens
	var tokens []Token

	// Iterate over the rows
	for rows.Next() {
		var token Token
    	err := rows.Scan(&token.ID, &token.NAME, &token.IMAGE, &token.DESCRIPTION, &token.CID)
		if err != nil {
			log.Fatal(err)
		}
		tokens = append(tokens, token)
	}

	// Convert the tokens to JSON
	jsonData, err := json.Marshal(tokens)
	if err != nil {
		log.Fatal(err)
	}

	// Set the Content-Type header and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func getTokenByCID(w http.ResponseWriter, r *http.Request) {
	// Get the CID parameter from the request URL
	vars := mux.Vars(r)
	cid := vars["cid"]
	fmt.Println(cid)

	// Fetch the token from the database for the given CID
	row := db.QueryRow(context.Background(), "SELECT * FROM public.metadata WHERE cid = $1", cid)

	var token Token
	err := row.Scan(&token.ID, &token.NAME, &token.IMAGE, &token.DESCRIPTION, &token.CID)
	if err != nil {
		if err == sql.ErrNoRows {
			// Return a 404 Not Found if the token doesn't exist
			http.NotFound(w, r)
			return
		}
		log.Fatal(err)
	}

	// Convert the token to JSON
	jsonData, err := json.Marshal(token)
	if err != nil {
		log.Fatal(err)
	}

	// Set the Content-Type header and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}
