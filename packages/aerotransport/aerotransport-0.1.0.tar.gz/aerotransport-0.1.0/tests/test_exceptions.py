import pytest

from aerotransport.exceptions import AerotransportError


def test_aerotransport_error_message():
    with pytest.raises(AerotransportError) as excinfo:
        raise AerotransportError("Mensaje de error personalizado")
    assert "Mensaje de error personalizado" in str(excinfo.value)
