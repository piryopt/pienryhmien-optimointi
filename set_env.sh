#!/bin/sh

while read line;
    do export ${line};
done < .env