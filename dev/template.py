main_go_gw = '''
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

func Run() error {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// Register gRPC server endpoint
	// Note: Make sure the gRPC server is running properly and accessible
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithInsecure()}
	err := gw.RegisterSampleHandlerFromEndpoint(ctx, mux, *grpcServerEndpoint, opts)
	if err != nil {
		return err
	}

	glog.Infoln("Server is starting...")

	// Start HTTP server (and proxy calls to gRPC server endpoint)
	return http.ListenAndServe(":{HTTP_PORT}", mux)
}
'''