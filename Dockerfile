ARG CUDA_VERSION="12.1"
ARG TORCH_VERSION="2.3.1"
ARG CUDNN_VERSION="8"

FROM pytorch/pytorch:${TORCH_VERSION}-cuda${CUDA_VERSION}-cudnn${CUDNN_VERSION}-runtime

WORKDIR /app
COPY . /app/
RUN pip install -e .
RUN DLWMLS -i /dummyinput -o /dummyoutput -device cpu
ENTRYPOINT ["/usr/bin/python3 /app/scripts/wrapper.py"]
