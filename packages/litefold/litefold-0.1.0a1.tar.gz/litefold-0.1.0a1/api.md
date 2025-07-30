# Litefold

Methods:

- <code title="get /">client.<a href="./src/litefold/_client.py">retrieve</a>() -> object</code>

# Upload

Methods:

- <code title="post /upload/fasta">client.upload.<a href="./src/litefold/resources/upload.py">create_fasta</a>(\*\*<a href="src/litefold/types/upload_create_fasta_params.py">params</a>) -> object</code>
- <code title="get /upload/stats">client.upload.<a href="./src/litefold/resources/upload.py">get_stats</a>() -> object</code>

# StructurePrediction

Methods:

- <code title="get /structure-prediction/results/{job_name}">client.structure_prediction.<a href="./src/litefold/resources/structure_prediction.py">get_results</a>(job_name) -> object</code>
- <code title="get /structure-prediction/status/{job_name}">client.structure_prediction.<a href="./src/litefold/resources/structure_prediction.py">get_status</a>(job_name) -> object</code>
- <code title="post /structure-prediction/submit">client.structure_prediction.<a href="./src/litefold/resources/structure_prediction.py">submit</a>(\*\*<a href="src/litefold/types/structure_prediction_submit_params.py">params</a>) -> object</code>
