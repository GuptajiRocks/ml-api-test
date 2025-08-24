# ML - TEST API
Here’s the **How to Run** section in clean markdown format:

````markdown
## 🚀 How to Run

### 1. Install dependencies
pip install flask flask_sqlalchemy prophet pandas
````

### 2. Create & seed the database with random data

```bash
flask seed
```

### 3. Run the server

```bash
flask run
```

### 4. Test endpoints

* **Fetch raw data** → [http://127.0.0.1:5000/fetch/device\_1](http://127.0.0.1:5000/fetch/device_1)
* **Predict battery %** → [http://127.0.0.1:5000/predict/device\_1](http://127.0.0.1:5000/predict/device_1)


