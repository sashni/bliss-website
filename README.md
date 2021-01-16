# bliss-website
e-commerce Flask application for Bliss International Ltd.

Application Features include:
- portal for customers to view and order products
- portal for admin to add, update and delete products available & view order/customer history.

Run Instructions:
- install requirements
`export FLASK_APP=bliss`
- (export FLASK_APP=development)
- flask db init
- flask db migrate -m "migration message"
- flask db upgrade
- flask run
