# Using python slim-buster
FROM codex51/codex:buster

# Clone branch
RUN git clone -b master https://github.com/Codex51/Codex /home/usercodex \
    && chmod 777 /home/usercodex/ \
    && mkdir /home/usercodex/bin/

COPY ./sample_config.py ./exampleconfig.py /home/usercodex/

# Path
ENV PATH="/home/usercodex/bin:$PATH"

# working directory 
WORKDIR /home/usercodex

CMD ["bash","./resources/starting_up/getstart.sh"]
