#!/usr/bin/env python3
"""Собирает карточку для Hugging Face: YAML-заголовок + общий README.

Зачем отдельный шаг. Первый прогон синхронизации залил на HF обычный README, у которого
заголовка нет, — и карточка обнулилась: слетели лицензия, теги и настройка просмотрщика
(cardData стал None). Заголовок обязателен, без него файл для них просто текст.

Заголовок лежит в tools/hf_card.yml и правится там; тело берётся из README.md, чтобы
описание не пришлось поддерживать в двух местах. Ссылка на просмотрщик заменяется:
на самой странице HF он и так сверху, вести оттуда на него же незачем.
"""
import io
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
header = io.open(os.path.join(HERE, "tools/hf_card.yml"), encoding="utf-8").read().rstrip("\n")
body = io.open(os.path.join(HERE, "README.md"), encoding="utf-8").read()

body = body.replace(
    "**[open the dataset viewer]"
    "(https://huggingface.co/datasets/Smurfetc/solana-memecoin-calls/viewer/default/train)**",
    "**Use the viewer at the top of this page** — the table above the card is the dataset itself.")

# зеркало на GitHub упоминаем в шапке карточки
body = body.replace(
    "dataset page: **[smugcalls.com/data.html](https://smugcalls.com/data.html)**",
    "dataset page: **[smugcalls.com/data.html](https://smugcalls.com/data.html)** ·\n"
    "mirror: **[github.com/Smurfetc/solana-memecoin-calls-dataset]"
    "(https://github.com/Smurfetc/solana-memecoin-calls-dataset)**", 1)

out = "---\n%s\n---\n\n%s" % (header, body)
path = os.path.join(HERE, "README_hf.md")
io.open(path, "w", encoding="utf-8").write(out)
print("собрана карточка HF: %d байт, заголовок из %d строк"
      % (len(out), len(header.splitlines())))
