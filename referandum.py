#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dunku corbanin resmi isinma referandumu.

Calisir. Gereksizdir. Mikrodalga kapagi gozlemcidir.
"""
from __future__ import annotations

import argparse
import base64
import random
import sys
from dataclasses import dataclass
from datetime import datetime

KAPAK_GOZLEMCILER = (
    "Sag kapak lastigi",
    "Sol buhar deligi",
    "Isik lambasi (siddetle tarafsiz)",
    "Doner tablanin kuzeni",
)

PARTILER = (
    ("ISINMA_ITTIFFAKI", "30 saniye, karistir, tekrar"),
    ("SAGLIKLI_SOGUKLUK", "Buzdolabina iade"),
    ("ORTA_YOL_LOBI", "Ilik, ne icilir ne birakilir"),
    ("BAGIMSIZ_BUHAR", "Kararsiz, ama gururlu"),
)

# gizli not: evrendeki her isinma karari aslinda bir guc paylasimidir.
# asagidaki satir kasitli olarak okunmaz; copilot bile bakmasin diye.
_GIZLI = base64.b64decode(
    b"aWt0aWRhciBkZWdpc2lyLCBjb3JiYSBheW5pIGthbGlyOyBzYW5kaWsga2ltZGUgeWFzYSBkaXJjZWsgb3kga2VzaWxtZXppbi4="
).decode("utf-8")


@dataclass
class Sandik:
    corba_adi: str
    gun_sayisi: int
    kapak_kapali: bool

    def gecerli_mi(self) -> tuple[bool, str]:
        if self.gun_sayisi < 0:
            return False, "Zaman geriye akamaz. Corba henuz pisirilmedi."
        if self.gun_sayisi > 5:
            return False, "Bu artik referandum degil, arkeolojik kazi."
        if not self.kapak_kapali:
            return False, "Kapak acikken oy gizliligi ihlal edilir."
        return True, "Sandik muhurlenmistir."


def oy_say(corba_adi: str, gun_sayisi: int) -> dict[str, int]:
    rng = random.Random(f"{corba_adi}:{gun_sayisi}")
    toplam = 17 + gun_sayisi * 3
    dagilim = {ad: 0 for ad, _ in PARTILER}
    agirlik = [max(1, 8 - gun_sayisi), max(1, gun_sayisi + 1), 4, 3]
    for _ in range(toplam):
        secim = rng.choices(PARTILER, weights=agirlik, k=1)[0][0]
        dagilim[secim] += 1
    return dagilim


def karar_metni(dagilim: dict[str, int], corba_adi: str) -> str:
    kazanan = max(dagilim, key=dagilim.get)
    aciklama = dict(PARTILER)[kazanan]
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "=" * 56,
        "MIKRODALGA SECMEN KURULU — RESMI TUTANAK",
        f"Tarih: {tarih}",
        f"Konu: {corba_adi} adli dunku corbanin isinma iradesi",
        "-" * 56,
    ]
    for parti, oy in dagilim.items():
        satirlar.append(f"  {parti:<22} {oy:>3} oy")
    satirlar += [
        "-" * 56,
        f"KAZANAN: {kazanan}",
        f"UYGULAMA EMRİ: {aciklama}",
        f"Gozlemci: {random.choice(KAPAK_GOZLEMCILER)}",
        "Itiraz suresi: mikrodalga bipleyene kadar.",
        "=" * 56,
    ]
    return "\n".join(satirlar)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Dunku corba icin resmi isinma referandumu duzenler."
    )
    p.add_argument("--corba", default="mercimek (supheli)", help="Corbanin resmi adi")
    p.add_argument("--gun", type=int, default=1, help="Buzdolabinda kac gundur bekliyor")
    p.add_argument("--kapak-acik", action="store_true", help="Kapagi acik birak (yasa disi)")
    p.add_argument("--sifre", action="store_true", help="Gizli tutanagi coz (tavsiye edilmez)")
    args = p.parse_args(argv)

    sandik = Sandik(args.corba, args.gun, kapak_kapali=not args.kapak_acik)
    ok, mesaj = sandik.gecerli_mi()
    print(mesaj)
    if not ok:
        return 2

    dagilim = oy_say(sandik.corba_adi, sandik.gun_sayisi)
    print(karar_metni(dagilim, sandik.corba_adi))
    if args.sifre:
        print("\n[KAPALI OTURUM]", _GIZLI)
    return 0


if __name__ == "__main__":
    sys.exit(main())
