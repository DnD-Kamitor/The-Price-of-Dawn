#!/usr/bin/env bash
# Wrapper: curl with mTLS cert for research-ready.nl
# Usage: mtls_curl.sh [curl args...]
# Cert extracted from ~/Desktop/fedora.p12 password Research-mTLS-2024!

CERT="/tmp/mtls_client.crt"
KEY="/tmp/mtls_client.key"

if [ ! -f "$CERT" ] || [ ! -f "$KEY" ]; then
  echo "Extracting mTLS cert..." >&2
  openssl pkcs12 -in ~/Desktop/fedora.p12 -clcerts -nokeys -out "$CERT" \
    -passin pass:"Research-mTLS-2024!" 2>/dev/null
  openssl pkcs12 -in ~/Desktop/fedora.p12 -nocerts -nodes -out "$KEY" \
    -passin pass:"Research-mTLS-2024!" 2>/dev/null
fi

exec curl --cert "$CERT" --key "$KEY" "$@"
