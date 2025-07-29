# Video Fragment Ingest 

Cloud Streaming Interfaces.

# Install

```bash
pip3 install video-fragment-ingest
```

# Api Reference Docs

https://vlt-ai.github.io/thrud/index.html

# Content

1. [Intro](#intro)
2. [Usage](#usage)
3. [Dependencies](#dependencies)

# Intro

Consume Streaming `VideoIngestFragment` messages and hardware decode them into `cpu` `np.ndarray`.


```protobuf
message VideoIngestFragment {
  string customer_id = 1;
  string facility_id = 2;
  string camera_id = 3;
  string s3_uri = 4;
  float duration = 5;
  google.protobuf.Timestamp start_ts = 7;
  map<string, string> tags = 8;
}
```

# Usage (Doc on private repo)

[Example](./example/consumer/sample_app.py)

## Run example

Build dev container:

```bash
$./
docker build -f example/consumer/dev.Dockerfile . -t thrud.local
```

Enter the container:

```bash
$./
bash example/consumer/run_dev_container.sh
```

Once inside the container:

```
python3 example/consumer/sample_app.py
```

see `python3 example/consumer/sample_app.py -h`


Run a mock producer:

```bash
cd example/producer/
docker compose up -d --build
```

# Dependencies

To run this package the environment must:

1. Have an available `nvidia` gpu device.
2. `DEEPSTREAM_VER="7.1"`
3. `GSTREAMER_VER="1.24.12"`

