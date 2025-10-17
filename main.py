"""
Arquivo inicial do projeto.

Fornece um ponto de entrada simples com parsing de argumentos, logging e carregamento básico de configuração.
Idioma: pt-br
"""

from __future__ import annotations
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict


__version__ = "0.1.0"


def setup_logging(verbose: bool) -> None:
    """Configura o logging básico."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Analisa os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description="Início do projeto - esqueleto")
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Caminho para arquivo de configuração JSON (opcional)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Ativa modo verboso (debug)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Exibe a versão e sai",
    )
    return parser.parse_args(argv)


def load_config(path: Path | None) -> Dict[str, Any]:
    """Carrega configuração a partir de um arquivo JSON. Retorna configurações padrão se não existir."""
    default_config: Dict[str, Any] = {"app_name": "meu_projeto", "workers": 1}
    if path is None:
        return default_config
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            logging.warning("Configuração inválida: esperado objeto JSON. Usando padrão.")
            return default_config
        return {**default_config, **data}
    except FileNotFoundError:
        logging.warning("Arquivo de configuração não encontrado: %s. Usando padrão.", path)
        return default_config
    except json.JSONDecodeError:
        logging.warning("Erro ao decodificar JSON em %s. Usando padrão.", path)
        return default_config
    except Exception as exc:
        logging.error("Erro ao carregar configuração: %s", exc)
        return default_config


def run(config: Dict[str, Any]) -> int:
    """Lógica principal do programa. Retorna código de saída."""
    logger = logging.getLogger("app")
    logger.info("Iniciando %s (workers=%s)", config.get("app_name"), config.get("workers"))
    # TODO: implementar lógica do projeto aqui
    logger.debug("Config completa: %s", config)
    logger.info("Execução concluída com sucesso.")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Função principal invocada ao executar o script."""
    args = parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    setup_logging(args.verbose)
    config = load_config(args.config)
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))