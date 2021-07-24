# Using python slim-buster
FROM codex51/codex:buster

# Clone
RUN git clone https://github.com/Codex51/Codex.git /root/usercodex
# Working directory
WORKDIR /root/usercodex
# Install requirements
RUN pip3 install -U -r requirements.txt
# ENV
ENV PATH="/home/usercodex/bin:$PATH"

RUN chmod 777 /home/Codex \
    && mkdir /home/Codex/bin/
# Workdir for bash
WORKDIR /home/Codex

CMD ["bash","./resources/starting_up/getstart.sh"]
