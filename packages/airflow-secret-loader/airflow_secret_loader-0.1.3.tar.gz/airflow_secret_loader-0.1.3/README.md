
# airflow-secret-loader

Automatically load secrets from AWS Secrets Manager into Airflow environment variables so that `Variable.get()` works seamlessly in DAGs.

This is designed for use in **Astronomer (Astro)** or any Airflow deployment where credentials to fetch secrets are provided via environment variables.

---

## 📦 Installation

Install from PyPI:

```bash
pip install airflow-secret-loader
```

Or from GitHub:

```bash
pip install git+https://github.com/rajeshkbathula/airflow-secret-loader.git
```

---

## ⚙️ Required Environment Variables

Set the following **environment variables** in your Astro deployment or Airflow environment:

| Variable             | Description |
|----------------------|-------------|
| `SECRET_ROLE_ARN`    | The IAM Role ARN to assume before accessing the secret |
| `SECRET_ID`          | The AWS Secrets Manager Secret ID or ARN |

Your secret in AWS should be stored in **JSON format**, e.g.:

```json
{
  "snowflake_user": "astro_user",
  "snowflake_key": "ABC123",
  "dbt_env": "prod"
}
```

---

## 🚀 Usage in DAG
In your DAG Python file:

`version <= 0.1.2`


```python
from airflow_secret_loader import load_env_from_aws_secret

# Load secrets as AIRFLOW_VAR_* env vars
load_env_from_aws_secret()

from airflow.models import Variable

# Now you can use them like any Airflow Variable
snowflake_user = Variable.get("snowflake_user")
dbt_env = Variable.get("dbt_env")
```

`version > 0.1.3`


```python
import airflow_secret_loader  # automatically triggers the secret loading

from airflow.models import Variable

sf_user = Variable.get("snowflake_user")  # works immediately
```

No need to store these variables in the Airflow metadata database — they'll be picked from environment variables prefixed with `AIRFLOW_VAR_`.

---

## ✅ Benefits

- Works seamlessly with Airflow's native `Variable.get()` logic
- Avoids hardcoding secrets in code or Airflow UI
- Great for Astro or ephemeral environments
- IAM role assumption ensures secure access control

---

## 🛠️ Dev & Build

```bash
# Build the package
make build

# Publish to PyPI (after setting up ~/.pypirc or using a token)
make publish
```

---

## 🔗 Links

- 📘 [Airflow Variables Docs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html)
- 🔐 [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- 🤖 [Astronomer Astro Docs](https://docs.astronomer.io/)

---

## 👨‍💻 Author

Created by [@rajeshkbathula](https://github.com/rajeshkbathula)

---
