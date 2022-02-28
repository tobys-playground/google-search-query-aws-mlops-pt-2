FROM ubuntu:20.04

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3-pip \
         python3-setuptools \
         python3-gevent\
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

RUN pip --no-cache-dir install numpy scikit-learn pandas sagemaker flask gunicorn torch transformers tqdm onnx onnxruntime gevent 

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY gpt_neo /opt/program
WORKDIR /opt/program