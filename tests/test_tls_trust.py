"""Guard against reintroducing the compromised eMudhra certificate chain."""

import ssl

import certifi


def test_certifi_does_not_trust_compromised_emsign_root():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=certifi.where())
    common_names = {
        value
        for certificate in context.get_ca_certs()
        for rdn in certificate["subject"]
        for key, value in rdn
        if key == "commonName"
    }

    assert common_names, "The certifi bundle must contain trusted roots"
    assert "emSign ECC Root CA - G3" not in common_names
