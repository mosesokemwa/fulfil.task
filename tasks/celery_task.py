import csv
import random
import time

from celery.utils.log import get_task_logger
from models import db_session
from models.models import Data, Product

from tasks import celery

logger = get_task_logger(__name__)

@celery.task
def add(x, y):
    logger.info(f'Adds {x} + {y}')
    return x + y


@celery.task(bind=True, countdown=30)
def import_file_task(self, file_path):
    index = 0
    status = ["active", "inactive"]
    total = len(list(csv.reader(open(file_path, "r"))))

    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

        for row in reader:
            product = Product(
                sku=row["sku"],
                name=row["name"],
                description=row["description"],
                status=random.choice(status),
            )

            index += 1
            logger.info(f'Processing row {index} of {total}')
            ### id duplicates are found  update
            try:
                if self.request.id is not None:
                    logger.info('updating state')
                    self.update_state(state="PROGRESS", meta={"current": index, "total": total, "status": "OK"})
                db_session.add(product)
                db_session.commit()

            except Exception as e:
                # update duplicate sku
                logger.info(f'Duplicate SKU {row["sku"]}')
                db_session.rollback()
                q = db_session.query(Product)
                q = q.filter(Product.sku==row["sku"])
                product = q.one()
                product.name = row["name"]
                product.description = row["description"]
                product.status = random.choice(status)
                db_session.commit()
                logger.info(f'Updated SKU {row["sku"]}')
            finally:
                db_session.remove()

        # patch Data models
        data = Data(sku=self.request.id, task_id=self.request.id)
        db_session.add(data)
        db_session.commit()
        return {"id": self.request.id}





