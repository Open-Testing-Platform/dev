main_go_gw = """
package main

import (
	"context"
	"flag"
	"net/http"

	"github.com/golang/glog"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"

	gw "github.com/open-testing-platform/go-rpc/{SERVICE_NAME}"
)

var (
	// command-line options:
	// gRPC server endpoint
	grpcServerEndpoint = flag.String("grpc-server-endpoint", "{RPC_ENDPOINT}", "gRPC server endpoint")
)

func run() error {{
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// Register gRPC server endpoint
	// Note: Make sure the gRPC server is running properly and accessible
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{{grpc.WithInsecure()}}
	err := gw.RegisterSampleHandlerFromEndpoint(ctx, mux, *grpcServerEndpoint, opts)
	if err != nil {{
		return err
	}}

	// Start HTTP server (and proxy calls to gRPC server endpoint)
	return http.ListenAndServe(":{HTTP_PORT}", mux)
}}

func main() {
  flag.Parse()
  defer glog.Flush()

  if err := run(); err != nil {
    glog.Fatal(err)
  }
}
"""

dockerfile_go_gw = """
FROM golang:1.16-alpine

WORKDIR /app

ADD . .

RUN go mod init github.com/open-testing-platform/grpc-gateway && \
	go mod tidy && \
	go build -o main

FROM alpine

WORKDIR /app

COPY --from=0 /app/main .

EXPOSE {HTTP_PORT}

ENTRYPOINT [ "./main" ]

CMD /bin/sh
"""
