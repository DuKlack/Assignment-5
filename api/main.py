from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .controllers import sandwich, Resource, recipe, order_detail, orders
from .models import models, schemas
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#ORDERS ENDPOINTS 
@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.delete(db=db, order_id=order_id)


#SANDWICHES ENDPOINTS
@app.post("/sandwiches/", response_model=schemas.Sandwich, tags=["Sandwiches"])
def create_sandwich(item: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwich.create(db=db, sandwich=item)


@app.get("/sandwiches/", response_model=list[schemas.Sandwich], tags=["Sandwiches"])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwich.read_all(db)


@app.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    item = sandwich.read_one(db, sandwich_id=sandwich_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return item


@app.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def update_sandwich(sandwich_id: int, item: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    db_item = sandwich.read_one(db, sandwich_id=sandwich_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich.update(db=db, sandwich=item, sandwich_id=sandwich_id)


@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    item = sandwich.read_one(db, sandwich_id=sandwich_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich.delete(db=db, sandwich_id=sandwich_id)


# RESOURCES ENDPOINTS 
@app.post("/resources/", response_model=schemas.Resource, tags=["Resources"])
def create_resource(item: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return Resource.create(db=db, resource=item)


@app.get("/resources/", response_model=list[schemas.Resource], tags=["Resources"])
def read_resources(db: Session = Depends(get_db)):
    return Resource.read_all(db)


@app.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    item = Resource.read_one(db, resource_id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item


@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_resource(resource_id: int, item: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    db_item = Resource.read_one(db, resource_id=resource_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return Resource.update(db=db, resource=item, resource_id=resource_id)


@app.delete("/resources/{resource_id}", tags=["Resources"])
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    item = Resource.read_one(db, resource_id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return Resource.delete(db=db, resource_id=resource_id)


# ==================== RECIPES ENDPOINTS ====================
@app.post("/recipes/", response_model=schemas.Recipe, tags=["Recipes"])
def create_recipe(item: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return recipe.create(db=db, recipe=item)


@app.get("/recipes/", response_model=list[schemas.Recipe], tags=["Recipes"])
def read_recipes(db: Session = Depends(get_db)):
    return recipe.read_all(db)


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    item = recipe.read_one(db, recipe_id=recipe_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return item


@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def update_recipe(recipe_id: int, item: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    db_item = recipe.read_one(db, recipe_id=recipe_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe.update(db=db, recipe=item, recipe_id=recipe_id)


@app.delete("/recipes/{recipe_id}", tags=["Recipes"])
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    item = recipe.read_one(db, recipe_id=recipe_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe.delete(db=db, recipe_id=recipe_id)


# ORDER DETAILS ENDPOINTS 
@app.post("/order_details/", response_model=schemas.OrderDetail, tags=["Order Details"])
def create_order_detail(item: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return order_detail.create(db=db, order_detail=item)


@app.get("/order_details/", response_model=list[schemas.OrderDetail], tags=["Order Details"])
def read_order_details(db: Session = Depends(get_db)):
    return order_detail.read_all(db)


@app.get("/order_details/{order_detail_id}", response_model=schemas.OrderDetail, tags=["Order Details"])
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    item = order_detail.read_one(db, order_detail_id=order_detail_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return item


@app.put("/order_details/{order_detail_id}", response_model=schemas.OrderDetail, tags=["Order Details"])
def update_order_detail(order_detail_id: int, item: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_item = order_detail.read_one(db, order_detail_id=order_detail_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order_detail.update(db=db, order_detail=item, order_detail_id=order_detail_id)


@app.delete("/order_details/{order_detail_id}", tags=["Order Details"])
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    item = order_detail.read_one(db, order_detail_id=order_detail_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order_detail.delete(db=db, order_detail_id=order_detail_id)