from unittest.mock import AsyncMock

import pytest

from data_gouv_mcp_server.main import McpDataGouv


class TestSearchDatasets:

    @pytest.fixture
    def mock_http_client(self):
        return AsyncMock()

    @pytest.fixture
    def mcp_data_gouv_server(self, mock_http_client):
        return McpDataGouv(mock_http_client, "TestDataGouvFr")

    @pytest.mark.asyncio
    async def test_search_datasets_should_return_results_when_given_a_query(self, mock_http_client, mcp_data_gouv_server):
        # GIVEN
        query = "accidents route"
        mock_http_client.get_datasets.return_value = {
            "data": [
                {
                    "id": "dataset1",
                    "title": "Jeu de données test 1",
                    "description": "Description du premier jeu de données",
                    "page": "https://www.data.gouv.fr/fr/datasets/dataset1/",
                    "organization": {"name": "Organisation Test"},
                    "tags": ["tag1", "tag2", "tag3"],
                    "created_at": "2024-01-15T10:30:00",
                    "last_modified": "2024-02-20T14:45:00",
                    "resources": [
                        {"format": "csv"},
                        {"format": "json"}
                    ]
                },
                {
                    "id": "dataset2",
                    "title": "Jeu de données test 2",
                    "description": "Description du second jeu de données",
                    "page": "https://www.data.gouv.fr/fr/datasets/dataset2/",
                    "organization": None,
                    "tags": [],
                    "created_at": "",
                    "last_modified": "",
                    "resources": []
                }
            ],
            "total": 2
        }

        # WHEN
        mcp_response = await mcp_data_gouv_server._search_datasets_impl(query)

        # THEN

        assert mcp_response == {'nombre_resultats': 2,
                                'query': 'accidents route',
                                'resultats': [{'date_creation': '2024-01-15',
                                               'derniere_modification': '2024-02-20',
                                               'description': 'Description du premier jeu de données',
                                               'formats_disponibles': ['JSON', 'CSV'],
                                               'id': 'dataset1',
                                               'nombre_ressources': 2,
                                               'organisation': 'Organisation Test',
                                               'tags': ['tag1', 'tag2', 'tag3'],
                                               'titre': 'Jeu de données test 1',
                                               'url': 'https://www.data.gouv.fr/fr/datasets/dataset1/'},
                                              {'date_creation': '',
                                               'derniere_modification': '',
                                               'description': 'Description du second jeu de données',
                                               'formats_disponibles': [],
                                               'id': 'dataset2',
                                               'nombre_ressources': 0,
                                               'organisation': '',
                                               'tags': [],
                                               'titre': 'Jeu de données test 2',
                                               'url': 'https://www.data.gouv.fr/fr/datasets/dataset2/'}],
                                'total_disponible': 2}

    @pytest.mark.asyncio
    async def test_search_datasets_return_error_message_when_query_is_empty(self, mcp_data_gouv_server):
        # GIVEN
        query = ""

        # WHEN
        mcp_response = await mcp_data_gouv_server._search_datasets_impl(query)

        # THEN

        assert mcp_response == {'error': 'La requête de recherche ne peut pas être vide'}
