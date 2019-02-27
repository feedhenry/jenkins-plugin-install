FROM python:3.6

RUN git clone https://github.com/adamsaleh/jenkins-plugin-install.git
WORKDIR jenkins-plugin-install
RUN pip install -r requirements.txt && python setup.py install
