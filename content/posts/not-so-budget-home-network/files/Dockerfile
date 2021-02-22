FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
      curl \
      ca-certificates \
      libgusb2 \
      libusb-1.0-0 \
      usb.ids \
      usbutils \
      expect \
      --no-install-recommends \
      && rm -rf /var/lib/apt/lists/*
RUN curl -s -L https://dl4jz3rbrsfum.cloudfront.net/software/ppb440-linux-x86_x64.sh -o ppb-linux-x86_64.sh \
 && chmod +x ppb-linux-x86_64.sh

COPY install.exp install.exp
RUN chmod +x install.exp && ./install.exp && rm ppb-linux-x86_64.sh

EXPOSE 3052
VOLUME ["/usr/local/ppbe/db_local/"]

ENTRYPOINT ["/usr/local/ppbe/ppbed", "run"]