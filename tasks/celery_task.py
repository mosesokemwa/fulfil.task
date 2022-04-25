import random
import csv
from models import db_session
from models.models import Product
from tasks import celery


@celery.task
def add(x, y):
    return x + y


@celery.task(bind=True)
def import_file_task(self, file_path):
    status = ["active", "inactive"]
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        # total = len(list(reader))
        # index = 0
        # print("-------------file_path------------")
        # print(file_path)
        # print("-------------file_path------------")
        for row in reader:
            product = Product(
                sku=row["sku"],
                name=row["name"],
                description=row["description"],
                status=random.choice(status),
            )
            db_session.add(product)
            db_session.commit()
            return product.sku

            ## id duplicates are found  update
            # try:
            #     db_session.add(product)
            #     db_session.commit()
            #     index += 1
            #     self.update_state(
            #         state="PROGRESS",
            #         meta={"current": index, "total": total, "status": "OK"},
            #     )
            # except Exception as e:
            #     # update duplicate sku
            #     print(f"Error {e}")
            #     db_session.rollback()
            #     product = Product.query.filter_by(sku=row["sku"]).first()
            #     product.name = row["name"]
            #     product.description = row["description"]
            #     product.status = random.choice(status)
            #     db_session.commit()
            #     print(f"{row['sku']} updated")
            # finally:
            #     db_session.remove()
