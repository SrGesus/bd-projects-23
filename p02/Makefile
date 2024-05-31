
all:
	cp data/E2-ProjetoBD.ipynb E2-Report-19.ipynb
	zip -r entrega-bd-02-19.zip E2-Report-19.ipynb
	rm E2-Report-19.ipynb
	zip -r entrega-bd-02-19.zip data/populate.sql
	zip -r entrega-bd-02-19.zip app/saude app/app.py app/requirements.txt app/Dockerfile.development

deploy:
	sudo systemctl start docker.service
	cd bdist-workspace && sudo docker compose -f docker-compose..app.yml up
