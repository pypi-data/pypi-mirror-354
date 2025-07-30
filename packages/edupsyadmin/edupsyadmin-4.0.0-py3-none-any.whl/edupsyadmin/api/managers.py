import logging  # just for interaction with the sqlalchemy logger
import os
import pathlib
from datetime import datetime
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from edupsyadmin.api.add_convenience_data import add_convenience_data
from edupsyadmin.api.clients import Client
from edupsyadmin.api.fill_form import fill_form
from edupsyadmin.api.taetigkeitsbericht_check_key import check_keyword
from edupsyadmin.core.config import config
from edupsyadmin.core.encrypt import Encryption
from edupsyadmin.core.logger import logger

BOOLEAN_COLS = [
    "notenschutz",
    "nos_rs",
    "nos_rs_ausn",
    "nos_les",
    "nachteilsausgleich",
    "nta_zeitv",
    "nta_font",
    "nta_aufg",
    "nta_struktur",
    "nta_arbeitsm",
    "nta_ersgew",
    "nta_vorlesen",
    "nta_other",
    "nta_nos_end",
]


class Base(DeclarativeBase):
    pass


encr = Encryption()


class ClientNotFound(Exception):
    def __init__(self, client_id: int):
        self.client_id = client_id
        super().__init__(f"Client with ID {client_id} not found.")


class ClientsManager:
    def __init__(
        self,
        database_url: str,
        app_uid: str,
        app_username: str,
        salt_path: str | os.PathLike[str],
    ):
        # set up logging for sqlalchemy
        logging.getLogger("sqlalchemy.engine").setLevel(config.core.logging)

        # connect to database
        logger.info(f"trying to connect to database at {database_url}")
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

        # set fernet for encryption
        encr.set_fernet(app_username, salt_path, app_uid)

        # create the table if it doesn't exist
        Base.metadata.create_all(self.engine, tables=[Client.__table__])
        logger.info(f"created connection to database at {database_url}")

    def add_client(self, **client_data: Any) -> int:
        logger.debug("trying to add client")
        with self.Session() as session:
            new_client = Client(encr, **client_data)
            session.add(new_client)
            session.commit()
            logger.info(f"added client: {new_client}")
            client_id = new_client.client_id
            return client_id

    def get_decrypted_client(self, client_id: int) -> dict[str, Any]:
        # TODO: move encryption logic to clients.py?
        logger.debug(f"trying to access client (client_id = {client_id})")
        with self.Session() as session:
            client = session.query(Client).filter_by(client_id=client_id).first()
            if client is None:
                raise ClientNotFound(client_id)
            client_dict = client.__dict__
            decr_vars = {}
            for attributekey in client_dict.keys():
                if attributekey.endswith("_encr"):
                    attributekey_decr = attributekey.removesuffix("_encr")
                    try:
                        decr_vars[attributekey_decr] = encr.decrypt(
                            client_dict[attributekey]
                        )
                    except:
                        logger.critical(
                            (
                                f"attribute: {attributekey}; "
                                f"value: {client_dict[attributekey]}"
                            )
                        )
                        raise
            client_dict.update(decr_vars)
            return client_dict

    def get_clients_overview(self, nta_nos: bool = True) -> pd.DataFrame:
        logger.debug("trying to query client data")
        stmt = select(Client)
        with self.Session() as session:
            if nta_nos:
                stmt = stmt.where(
                    (Client.notenschutz == 1) or (Client.nachteilsausgleich == 1)
                )
            results = session.scalars(stmt).all()
            results_list_of_dict = [
                {
                    "client_id": entry.client_id,
                    "school": entry.school,
                    "last_name": encr.decrypt(entry.last_name_encr),
                    "first_name": encr.decrypt(entry.first_name_encr),
                    "class_name": entry.class_name,
                    "notenschutz": entry.notenschutz,
                    "nachteilsausgleich": entry.nachteilsausgleich,
                    "lrst_diagnosis": entry.lrst_diagnosis,
                    "n_sessions": entry.n_sessions,
                    "keyword_taetigkeitsbericht": entry.keyword_taetigkeitsbericht,
                }
                for entry in results
            ]
            df = pd.DataFrame(results_list_of_dict)
            return df.sort_values(["school", "last_name"])

    def get_data_raw(self) -> pd.DataFrame:
        """
        Get the data without decrypting encrypted data.
        """
        logger.debug("trying to query the entire database")
        with self.Session() as session:
            query = session.query(Client).statement
            df = pd.read_sql_query(query, session.bind)
        return df

    def edit_client(self, client_id: int, new_data: dict[str, Any]) -> None:
        # TODO: Warn if key does not exist
        # TODO: If key does not exist, check if key + _encr exists and use it
        logger.debug(f"editing client (id = {client_id})")
        with self.Session() as session:
            client = session.query(Client).filter_by(client_id=client_id).first()
            if client:
                for key, value in new_data.items():
                    logger.debug(f"changing value for key: {key}")
                    if key.endswith("_encr"):
                        setattr(client, key, encr.encrypt(value))
                    else:
                        setattr(client, key, value)
                client.datetime_lastmodified = datetime.now()
                session.commit()
            else:
                logger.error("client could not be found!")

    def delete_client(self, client_id: int) -> None:
        logger.debug("deleting client")
        with self.Session() as session:
            client = session.query(Client).filter_by(client_id=client_id).first()
            if client:
                session.delete(client)
                session.commit()


