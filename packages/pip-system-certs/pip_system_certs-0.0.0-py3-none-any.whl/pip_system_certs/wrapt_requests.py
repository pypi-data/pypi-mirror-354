import truststore

_injected = False

def inject_truststore():
    global _injected
    if not _injected:
        try:
            truststore.inject_into_ssl()
            _injected = True
        except Exception as ex:
            print("pip_system_certs: ERROR: could not inject truststore:", ex)
