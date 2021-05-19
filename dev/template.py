main_go_gw = """
package {SERVICE_NAME}

import (
	"context"
	"flag"
	"net/http"

	"github.com/golang/glog"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"

	gw "github.com/open-testing-platform/go-rpc/{SERVICE_NAME}" // Update
)

var (
	// command-line options:
	// gRPC server endpoint
	grpcServerEndpoint = flag.String("grpc-server-endpoint", "{RPC_ENDPOINT}", "gRPC server endpoint")
)

func Run() error {{
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
"""

dockerfile_go_gw = """
FROM golang:1.16-alpine

WORKDIR /app

ADD . .

RUN go build -o main

FROM alpine

WORKDIR /app

COPY --from=0 /app/main .

EXPOSE {HTTP_PORT}

ENTRYPOINT [ "./main" ]

CMD /bin/sh
"""

go_mod_gw = """
module github.com/open-testing-platform/grpc-gateway

go 1.16

require (
	github.com/golang/glog v0.0.0-20210429001901-424d2337a529
	github.com/grpc-ecosystem/grpc-gateway/v2 v2.4.0
	github.com/open-testing-platform/go-rpc v0.0.0-20210519094701-23c33ef2369c
	google.golang.org/grpc v1.37.1
)
"""
