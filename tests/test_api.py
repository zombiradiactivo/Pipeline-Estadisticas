import pytest
from src.app import app


@pytest.fixture
def cliente():
    """Fixture que inicializa el cliente de pruebas de Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(cliente):
    res = cliente.get('/salud')
    assert res.status_code == 200
    assert res.get_json() == {"estado": "ok"}


def test_endpoint_estadisticas_success(cliente):
    payload = {"datos": [10, 20, 30]}
    res = cliente.post('/estadisticas', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["media"] == 20.0


def test_endpoint_estadisticas_error_vacio(cliente):
    res = cliente.post('/estadisticas', json={"datos": []})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_endpoint_outliers(cliente):
    payload = {"datos": [1, 1, 1, 1, 1, 100]}
    res = cliente.post('/outliers', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert 100 in data["outliers"]


def test_endpoint_estadisticas_sin_clave_datos(cliente):
    # Cubre validación de 'datos' not in contenido
    res = cliente.post('/estadisticas', json={"numeros": [1, 2]})
    assert res.status_code == 400
    assert "Se requiere una lista de 'datos'" in res.get_json()["error"]


def test_endpoint_estadisticas_no_es_lista(cliente):
    # Cubre validación isinstance(..., list)
    res = cliente.post('/estadisticas', json={"datos": "no soy lista"})
    assert res.status_code == 400


def test_endpoint_outliers_error_formato(cliente):
    # Cubre bloques de excepción en outliers
    res = cliente.post('/outliers', json={"datos": ["no_soy_numero"]})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_endpoint_estadisticas_json_mal_formado(cliente):
    # Cubre el caso de contenido is None (silent=True)
    res = cliente.post('/estadisticas',
                       data="esto no es json",
                       content_type='application/json')
    assert res.status_code == 400
