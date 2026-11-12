# Week 6 exercise: from script to automated pipeline

* CMKL 41-645 Software Engineering for AI-Enabled Systems
* Week 6: Automating the ML Pipeline

**Individual work · about 30 minutes**

## Learning outcomes

By the end of this exercise, you should be able to:

1. Split a monolithic training script into pipeline stages with clear inputs and outputs.
2. Make one stage robust to new data and prove the fix with a test.
3. Run the pipeline automatically on GitHub Actions, with an evaluation gate that stops a bad model.

## Scenario

You work for an online real-estate marketplace that shows a predicted fair value for every home. The model was built in a notebook and later pasted into `train_all.py`. It loads, cleans, encodes, trains, evaluates and saves in one file. Once a year someone runs it by hand.

The data team has just exported the first sales of 2026 (`data/sales_2026_q1.csv`). Your job is to turn the script into a pipeline that can take in new data and run without anyone watching.

```
collect ──► clean ──► features ──► train ──► evaluate (gate) ──► out/model.joblib
pipeline/   pipeline/  pipeline/    pipeline/  pipeline/
collect.py  clean.py   features.py  train.py   evaluate.py   ◄── run_pipeline.py chains them
```

---

## 0. Setup (3 min)

1. **Fork** this repository (top right on GitHub) into your own account.
2. Get a terminal with Python. Pick **one** option:
   - **Your machine** (Python 3.9 or newer):
     ```bash
     git clone https://github.com/<your-username>/se4ai-pipeline.git
     cd se4ai-pipeline
     python -m venv .venv
     source .venv/bin/activate        # Windows: .venv\Scripts\activate
     pip install -r requirements.txt
     ```
   - **No Python installed?** On your fork, click **Code → Codespaces → Create codespace on main**. Everything is installed for you.
3. Check that the old script still works:
   ```bash
   python train_all.py
   ```
   You should see `MAE: $35,734` and `saved out/model.joblib`.

> **Stuck?** On Windows, try `py` instead of `python`. Always run commands from the repository root (the folder with this README).

---

## Task 1. Modularize (10 min)

`train_all.py` has six numbered blocks. Move blocks 1–4 into the matching stubs in `pipeline/`. Each stub has a docstring that says what it takes in and what it must return.

| Block in `train_all.py` | Goes into |
|---|---|
| 1. collect | `pipeline/collect.py` → `load_sales(paths)` |
| 2. clean | `pipeline/clean.py` → `clean_sales(df)` |
| 3. features | `pipeline/features.py` → `encode(df)` |
| 4. train (only the model lines) | `pipeline/train.py` → `train_model(X, y, max_depth)` |

`evaluate.py` and `run_pipeline.py` are already written.

When you are done:

```bash
python run_pipeline.py
```

It should print the **same MAE as the script** ($35,734) and save `out/model.joblib` and `out/metrics.json`.

> **Stuck?**
> - Each function gets its input as a parameter instead of using a global `df`, and must `return` its result.
> - `encode` returns two things: `return X, y`.
> - Don't copy the `USE_LOG_PRICE` experiment. Dead code paths are an antipattern.

---

## Task 2. New data arrives (8 min)

1. In `run_pipeline.py`, add the new file to `DATA_FILES`:
   ```python
   DATA_FILES = [
       Path("data/sales_2025.csv"),
       Path("data/sales_2026_q1.csv"),
   ]
   ```
2. Run `python run_pipeline.py`. It crashes. Open `data/sales_2026_q1.csv` and compare it with the 2025 file. What changed?
3. Run the tests, which describe what the clean stage must guarantee:
   ```bash
   pytest
   ```
4. Fix `clean_sales` until `pytest` passes, then run `python run_pipeline.py` again. It should pass the evaluation gate.

> **Stuck?**
> - Dates: `pd.to_datetime(df["sold_date"], format="ISO8601", utc=True)` reads both formats.
> - Missing `sqft`: decide whether to drop those rows (`dropna(subset=["sqft"])`) or fill them in. Be ready to say why.
> - A tree model will happily train on missing values without any error. That is exactly the kind of silent problem a test catches.

---

## Task 3. Automate (7 min)

1. On GitHub, open the **Actions** tab of your fork and click **"I understand my workflows, go ahead and enable them"**. Forks start with Actions turned off.
2. Commit and push your work:
   ```bash
   git add -A
   git commit -m "Split training script into pipeline stages"
   git push
   ```
