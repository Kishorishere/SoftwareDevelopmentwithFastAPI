import logging
from fastapi import FastAPI
from routers import customer, product, productline, office, employee, order, orderdetail, payment, counts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Fusemachines Week 2 API", version="1.0.0")

app.include_router(counts.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(productline.router)
app.include_router(office.router)
app.include_router(employee.router)
app.include_router(order.router)
app.include_router(orderdetail.router)
app.include_router(payment.router)


@app.get("/")
def root():
    return {"message": "API is running. Visit /docs for Swagger UI."}
