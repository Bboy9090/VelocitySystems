"""Bobby Dev Mode modules."""
from .dossier import run_dossier
from .warhammer import run_warhammer
from .darklab import run_dark_lab
from .forbidden import run_forbidden
from .fastboot_arsenal import run_fastboot_arsenal
from .recovery_ops import run_recovery_ops


MODULES = {
    "dossier": run_dossier,
    "warhammer": run_warhammer,
    "darklab": run_dark_lab,
    "forbidden": run_forbidden,
    "fastboot": run_fastboot_arsenal,
    "recovery": run_recovery_ops,
}
