#!/bin/bash
sudo rm -rf bin/*
sudo mkarchiso -v -w bin/ -o bin/ releng/
