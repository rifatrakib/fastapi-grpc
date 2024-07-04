from __future__ import print_function
import logging

import grpc

import product_pb2
import product_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = product_pb2_grpc.ProductStub(channel)
        for page in range(3):
            response = stub.GetProducts(product_pb2.GetProductsRequest(page=page + 1))
            print(response.products)

        for i in range(6):
            response = stub.GetProductsById(product_pb2.GetProductsByIdRequest(id=i + 1))
            print(response.product)


if __name__ == "__main__":
    logging.basicConfig()
    run()
