# Set DIVIO_HOSTING environment variable before running the script
export DIVIO_HOSTING=True
export DEFAULT_STORAGE_ACCESS_KEY_ID='AKIA6EOIDQE3KXRV72NA'
export DEFAULT_STORAGE_SECRET_ACCESS_KEY='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'
export DEFAULT_STORAGE_BUCKET='beilage111-test-5d283a4e9cd740efae7c4ba-ac86959.divio-media.org'
export DEFAULT_STORAGE_REGION='eu-central-1'

# Run the script
python list_bucket_contents.py

# Optionally, unset the variables afterward
unset DIVIO_HOSTING
unset DEFAULT_STORAGE_ACCESS_KEY_ID
unset DEFAULT_STORAGE_SECRET_ACCESS_KEY
unset DEFAULT_STORAGE_BUCKET
unset DEFAULT_STORAGE_REGION
