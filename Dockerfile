# Using python slim-buster
FROM codex51/codex:buster

# Clone
RUN git clone https://github.com/Codex51/Codex.git /root/usercodex
#working directory 
WORKDIR /root/usercodex

# Install requirements
RUN pip3 install -U -r requirements.txt

ENV PATH="/home/usercodex/bin:$PATH"

CMD ["python3","-m","./run"]
