# Set DIVIO_HOSTING environment variable before running the script
export DIVIO_HOSTING=True
export DEFAULT_STORAGE_ACCESS_KEY_ID='AKIA2UXM2NNWBHDLPHHY'
export DEFAULT_STORAGE_SECRET_ACCESS_KEY='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'
export DEFAULT_STORAGE_BUCKET='beilage111-test-5d283a4e9cd740efae7c4ba-64f17a2.divio-media.net'
export DEFAULT_STORAGE_REGION='eu-central-1'

# Run the script
python list_bucket_contents.py

# Optionally, unset the variables afterward
unset DIVIO_HOSTING
unset DEFAULT_STORAGE_ACCESS_KEY_ID
unset DEFAULT_STORAGE_SECRET_ACCESS_KEY
unset DEFAULT_STORAGE_BUCKET
unset DEFAULT_STORAGE_REGION
