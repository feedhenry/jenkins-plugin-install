FROM python:2

RUN git clone https://github.com/feedhenry/jenkins-plugin-install.git
WORKDIR jenkins-plugin-install
RUN pip install -r requirements.txt && python setup.py install
