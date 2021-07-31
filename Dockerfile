# Using python slim-buster
FROM codex51/codex:buster

# Clone
RUN git clone https://github.com/ipindanger/Codex-z.git /root/usercodex
#working directory 
WORKDIR /root/usercodex

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/usercodex/bin:$PATH"

CMD ["python3","-m","usercodex"]