3. Watch the **ml-pipeline** run in the Actions tab. It installs the dependencies, runs `pytest`, then runs `run_pipeline.py`. When it is green, open the run and download the **model** artifact. That artifact is your trained model, built by a machine rather than by you.
4. Now break it on purpose. Set `MAX_DEPTH = 1` in `run_pipeline.py`, then commit and push. The evaluation gate should fail the run (red ✗), and no model artifact is produced.
5. Set `MAX_DEPTH` back to `8` and push again, so your latest run is green.

The pipeline definition is in `.github/workflows/pipeline.yml`. Read it: it is only about 30 lines.

> **Stuck?**
> - If no run appears, check that Actions is enabled (step 1). You can also click **Run workflow** to start one by hand.
> - If `git push` asks for a password, use the Codespace, or GitHub Desktop, or sign in with `gh auth login`.

---

## Stretch goals (if you finish early)

- **Retrain on a schedule:** uncomment the `schedule:` lines in `.github/workflows/pipeline.yml`.
- **Validate the data:** make `load_sales` raise a clear error if a required column is missing. Add a test for it.

---

## Optional: orchestrate with Apache Airflow (15–20 min, after Task 2)

GitHub Actions ran your pipeline as one command. A **workflow orchestrator** such as [Apache Airflow](https://airflow.apache.org/) runs each stage as a separate **task**. It knows which tasks depend on which, so it can retry a failed task on its own, show every run in a web UI and start runs on a schedule. [`orchestration/dags/home_value_pipeline.py`](orchestration/dags/home_value_pipeline.py) defines the pipeline as an Airflow **DAG** (directed acyclic graph):

```
collect ──► clean ──► features ──► train ──► evaluate
```

Each task calls **your** stage function from `pipeline/` and saves its result as a file in `out/airflow/` for the next task. Finish Tasks 1 and 2 first.

### 1. Get Airflow (5 min)

Airflow does not run natively on Windows, so use a Codespace if you are on Windows or have no Python 3.11+:

- **Codespace with Airflow (recommended):** on your fork, click **Code → Codespaces → ⋯ → New with options**. Under **Dev container configuration**, choose **SE4AI Week 6 pipeline + Apache Airflow**, then **Create codespace**. Setup installs Airflow for you; it takes a few minutes.
- **Your machine (macOS or Linux, Python 3.11 or newer):** in your activated virtual environment, run
  ```bash
  bash orchestration/install_airflow.sh
  ```

### 2. Run the DAG once in the terminal (3 min)

```bash
./orchestration/airflow.sh dags test home_value_pipeline
```

You should see the five tasks run in order, `MAE: $34,585`, and finally `state=success`. The first run also sets up Airflow's database in `.airflow/`, which is ignored by git.

### 3. Watch it in the web UI (10 min)

```bash
./orchestration/airflow.sh standalone
```

Wait until the output stops scrolling (about 10–30 seconds). Then open port **8080**: in a Codespace, click **Open in Browser** in the pop-up or the **Ports** tab; on your machine, go to <http://localhost:8080>. There is no login.

1. Open **home_value_pipeline**, click **Trigger** (top right), then **Trigger** again in the dialog. Click the graph icon (**Show Graph**) at the top of the left panel and watch each task turn green.
2. Click the **evaluate** task and open its **Logs** tab: you should find your MAE.
3. Break the gate again: set `MAX_DEPTH = 1` in `run_pipeline.py`, save, and trigger a new run. Which task fails, and which tasks still succeed? Set it back to `8`.
4. Press **Ctrl+C** in the terminal to stop Airflow.

> **Stuck?**
> - `NotImplementedError` in a task log: finish Task 1 first.
> - Port 8080 is already in use: stop the other program, or the earlier Airflow, with Ctrl+C.
> - Codespaces count against your free monthly quota: **stop the Codespace** when you are done (Code → Codespaces → ⋯ → Stop codespace).

**Think about it:** GitHub Actions and Airflow both ran your pipeline. What does Airflow give you that the Actions workflow does not, and what does it cost to run it?

## Reflection (2 min)

Answer the three questions in [`REFLECTION.md`](REFLECTION.md), then commit and push.

## How to submit

Submit the URL of your fork. Your fork should show:

- [ ] a **green** ml-pipeline run on the latest commit, with a **model** artifact;
- [ ] `pytest` passing (it is part of that run);
- [ ] `REFLECTION.md` filled in.
