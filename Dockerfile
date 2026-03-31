FROM golang:1.25-alpine AS builder
# Install required packages
RUN apk --no-cache add git

WORKDIR /src
# Copy the test directory (assuming your unified test script is in test/stress-test)
COPY test/stress-test/ ./stress-test/

# Build k6 with the influxdb extension (used in dev mode)
RUN go install go.k6.io/xk6/cmd/xk6@latest
RUN xk6 build --with github.com/grafana/xk6-output-influxdb --output /tmp/k6

# ----------------------------------------------------------------
FROM alpine:3.21
RUN apk add --no-cache ca-certificates bash && \
    adduser -D -u 12345 -g 12345 k6

# For convenience, copy the built k6 binary to /usr/bin
COPY --from=builder /tmp/k6 /usr/bin/k6

WORKDIR /app
# Copy the test scripts (choose the one you want to use)
# You can rename or merge your test scripts so you have one file (here named rinha-test.js)
COPY test/stress-test/rinha-test.js .

# Copy the unified entrypoint script that selects the appropriate mode.
COPY test/stress-test/run-test.sh .

# Create a folder for prod reports (if needed)
RUN mkdir -p /reports

# Ensure the run script is executable
RUN chmod +x /app/run-test.sh

# Default entrypoint uses our run script
ENTRYPOINT ["/app/run-test.sh"]