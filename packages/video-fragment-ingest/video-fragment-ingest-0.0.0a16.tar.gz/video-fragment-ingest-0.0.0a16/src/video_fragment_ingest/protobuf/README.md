# Bifrost 

![Bifrost](static/bifrost.jpg)
> Bifrost (pronounced roughly “BIF-roast;” Old Norse Bifröst) is the rainbow bridge that connects Asgard, the world of 
>the Aesir tribe of gods, with Midgard, the world of humanity. Bifrost is guarded by the ever-vigilant god Heimdall.
>
> -- https://norse-mythology.org/
>
>

## Description 
**Common repository of serivce and protocol definitions**

This repository is used as a git submodule in other service (e.g. Odin) as a git submodule to compile and build 
appropriate language binding for messages and client/service stubs.

## Service List
* **Frigg** - ML Prediction services (e.g. object_detection)
* **Odin** - Core VOLT API services for clients/services and VOLT SOC software
* **Huginn** - Video Coding & Inferring (calling Frigg) Service 
* **Muninn** - Flink service for streaming feature generation based on Huggin's output 
* **Loki** - Desktop Application for VOLT SOC 

## Production Endpoints
Endpoint are hidden behind loadbalancers which can be found here:

[https://volt-public.s3.us-east-1.amazonaws.com/metadata/service-discovery.json](https://volt-public.s3.us-east-1.amazonaws.com/metadata/service-discovery.json)