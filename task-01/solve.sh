#!/bin/bash
read -p "Enter Base64 string: " b64
echo "$b64" | base64 --decode
echo
