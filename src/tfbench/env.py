from dotenv import dotenv_values

ENV = dotenv_values(".env")

assert ENV, "No .env file found! Please create one with the required variables."
