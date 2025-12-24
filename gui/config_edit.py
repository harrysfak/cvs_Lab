import importlib.util
from pathlib import Path


def load_config_module(config_path: Path):
    spec = importlib.util.spec_from_file_location("app_config", str(config_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_config_previous_folder(start_path, filename="config.py"):
    # start_path = το αρχείο που τρέχει (π.χ. gui/config_edit.py)
    start = Path(start_path).resolve()
    candidate = start.parent.parent / filename  # ακριβώς 1 φάκελο πάνω από το gui/

    if candidate.exists():
        return candidate

    raise FileNotFoundError(f"{filename} δεν βρέθηκε στον προηγούμενο φάκελο: {candidate.parent}")


class ConfigEditor:
    """Κλάση για επεξεργασία του config.py"""

    def __init__(self):
        self.config_path = find_config_previous_folder(__file__)
        self.config_values = {}
        self.load_config()

    def load_config(self):
        """Φορτώνει τιμές από το config.py που βρήκαμε"""
        cfg = load_config_module(self.config_path)

        self.config_values = {
            'BASE_PATH': getattr(cfg, 'BASE_PATH', ''),
            'OUTPUT_PATH': getattr(cfg, 'OUTPUT_PATH', ''),
            'BATCH_SIZE': getattr(cfg, 'BATCH_SIZE', 87),
            'T_SAMPLE_INCREMENT': getattr(cfg, 'T_SAMPLE_INCREMENT', 43),
            'T_ZERO_INCREMENT': getattr(cfg, 'T_ZERO_INCREMENT', 19),
            'DEFAULT_PRODUCT': getattr(cfg, 'DEFAULT_PRODUCT', 'AIG NEWXX'),
            'DEFAULT_TIME': getattr(cfg, 'DEFAULT_TIME', '11:00'),
            'DEFAULT_REP': getattr(cfg, 'DEFAULT_REP', 1),
            'DROP_ZERO_NUTRIENTS': getattr(cfg, 'DROP_ZERO_NUTRIENTS', True),
        }

    def save_config(self, new_values):
        """Αποθηκεύει τις νέες τιμές στο config.py"""
        try:
            lines = self.config_path.read_text(encoding="utf-8").splitlines(True)
            new_lines = []

            for line in lines:
                s = line.strip()

                if s.startswith("BASE_PATH "):
                    base = str(new_values["BASE_PATH"]).replace('"', '\\"')
                    new_lines.append(f'BASE_PATH = r"{base}"\n')

                elif s.startswith("OUTPUT_PATH"):
                    output = str(new_values["OUTPUT_PATH"]).replace('"', '\\"')
                    new_lines.append(f'OUTPUT_PATH = r"{output}"\n')

                elif s.startswith("BATCH_SIZE"):
                    new_lines.append(f'BATCH_SIZE = {int(new_values["BATCH_SIZE"])}\n')

                elif s.startswith("T_SAMPLE_INCREMENT"):
                    new_lines.append(f'T_SAMPLE_INCREMENT = {int(new_values["T_SAMPLE_INCREMENT"])}\n')

                elif s.startswith("T_ZERO_INCREMENT"):
                    new_lines.append(f'T_ZERO_INCREMENT = {int(new_values["T_ZERO_INCREMENT"])}\n')

                elif s.startswith("DEFAULT_PRODUCT"):
                    prod = str(new_values["DEFAULT_PRODUCT"]).replace('"', '\\"')
                    new_lines.append(f'DEFAULT_PRODUCT = "{prod}"\n')

                elif s.startswith("DEFAULT_TIME"):
                    new_lines.append(f'DEFAULT_TIME = "{new_values["DEFAULT_TIME"]}"\n')

                elif s.startswith("DEFAULT_REP"):
                    new_lines.append(f'DEFAULT_REP = {int(new_values["DEFAULT_REP"])}\n')

                elif s.startswith("DROP_ZERO_NUTRIENTS"):
                    new_lines.append(f'DROP_ZERO_NUTRIENTS = {bool(new_values["DROP_ZERO_NUTRIENTS"])}\n')

                else:
                    new_lines.append(line)

            self.config_path.write_text("".join(new_lines), encoding="utf-8")
            return True

        except Exception as e:
            print(f"Error saving config: {e}")
            return False
