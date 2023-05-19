#!/bin/bash

docker build . -t ohtu-projekti

docker run -it -p 5000:5000 ohtu-projekti