def new_client(
    app_username: str,
    app_uid: str,
    database_url: str,
    salt_path: str | os.PathLike[str],
    csv: str | os.PathLike[str] | None = None,
    school: str | None = None,
    name: str | None = None,
    keepfile: bool = False,
) -> None:
    clients_manager = ClientsManager(
        database_url=database_url,
        app_uid=app_uid,
        app_username=app_username,
        salt_path=salt_path,
    )
    if csv:
        if name is None:
            raise ValueError("Pass a name to read a client from a csv.")
        enter_client_untiscsv(clients_manager, csv, school, name)
        if not keepfile:
            os.remove(csv)
    else:
        enter_client_cli(clients_manager)


def set_client(
    app_username: str,
    app_uid: str,
    database_url: str,
    salt_path: str | os.PathLike[str],
    client_id: int,
    key_value_pairs: list[str],
) -> None:
    """
    Set the value for a key given a client_id
    """
    clients_manager = ClientsManager(
        database_url=database_url,
        app_uid=app_uid,
        app_username=app_username,
        salt_path=salt_path,
    )
    pairs_list = [pair.split("=", 1) for pair in key_value_pairs]
    new_data: dict[str, str | bool | None] = {}
    for key, value in pairs_list:
        # TODO: use `validate` methods in clients.py
        if key in BOOLEAN_COLS:
            # TODO: Add try-except
            new_data[key] = bool(int(value))
        elif key == "keyword_taetigkeitsbericht":
            new_data[key] = check_keyword(value)
        else:
            new_data[key] = value
    clients_manager.edit_client(client_id, new_data)


def get_clients(
    app_username: str,
    app_uid: str,
    database_url: str,
    salt_path: str | os.PathLike[str],
    nta_nos: bool = False,
    client_id: int | None = None,
    out: str | None = None,
) -> None:
    clients_manager = ClientsManager(
        database_url=database_url,
        app_uid=app_uid,
        app_username=app_username,
        salt_path=salt_path,
    )
    if client_id:
        original_df = pd.DataFrame([clients_manager.get_decrypted_client(client_id)]).T
        df = original_df[
            ~(
                original_df.index.str.endswith("_encr")
                | (original_df.index == "_sa_instance_state")
            )
        ]
    else:
        original_df = clients_manager.get_clients_overview(nta_nos=nta_nos)
        df = original_df.set_index("client_id")
    if out:
        df.to_csv(out)
    else:
        with pd.option_context(
            "display.max_columns",
            None,
            "display.width",
            None,
            "display.max_colwidth",
            None,
            "display.expand_frame_repr",
            False,
        ):
            print(df)


def get_data_raw(
    app_username: str,
    app_uid: str,
    database_url: str,
    salt_path: str | os.PathLike[str],
) -> pd.DataFrame:
    clients_manager = ClientsManager(
        database_url=database_url,
        app_uid=app_uid,
        app_username=app_username,
        salt_path=salt_path,
    )
    df = clients_manager.get_data_raw()
    return df


