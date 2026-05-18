from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="opendatalab/OmniDocBench",
    repo_type="dataset",
    local_dir="data/OmniDocBench",
    local_dir_use_symlinks=False,
)