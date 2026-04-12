import json
import os
from pathlib import Path

def get_config_path()->Path:
    config_home=os.environ.get("XDG_CONFIG_HOME")
    if not config_home:
        config_home=os.path.expanduser("~/.config")
    return Path(config_home) / "gittot" / "config.json"

def load_config() -> dict:
    path=get_config_path()
    if not path.exists():
        return {}
    
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        print("Something went wrong with the config file.")
        return {}

def save_config(data:dict)->None:
    path=get_config_path()
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf-8"
    )

    try:
        os.chmod(path,0o600)
    except Exception:
        pass

def bind_token(token:str)->None:
    token=token.strip()
    if not token:
        raise ValueError("Token cannot be empty.")

    data=load_config()
    data["github_token"]=token
    save_config(data)

def get_bound_token()->str|None:
    data=load_config()
    token = data.get("github_token")

    if token and isinstance(token, str) and token.strip():
        return token.strip()
    return None

def unbind_token() -> bool:
    data = load_config()

    if "github_token" in data:
        del data["github_token"]
        save_config(data)
        return True

    return False

    
     