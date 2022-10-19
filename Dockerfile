# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

#
COPY
COPY ./main.py /code/main.py

#
COPY ./package /code/package

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./package /code/package

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

