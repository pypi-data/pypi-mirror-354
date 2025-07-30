import pytest

from edupsyadmin.api.managers import (
    ClientNotFound,
    enter_client_cli,
    enter_client_untiscsv,
)

EXPECTED_KEYS = {
    "parent_encr",
    "class_name",
    "notenschutz",
    "nta_ersgew",
    "telephone1_encr",
    "class_int",
    "nos_rs_ausn",
    "nos_rs_ausn_faecher",
    "nta_vorlesen",
    "telephone2_encr",
    "estimated_date_of_graduation",
    "nta_zeitv_vieltext",
    "nta_other",
    "nta_notes",
    "email_encr",
    "document_shredding_date",
    "nos_les",
    "nta_zeitv_wenigtext",
    "nta_other_details",
    "first_name_encr",
    "notes_encr",
    "keyword_taetigkeitsbericht",
    "nachteilsausgleich",
    "nta_font",
    "last_name_encr",
    "client_id",
    "lrst_diagnosis",
    "nta_zeitv",
    "nta_aufg",
    "street_encr",
    "gender_encr",
    "school",
    "datetime_created",
    "nta_struktur",
    "n_sessions",
    "birthday_encr",
    "city_encr",
    "entry_date",
    "datetime_lastmodified",
    "nta_arbeitsm",
    "parent",
    "telephone1",
    "telephone2",
    "email",
    "first_name",
    "notes",
    "last_name",
    "street",
    "gender",
    "birthday",
    "city",
}


class ManagersTest:
    def test_add_client(self, mock_keyring, clients_manager, sample_client_dict):
        client_id = clients_manager.add_client(**sample_client_dict)
        client = clients_manager.get_decrypted_client(client_id=client_id)
        assert EXPECTED_KEYS.issubset(client.keys())
        assert client["first_name"] == sample_client_dict["first_name"]
        assert client["last_name"] == sample_client_dict["last_name"]
        mock_keyring.assert_called_with("example.com", "test_user_do_not_use")

    def test_edit_client(self, mock_keyring, clients_manager, sample_client_dict):
        client_id = clients_manager.add_client(**sample_client_dict)
        client = clients_manager.get_decrypted_client(client_id=client_id)
        updated_data = {
            "first_name_encr": "Jane",
            "last_name_encr": "Smith",
            "nta_zeitv_vieltext": 25,
            "nta_font": True,
        }
        clients_manager.edit_client(client_id, updated_data)
        updated_client = clients_manager.get_decrypted_client(client_id)

        print(f"Keys of the updated client: {updated_client.keys()}")

        assert EXPECTED_KEYS.issubset(updated_client.keys())
        assert updated_client["first_name"] == "Jane"
        assert updated_client["last_name"] == "Smith"

        assert updated_client["nta_zeitv_vieltext"] == 25
        assert updated_client["nta_font"] is True
        assert updated_client["nta_zeitv"] is True
        assert updated_client["nachteilsausgleich"] is True

        assert updated_client["nta_ersgew"] is False

        assert updated_client["datetime_lastmodified"] > client["datetime_lastmodified"]

        mock_keyring.assert_called_with("example.com", "test_user_do_not_use")

    def test_delete_client(self, clients_manager, sample_client_dict):
        client_id = clients_manager.add_client(**sample_client_dict)
        clients_manager.delete_client(client_id)
        try:
            clients_manager.get_decrypted_client(client_id)
            assert (
                False
            ), "Expected ClientNotFound exception when retrieving a deleted client"
        except ClientNotFound as e:
            assert e.client_id == client_id

    def test_enter_client_cli(
        self, mock_keyring, clients_manager, monkeypatch, sample_client_dict
    ):
        # simulate the commandline input
        inputs = iter(sample_client_dict)

        def mock_input(prompt):
            return sample_client_dict[next(inputs)]

        monkeypatch.setattr("builtins.input", mock_input)

        client_id = enter_client_cli(clients_manager)
        client = clients_manager.get_decrypted_client(client_id=client_id)
        assert EXPECTED_KEYS.issubset(client.keys())
        assert client["first_name"] == sample_client_dict["first_name"]
        assert client["last_name"] == sample_client_dict["last_name"]
        mock_keyring.assert_called_with("example.com", "test_user_do_not_use")

    def test_enter_client_untiscsv(
        self, mock_keyring, clients_manager, mock_webuntis, sample_client_dict
    ):
        client_id = enter_client_untiscsv(
            clients_manager, mock_webuntis, school=None, name="MustermMax1"
        )
        client = clients_manager.get_decrypted_client(client_id=client_id)
        assert EXPECTED_KEYS.issubset(client.keys())
        assert client["first_name"] == "Max"
        assert client["last_name"] == "Mustermann"
        assert client["school"] == "FirstSchool"
        mock_keyring.assert_called_with("example.com", "test_user_do_not_use")


# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
