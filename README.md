# neural-network-tutorial

A basic demo on a full stack app involving neural network training and
deployment.

Easiest way to run the demo:

  1. Install docker
  2. Clone this repo:
  ```
  git clone https://github.com/env3d/neural-network-tutorial.git
  ```
  3. Run with `docker-compose`
  ```
  docker-compose up -d
  ```

Visit `http://localhost:5000` for the main inference app, where
we use tensorflowjs to load the model, allow a user to draw
a shape, and identify if the shape belongs to one of the four
classes.

`http://localhost:5000/train` will bring you to the training
page, where users can provide training data.  The data
is stored in a postgres database.

`http://localhost:8888` will give you to the notebook.
Run the following code to train the neural network with
user data for today:

```
import train
train.train_today()
```

# Interesting files

  index.html - The prediction UI

  train.html - The training UI

  app.py - Simple flask app to server the UI, as well as create a route
  to write data to postgres

  train.py - Performs the training using the keras library and write model
  to the `my_icons.json/` directory