def enter_client_untiscsv(
    clients_manager: ClientsManager,
    csv: str | os.PathLike[str],
    school: str | None,
    name: str,
) -> int:
    """
    Read client from a webuntis csv

    :param clients_manager: a ClientsManager instance used to add the client to the db
    :param csv: path to a tab separated webuntis export file
    :param school: short name of the school as set in the config file
    :param name: name of the client as specified in the "name" column of the csv
    return: client_id
    """
    untis_df = pd.read_csv(csv, sep="\t", encoding="utf-8")
    client_series = untis_df[untis_df["name"] == name]

    # check if id is known
    if "client_id" in client_series.columns:
        client_id = client_series["client_id"].item()
    else:
        client_id = None

    # check if school was passed and if not use the first from the config
    if school is None:
        school = list(config.school.keys())[0]

    client_id_n = clients_manager.add_client(
        school=school,
        gender=client_series["gender"].item(),
        entry_date=datetime.strptime(
            client_series["entryDate"].item(), "%d.%m.%Y"
        ).strftime("%Y-%m-%d"),
        class_name=client_series["klasse.name"].item(),
        first_name=client_series["foreName"].item(),
        last_name=client_series["longName"].item(),
        birthday=datetime.strptime(
            client_series["birthDate"].item(), "%d.%m.%Y"
        ).strftime("%Y-%m-%d"),
        street=client_series["address.street"].item(),
        city=str(client_series["address.postCode"].item())
        + " "
        + client_series["address.city"].item(),
        telephone1=str(
            client_series["address.mobile"].item()
            or client_series["address.phone"].item()
        ),
        email=client_series["address.email"].item(),
        client_id=client_id,
    )
    return client_id_n


def enter_client_cli(clients_manager: ClientsManager) -> int:
    client_id_input = input("client_id (press ENTER if you don't know): ")
    client_id = int(client_id_input) if client_id_input else None

    while True:
        school = input("School: ")
        if school in config.school.keys():
            break
        print(f"School must be one of the following strings: {config.schools.keys()}")

    client_id_n = clients_manager.add_client(
        school=school,
        gender=input("Gender (f/m): "),
        entry_date=input("Entry date (YYYY-MM-DD): "),
        class_name=input("Class name: "),
        first_name=input("First Name: "),
        last_name=input("Last Name: "),
        birthday=input("Birthday (YYYY-MM-DD): "),
        street=input("Street and house number: "),
        city=input("City (postcode + name): "),
        telephone1=input("Telephone: "),
        email=input("Email: "),
        client_id=client_id,
    )
    return client_id_n


def create_documentation(
    app_username: str,
    app_uid: str,
    database_url: str,
    salt_path: str | os.PathLike[str],
    client_id: int,
    form_set: str | None = None,
    form_paths: list[str] = [],
) -> None:
    clients_manager = ClientsManager(
        database_url=database_url,
        app_uid=app_uid,
        app_username=app_username,
        salt_path=salt_path,
    )
    if form_set:
        form_paths.extend(config.form_set[form_set])
    elif not form_paths:
        raise ValueError("At least one of 'form_set' or 'form_paths' must be non-empty")
    form_paths_normalized = [_normalize_path(p) for p in form_paths]
    logger.debug(f"Trying to fill the files: {form_paths_normalized}")
    client_dict = clients_manager.get_decrypted_client(client_id)
    client_dict_with_convenience_data = add_convenience_data(client_dict)
    fill_form(client_dict_with_convenience_data, form_paths_normalized)


def _normalize_path(path_str: str) -> str:
    path = pathlib.Path(os.path.expanduser(path_str))
    return str(path.resolve())


def delete_client(
    app_username: str,
    app_uid: str,
    database_url: str,
    salt_path: str | os.PathLike[str],
    client_id: int,
) -> None:
    clients_manager = ClientsManager(
        database_url=database_url,
        app_uid=app_uid,
        app_username=app_username,
        salt_path=salt_path,
    )
    clients_manager.delete_client(client_id)
