# Introduction
<hr>

#### Problem
The objective of this project was to solve a problem I had while living in an apartment with multiple tenants sharing the same laundry room: "when is the laundry free?". 

Every time I needed to do laundry I could do one of two things:
1) Walk downstairs, check if the laundry washer and dryer were free, then walk back upstairs, (if free) grab my laundry, and then walk back downstairs. (this also hopes that the laundry wasn't taken in the little amount of time retrieiving my laundry)
2) Walk downstairs with my laundry, check if the laundry washer and dryer were free, (if not free), have to wheel my laundry back upstairs and try again later.

While this was great exercise, there had to be a better way.

#### Solution
Arduino's with accelerometers attached to washing machines...
Home api server, postgres database, and grafana, hosted on raspberry pi...


### Prerequisistes
<hr>

1) UV Package Manger
- `brew install uv`


### To Run Locally
<hr>
It is highly suggested everything using make to simplify development and run actions atomically

The following actions are specified in the Makefile:
- `make env`
    - clears and creates a virtual environment with required python dependencies for the api server

- `make run`
    - runs the api server
