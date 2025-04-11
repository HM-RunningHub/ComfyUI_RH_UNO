from pathlib import Path
import json
import os

json_path = Path(__file__).parent.parent.parent / "config.json"
node_model_config = json.loads(json_path.resolve().read_text(encoding="utf-8"))
vae_base_path = node_model_config['vae_base']
if vae_base_path.strip() == "":
    vae_base_path = os.path.join(folder_paths.models_dir, 'vae')
ckpt_path = os.path.join(vae_base_path, node_model_config['vae'])