# Use the official Golang base image
FROM golang:1.16-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go application
RUN go mod download golang.org/x/sys
RUN go mod download github.com/stretchr/testify
RUN go mod download golang.org/x/sys
RUN go mod download github.com/davecgh/go-spew
ENV CGO_ENABLED=0 
RUN go build -ldflags "-X main.version=1.0.0" -o fetcher fetcher

# Expose the port on which the application will listen
EXPOSE 8000

# Run the application
CMD ["./app"]
