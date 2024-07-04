from concurrent import futures
import logging

import grpc

import product_pb2
import product_pb2_grpc

products = [
    {"id": 1, "name": "Laptop", "price": 800.00, "description": "New Mac Pro"},
    {"id": 2, "name": "Mouse", "price": 40.00, "description": "New Mac Pro"},
    {"id": 3, "name": "Keyboard", "price": 40.00, "description": "New Mac Pro"},
    {"id": 4, "name": "Monitor", "price": 400.00, "description": "New Mac Pro"},
    {"id": 5, "name": "Headphones", "price": 40.00, "description": "New Mac Pro"},
]


class Product(product_pb2_grpc.ProductServicer):
    def GetProducts(self, request, context):
        page_number = request.page
        offset = (page_number - 1) * 2
        limit = offset + 2
        logging.info(f"Page number: {page_number}")
        logging.info(f"Offset: {offset}")
        logging.info(f"Limit: {limit}")
        data = products[offset:limit]
        return product_pb2.GetProductsResponse(products=[product_pb2.Item(**product) for product in data])

    def GetProductsById(self, request, context):
        product_id = request.id
        logging.info(f"Product ID: {product_id}")

        data = None
        for product in products:
            if product["id"] == product_id:
                data = product
                break

        if data:
            return product_pb2.GetProductsByIdResponse(product=product_pb2.Item(**data))

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Product not found")
        return product_pb2.Item()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServicer_to_server(Product(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
