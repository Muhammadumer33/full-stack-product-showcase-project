from database import SessionLocal, engine
from models import Base, Product
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        # Check if data exists
        if db.query(Product).count() > 0:
            logger.info("Data already exists. Skipping seed.")
            return

        products = [
            Product(
                name="Wireless Headphones",
                description="Premium noise-canceling headphones with 20h battery life.",
                price=199.99,
                category="Electronics",
                brand="AudioTech",
                stock=50,
                rating=4.5,
                image_path=""
            ),
            Product(
                name="Smart Watch Pro",
                description="Advanced fitness tracking and health monitoring.",
                price=299.99,
                category="Electronics",
                brand="WristTech",
                stock=30,
                rating=4.8,
                image_path=""
            ),
            Product(
                name="Ergonomic Chair",
                description="Comfortable office chair with lumbar support.",
                price=149.99,
                category="Furniture",
                brand="ComfortSeatz",
                stock=15,
                rating=4.2,
                image_path=""
            ),
             Product(
                name="Mechanical Keyboard",
                description="RGB mechanical keyboard with blue switches.",
                price=89.99,
                category="Electronics",
                brand="KeyMaster",
                stock=100,
                rating=4.7,
                image_path=""
            )
        ]

        db.add_all(products)
        db.commit()
        logger.info(f"Successfully added {len(products)} products!")

    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Database URL from env or default will be used...")
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    seed_data()
