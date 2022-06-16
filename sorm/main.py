# -*- coding: utf-8 -*-
from ast import If
from mimetypes import init
import traceback
from typing import List, Tuple, DefaultDict
from collections import deque, defaultdict
from venv import create
import click, csv, sys
from cdr import Gcdr, Subscriber, Dvo, Interfacez, UserType, CallType, Reg

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    PrimaryKeyConstraint,
    create_engine,
)
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy_utils import database_exists, create_database
from pathlib import Path
from enum import Enum
from cdr_parser import cdr_parser

from utility import get_logger, set_variables, bcd_to_str, bcd_to_time, to_sec

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
#выбор птус
@click.option(
    "--ptus", type=click.Choice(["SK", "SV", "VV", "PO", "PI", "DV"], case_sensitive=False)
)
def main(files, ptus):
    # в зависимости от выбранного птус создает словарь 
    #     "log": log_file,
    #     "data": data_out,
    #     "dxt_release": tetra_version,
    #     "provider_id": provider_id,
    #     "url_db": url_db,
    var_dict = set_variables(ptus)
    logger = get_logger(var_dict.get("log"))
    #cdr - call data record
    for cdr_file in files:
        logger.info(f"Processing {cdr_file}")
        path = Path(cdr_file)
        try:
            out_buffers: Tuple[List[Gcdr], DefaultDict[str, List[Reg]]] = cdr_parser(
                path, var_dict.get("dxt_release"), var_dict.get("provider_id"), logger
            )
            write_to_csv(out_buffers, f'{var_dict.get("data")}/{Path(path).name}')
            write_to_db(out_buffers[1], var_dict.get("url_db"))
        except ValueError as err:
            logger.error(err)
            sys.exit(1)
        except AttributeError as err:
            logger.error(f"Check Tetra software release: {err}")
            track = traceback.format_exc()
            sys.exit(1)
        except Exception as exp:
            logger.error(f"No Tetra format or file corrupted: {exp}")
            sys.exit(1)
        finally:
            traceback.print_exc()

def write_to_db(reg_dict, url_db):
    """
    Write REGs record to db
    """
    conn, REGS_TABLE = init_db(url_db)
    buffer = []
    for nitsi in reg_dict:
        if len(reg_dict[nitsi]) > 0:
            for reg in reg_dict[nitsi]:
                buffer.append(reg.__dict__)
    if len(buffer):
        stmt = insert(REGS_TABLE).values(buffer)
        conn.execute(stmt.on_conflict_do_nothing())


def init_db(path):
    conn = None
    engine = create_engine(f"sqlite:///{path}", echo=True)
    metadata = MetaData()

    regs_table = Table(
        "regs",
        metadata,
        Column("_id", Integer, nullable=True),
        Column("_nitsi", String(12), nullable=True),
        Column("_location", Integer),
        Column("_prev_location", Integer),
        Column("_reg_at", DateTime),
        PrimaryKeyConstraint("_id", "_nitsi", name="reg_pk"),
    )
    # Create database if it does not exist.
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        conn = engine.connect()
    metadata.create_all(engine)
    return conn, regs_table


def write_to_csv(
    out_buffers: Tuple[List[Gcdr], DefaultDict[str, List[Reg]]], file: str
):
    cdr_buff, reg_buff = out_buffers
    # Write gcdrs to file
    with open(file, "w+", newline="") as csv_file:
        wr = csv.writer(csv_file, delimiter=";")
        for cdr in cdr_buff:
            cdr.abon_a.get_last_location(reg_buff, cdr.date, cdr.call_duration)
            cdr.abon_b.get_last_location(reg_buff, cdr.date, cdr.call_duration)
            wr.writerow(list(cdr))


if __name__ == "__main__":
    main()
