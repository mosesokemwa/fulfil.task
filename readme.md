## File importer using Flask, Celery and Redis


### Product specification
#### STORY 1:
- [ ] As a user of the application, I should be able to upload a large CSV file of 500K products [see here](https://drive.google.com/file/d/19J8MfLmRqAIdBXBCiZT4ABTjEa2RqSmt/view?usp=sharing)
- [ ] If there are existing products it should overwrite the data.
    * De-duplication can be done using the SKU of the product.
    * SKU is case insensitive.
    * Though not in the CSV file.
- [ ] Some products should be active and others should be inactive.
- [ ] The SKU is expected to be unique.

#### STORY 2:
- [ ] Users are also expected to see the upload progress
- [ ] It can be as simple as displaying a progress bar on the UI.


#### Toolkit
Acme Inc. is also opinionated about its tech stack. The tools should be:
1. Web framework: Flask
2. Asynchronous execution: Celery with Redis
3. ORM: SQLAlchemy.
4. Database: Postgres

### Important Note
The application would be;
1. containerized and deployed on stateless servers
2. The server has a strict request timeout of 30 seconds. Please keep this in mind while coming up with a solution.
