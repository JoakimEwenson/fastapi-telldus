# FastAPI proxy for Telldus Live! API

_created by Joakim Ewenson (<joakim@ewenson.se>)_

## Description

A simple FastAPI proxy for fetching Telldus Live! API sensor data without the trouble of implementing OAuth1 in the frontend.

## Deploying

Everything is prepared for deploying on Heroku with a Procfile and requirements.txt provided. To use this you need your own API keys from Telldus and add those to you enviroment with the supplied .env.template as a template for the variable naming. For built in API documentation see https://ewenson-telldus-api.herokuapp.com/docs

## Telldus API

Get your own API keys from https://developer.telldus.com/
